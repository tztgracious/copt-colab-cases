"""Turn the downloaded cardopt.com case zips into a Colab-ready notebook repo.

  python tools/build_repo.py                      # rebuild notebooks/ from _zips/
  python tools/build_repo.py --repo owner/name    # also regenerate README.md links
"""
import argparse, json, pathlib, re, shutil, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ZIPS, OUT = ROOT / "_zips", ROOT / "notebooks"

INSTALL_MD = (
    "> **Open in Google Colab.** The next cell installs `coptpy`. The bundled free "
    "license is size-limited but covers this case. Then run *Runtime > Run all*.\n"
)
# module name -> pip name, for third-party imports found in a case
PIP_NAME = {"sklearn": "scikit-learn", "cv2": "opencv-python", "PIL": "pillow",
            "yaml": "pyyaml", "skimage": "scikit-image", "mpl_toolkits": "matplotlib"}
# never pip-install these: stdlib or provided by Colab already
STDLIB = set(sys.stdlib_module_names) | {"coptpy", "google", "__future__"}


def imports_of(nb):
    """Third-party top-level modules a notebook imports."""
    found = set()
    for c in nb.get("cells", []):
        if c.get("cell_type") != "code":
            continue
        src = "".join(c.get("source", []))
        for m in re.finditer(r"^\s*(?:from|import)\s+([A-Za-z_][\w.]*)", src, re.M):
            top = m.group(1).split(".")[0]
            if top not in STDLIB:
                found.add(PIP_NAME.get(top, top))
    return found


def install_cell(extra):
    pkgs = " ".join(["coptpy"] + sorted(extra))
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": ["# COPT Python API and this case's dependencies\n",
                       f"%pip install -q {pkgs}\n"]}


KERNEL = {"display_name": "Python 3", "language": "python", "name": "python3"}


def slug(title):
    return re.sub(r"_+", "_", re.sub(r"[^0-9A-Za-z]+", "_", title)).strip("_")


def colab_ready(nb):
    # a few cases ship a conda bootstrap that cannot work on Colab
    for c in nb.get("cells", []):
        src = "".join(c.get("source", []))
        if c.get("cell_type") == "code" and "conda create" in src:
            c["source"] = ["# Colab has no conda; install this case's requirements with pip\n",
                           "%pip install -q -r requirements.txt\n"]
            c["outputs"] = []
        elif c.get("cell_type") == "markdown" and "conda" in src.lower():
            c["source"] = ["## Install Dependencies\n",
                           "Run the cell below to install this case's packages "
                           "(`requirements.txt`) into the Colab runtime. "
                           "No environment switch or kernel change is needed.\n"]

    head = "".join("".join(c.get("source", [])) for c in nb.get("cells", [])[:4])
    if "pip install" not in head:
        nb["cells"][:0] = [
            {"cell_type": "markdown", "metadata": {}, "source": [INSTALL_MD]},
            install_cell(imports_of(nb)),
        ]
    md = nb.setdefault("metadata", {})
    md["colab"] = {"provenance": [], "toc_visible": True}
    md["kernelspec"] = dict(KERNEL)      # vendor zips carry kernels that do not exist elsewhere
    md.pop("language_info", None)
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


STATUS_ICON = {"ok": "\u2705", "license": "\U0001f511", "issue": "\u26a0\ufe0f"}


def load_status():
    f = ROOT / "status.tsv"
    if not f.exists():
        return {}
    out = {}
    for line in f.read_text().splitlines():
        if line.strip():
            title, kind, note = line.split("\t")
            out[title] = (kind, note)
    return out


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
        "Every case below was executed end to end on a bare Colab-like runtime with nothing",
        "but `pip install coptpy`. \u2705 runs as is; \U0001f511 solves only with a licensed COPT",
        "(the model is larger than the free build allows); \u26a0\ufe0f has a known glitch, noted inline.",
        "The free build caps a MIP at 2000 variables and 2000 constraints, and a pure LP at 10000",
        "of each.", "",
        "| | Case | Level | Domain | Colab | Source |", "|---|---|---|---|---|---|",
    ]
    status = load_status()
    notes = []
    for c in cases:
        if not c.get("path"):
            continue
        kind, note = status.get(c["title"], ("ok", ""))
        icon = STATUS_ICON.get(kind, "")
        link = base + c["path"].replace(" ", "%20")
        lines.append(f'| {icon} | {c["title"]} | {c["difficulty"]} | {c["scene"]} | '
                     f'[![Open In Colab]({badge})]({link}) | [doc]({c["source"]}) |')
        if note:
            notes.append(f'- **{c["title"]}** {icon} — {note}')
    if notes:
        lines += ["", "### Notes", ""] + notes
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
