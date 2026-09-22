"""Turn the downloaded cardopt.com case zips into a Colab-ready notebook repo.

  python tools/build_repo.py                      # rebuild notebooks/ from _zips/
  python tools/build_repo.py --repo owner/name    # also regenerate README.md links
"""
import argparse, json, pathlib, re, shutil, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ZIPS, OUT = ROOT / "_zips", ROOT / "notebooks"

INSTALL_MD = (
    "> **Open in Google Colab.** The next cell installs `coptpy`. The bundled free "
    "license is size-limited but covers this case. Then run *Runtime > Run all*.\n"
)
INSTALL_CODE = ["# COPT Python API\n", "%pip install -q coptpy\n"]


def slug(title):
    return re.sub(r"_+", "_", re.sub(r"[^0-9A-Za-z]+", "_", title)).strip("_")


def colab_ready(nb):
    head = "".join("".join(c.get("source", [])) for c in nb.get("cells", [])[:4])
    if "pip install" not in head:
        nb["cells"][:0] = [
            {"cell_type": "markdown", "metadata": {}, "source": [INSTALL_MD]},
            {"cell_type": "code", "execution_count": None, "metadata": {},
             "outputs": [], "source": INSTALL_CODE},
        ]
    nb.setdefault("metadata", {})["colab"] = {"provenance": [], "toc_visible": True}
    return nb


def data_cell(case_dir, files, repo, branch):
    """Colab loads only the .ipynb, so a case with data files must fetch them."""
    base = f"https://raw.githubusercontent.com/{repo}/{branch}/notebooks/{case_dir}/"
    listing = ",\n    ".join(repr(f) for f in sorted(files))
    src = (
        "# This case needs data files. Colab opens the notebook alone, so fetch them here.\n"
        "import os, urllib.parse, urllib.request\n"
        f"BASE = {base!r}\n"
        f"FILES = [\n    {listing},\n]\n"
        "for f in FILES:\n"
        "    if not os.path.exists(f):\n"
        "        os.makedirs(os.path.dirname(f) or '.', exist_ok=True)\n"
        "        urllib.request.urlretrieve(BASE + urllib.parse.quote(f), f)\n"
        "print(len(FILES), 'data file(s) ready')"
    )
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": [l + "\n" for l in src.split("\n")]}


def load_manifest():
    rows = []
    for line in (ROOT / "manifest.tsv").read_text().splitlines():
        if not line.strip():
            continue
        cid, title, diff, scene, path = line.split("\t")
        rows.append({"id": cid, "title": title, "difficulty": diff, "scene": scene,
                     "zip": path.rsplit("/", 1)[-1],
                     "source": f"https://www.cardopt.com/copt-document/detail?docType=4&id={cid}"})
    return rows


SKIP_DIRS = ("__MACOSX", ".ipynb_checkpoints")


def keep(name):
    parts = pathlib.PurePosixPath(name).parts
    return not (name.endswith("/")
                or any(d in parts for d in SKIP_DIRS)
                or any(pt.startswith(".") for pt in parts))


def strip_root(names):
    """Drop the single common top-level folder a zip may wrap everything in."""
    tops = {pathlib.PurePosixPath(n).parts[0] for n in names}
    if len(tops) == 1 and all(len(pathlib.PurePosixPath(n).parts) > 1 for n in names):
        top = tops.pop()
        return {n: pathlib.PurePosixPath(n).relative_to(top).as_posix() for n in names}
    return {n: n for n in names}


def pick_primary(rel_nbs, case):
    """The notebook the README should link to."""
    def score(r):
        stem = pathlib.PurePosixPath(r).stem.lower()
        return (0 if "coding" in stem else 1,
                0 if "original" in stem else 1,
                0 if stem.endswith(("_en", "-en")) else 1,
                len(pathlib.PurePosixPath(r).parts), stem)
    return sorted(rel_nbs, key=score)[0]


def build_one(case, repo, branch):
    zf = zipfile.ZipFile(ZIPS / case["zip"])
    names = [n for n in zf.namelist() if keep(n)]
    rel = strip_root(names)
    nbs = {n: r for n, r in rel.items() if r.endswith(".ipynb")}
    if not nbs:
        return None
    extras = {n: r for n, r in rel.items() if not r.endswith(".ipynb")}
    name = slug(case["title"])

    flat = len(nbs) == 1 and not extras
    dest = OUT if flat else OUT / name
    dest.mkdir(parents=True, exist_ok=True)

    boot = data_cell(name, extras.values(), repo, branch) if extras else None

    written = {}
    for n, r in nbs.items():
        out = dest / (name + ".ipynb") if flat else dest / r
        out.parent.mkdir(parents=True, exist_ok=True)
        nb = colab_ready(json.loads(zf.read(n).decode("utf-8")))
        if boot and not any("raw.githubusercontent" in "".join(c.get("source", []))
                            for c in nb["cells"][:4]):
            nb["cells"].insert(2, json.loads(json.dumps(boot)))
        out.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
        written[r] = out
    for n, r in extras.items():
        out = dest / r
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(zf.read(n))

    primary = written[pick_primary(list(written), case)]
    return primary.relative_to(ROOT).as_posix()


def readme(cases, repo, branch):
    base = f"https://colab.research.google.com/github/{repo}/blob/{branch}/"
    badge = "https://colab.research.google.com/assets/colab-badge.svg"
    lines = [
        "# COPT Application Cases for Google Colab", "",
        "Every [COPT](https://www.cardopt.com/) application case from the Cardinal Operations",
        "documentation site, packaged so it runs in Google Colab with one click. Each notebook",
        "opens with a `pip install coptpy` cell; the bundled free license is size-limited but",
        "covers every case here, so no license file is needed.", "",
        "| Case | Level | Domain | Colab | Source |", "|---|---|---|---|---|",
    ]
    for c in cases:
        if not c.get("path"):
            continue
        link = base + c["path"].replace(" ", "%20")
        lines.append(f'| {c["title"]} | {c["difficulty"]} | {c["scene"]} | '
                     f'[![Open In Colab]({badge})]({link}) | [doc]({c["source"]}) |')
    lines += ["", "## Rebuilding", "",
              "`tools/copt_cases.py` scrapes the case list and zips from cardopt.com;",
              "`tools/build_repo.py` unpacks them into `notebooks/` and regenerates this table:", "",
              "```bash", "python tools/copt_cases.py --out _zips --raw",
              f"python tools/build_repo.py --repo {repo} --branch {branch}", "```", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="OWNER/REPO")
    ap.add_argument("--branch", default="main")
    a = ap.parse_args()

    try:                      # some mounts disallow deletes; overwriting is fine
        if OUT.exists():
            shutil.rmtree(OUT)
    except OSError:
        pass
    OUT.mkdir(parents=True, exist_ok=True)
    cases = load_manifest()
    for c in cases:
        try:
            c["path"] = build_one(c, a.repo, a.branch)
            print(("ok   " if c["path"] else "SKIP ") + c["title"] + " -> " + str(c.get("path")))
        except Exception as e:                                           # noqa: BLE001
            c["path"] = None
            print(f'FAIL {c["title"]}: {type(e).__name__}: {e}')
    (ROOT / "README.md").write_text(readme(cases, a.repo, a.branch), encoding="utf-8")
    print(f'\n{sum(1 for c in cases if c.get("path"))}/{len(cases)} notebooks written')


if __name__ == "__main__":
    main()
