"""Turn the downloaded cardopt.com case zips into a Colab/ModelWhale-ready notebook repo.

Layout:  notebooks/en/<Case>...   notebooks/zh/<Case>...
Case folder names are the ASCII slug of the English title in both trees, so the
two mirror each other and the ModelWhale clone command differs only by `en`/`zh`.

  python tools/build_repo.py --repo tztgracious/copt-colab-cases
"""
import argparse, json, pathlib, re, shutil, sys, urllib.parse, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "notebooks"
ZIPS = {"en": ROOT / "_zips", "zh": ROOT / "_zips_zh"}

INSTALL_MD = {
    "en": "> **Open in Google Colab.** The next cell installs `coptpy`. The bundled free "
          "license is size-limited but covers this case. Then run *Runtime > Run all*.\n",
    "zh": "> **在线运行说明。** 下一格安装 `coptpy`。内置的免费许可有规模上限，但足够跑通本案例。"
          "然后执行「运行所有」。\n",
}

# module name -> pip name, for third-party imports found in a case
PIP_NAME = {"sklearn": "scikit-learn", "cv2": "opencv-python", "PIL": "pillow",
            "yaml": "pyyaml", "skimage": "scikit-image", "mpl_toolkits": "matplotlib"}
STDLIB = set(sys.stdlib_module_names) | {"coptpy", "google", "__future__"}

KERNEL = {"display_name": "Python 3", "language": "python", "name": "python3"}

# Colab and ModelWhale runtimes ship no CJK font, and the cases ask for SimHei /
# Microsoft YaHei / PingFang, which exist only on Windows and macOS. Naming a font
# that is absent is worse than naming none: matplotlib pins that family and the
# labels come out as tofu boxes. So a GB2312 subset of Noto Sans CJK SC (SIL OFL)
# ships in assets/ and is registered ahead of whatever the notebook asks for.
FONT_FILE = "NotoSansCJKsc-Regular-subset.otf"
FONT_NAME = "Noto Sans CJK SC"


def font_cell(repo, branch):
    src = (
        "# \u4e2d\u6587\u5b57\u4f53\uff1a\u8fd0\u884c\u73af\u5883\u901a\u5e38\u6ca1\u6709 CJK \u5b57\u4f53\uff0c"
        "\u6ce8\u518c\u968f\u4ed3\u5e93\u5206\u53d1\u7684\u601d\u6e90\u9ed1\u4f53\u5b50\u96c6\n"
        "import os, urllib.request, matplotlib, matplotlib.font_manager as fm\n"
        f"FONT = {FONT_FILE!r}\n"
        "CAND = [FONT, os.path.join('..', 'assets', FONT), os.path.join('..', '..', 'assets', FONT),\n"
        "        os.path.join('assets', FONT)]\n"
        "URLS = [\n"
        f"    'https://gitee.com/{repo}/raw/{branch}/assets/' + FONT,\n"
        f"    'https://raw.githubusercontent.com/{repo}/{branch}/assets/' + FONT,\n"
        "]\n"
        "path = next((p for p in CAND if os.path.exists(p)), None)\n"
        "if path is None:\n"
        "    for u in URLS:\n"
        "        try:\n"
        "            urllib.request.urlretrieve(u, FONT); path = FONT; break\n"
        "        except Exception:\n"
        "            continue\n"
        "if path:\n"
        "    fm.fontManager.addfont(path)\n"
        "    matplotlib.rcParams['font.sans-serif'] = [fm.FontProperties(fname=path).get_name()]\n"
        "    matplotlib.rcParams['axes.unicode_minus'] = False\n"
        "    print('\u4e2d\u6587\u5b57\u4f53\u5df2\u5c31\u7eea:', matplotlib.rcParams['font.sans-serif'][0])\n"
        "else:\n"
        "    print('\u672a\u80fd\u52a0\u8f7d\u4e2d\u6587\u5b57\u4f53\uff0c\u56fe\u8868\u4e2d\u7684\u4e2d\u6587\u53ef\u80fd\u663e\u793a\u4e3a\u65b9\u5757')"
    )
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": as_source(src)}


def prefer_bundled_font(nb):
    """Put the bundled family first in every font list the notebook sets itself."""
    n = 0
    for c in nb.get("cells", []):
        if c.get("cell_type") != "code":
            continue
        src = "".join(c.get("source", []))
        new = re.sub(r"(rcParams\[[\'\"]font\.sans-serif[\'\"]\]\s*=\s*\[)",
                     lambda m: m.group(1) + repr(FONT_NAME) + ", ", src)
        new = re.sub(r"(for\s+\w+\s+in\s+\[)(?=[\'\"](?:Microsoft YaHei|SimHei|PingFang))",
                     lambda m: m.group(1) + repr(FONT_NAME) + ", ", new)
        if new != src:
            c["source"] = as_source(new)
            n += 1
    return n
SKIP_DIRS = ("__MACOSX", ".ipynb_checkpoints")

# Per-case source fixes, applied to whichever language notebooks contain the text.
PATCHES = {
    "Trajectory_Smoothing_Optimization": [
        ("p_results = p.X",
         "p_results = np.array(p.X.tolist())    # matplotlib cannot consume coptpy's NdArray"),
        ("px_results = p_x.X", "px_results = np.array(p_x.X.tolist())"),
        ("py_results = p_y.X", "py_results = np.array(p_y.X.tolist())"),
    ],
}


def slug(title):
    return re.sub(r"_+", "_", re.sub(r"[^0-9A-Za-z]+", "_", title)).strip("_")


def as_source(text):
    lines = text.split("\n")
    return [l + "\n" for l in lines[:-1]] + [lines[-1]]


def keep(name):
    parts = pathlib.PurePosixPath(name).parts
    return not (name.endswith("/")
                or any(d in parts for d in SKIP_DIRS)
                or any(pt.startswith(".") for pt in parts))


def strip_root(names):
    tops = {pathlib.PurePosixPath(n).parts[0] for n in names}
    if len(tops) == 1 and all(len(pathlib.PurePosixPath(n).parts) > 1 for n in names):
        top = tops.pop()
        return {n: pathlib.PurePosixPath(n).relative_to(top).as_posix() for n in names}
    return {n: n for n in names}


def pick_primary(rel_nbs):
    def score(r):
        stem = pathlib.PurePosixPath(r).stem.lower()
        return (0 if "coding" in stem else 1,
                0 if "original" in stem or "原" in stem else 1,
                0 if stem.endswith(("_en", "-en", "_cn", "-cn")) else 1,
                len(pathlib.PurePosixPath(r).parts), stem)
    return sorted(rel_nbs, key=score)[0]


def imports_of(nb):
    found = set()
    for c in nb.get("cells", []):
        if c.get("cell_type") != "code":
            continue
        for m in re.finditer(r"^\s*(?:from|import)\s+([A-Za-z_][\w.]*)",
                             "".join(c.get("source", [])), re.M):
            top = m.group(1).split(".")[0]
            if top not in STDLIB:
                found.add(PIP_NAME.get(top, top))
    return found


def install_cell(extra):
    # `!pip` rather than `%pip`: ModelWhale images ship an IPython that predates the
    # %pip magic and fails silently. `!pip` works there and on Colab alike.
    pkgs = " ".join(["coptpy"] + sorted(extra))
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": ["# COPT Python API and this case's dependencies\n",
                       f"!pip install -q {pkgs}\n"]}


def inline_attachments(nb):
    """Colab does not resolve `attachment:` image refs, so embed them as data URIs."""
    for c in nb.get("cells", []):
        att = c.get("attachments")
        if not att:
            continue
        text = "".join(c.get("source", []))
        for fname, payload in att.items():
            mime, blob = next(iter(payload.items()))
            b64 = "".join("".join(blob).split()) if isinstance(blob, list) else "".join(blob.split())
            text = text.replace(f"attachment:{fname}", f"data:{mime};base64,{b64}")
        c.pop("attachments")
        c["source"] = as_source(text)
    return nb


def apply_patches(nb, case_slug, strict):
    applied = set()
    for c in nb.get("cells", []):
        if c.get("cell_type") != "code":
            continue
        src = "".join(c.get("source", []))
        for old, new in PATCHES.get(case_slug, []):
            if old in src:
                src = src.replace(old, new)
                applied.add(old)
        c["source"] = as_source(src)
    expected = {old for old, _ in PATCHES.get(case_slug, [])}
    if applied != expected:
        msg = f"{case_slug}: patches did not match: {sorted(expected - applied)}"
        if strict:
            raise RuntimeError(msg)
        print("  WARN " + msg)
    return nb


def data_cell(case_dir, files, repo, branch, lang):
    """Colab loads only the .ipynb, so a case with data files must fetch them.
    On ModelWhale the clone already placed them, and os.path.exists skips the fetch.
    GitHub is unreachable from mainland China, so the Chinese notebooks try the
    Gitee mirror first and fall back to GitHub; the English ones do the reverse."""
    gh = f"https://raw.githubusercontent.com/{repo}/{branch}/notebooks/{lang}/{case_dir}/"
    gt = f"https://gitee.com/{repo}/raw/{branch}/notebooks/{lang}/{case_dir}/"
    bases = [gt, gh] if lang == "zh" else [gh, gt]
    listing = ",\n    ".join(repr(f) for f in sorted(files))
    note = ("# \u672c\u6848\u4f8b\u9700\u8981\u6570\u636e\u6587\u4ef6\uff1b"
            "\u82e5\u5df2\u5728 notebook \u65c1\u8fb9\u5219\u8df3\u8fc7\u4e0b\u8f7d\n"
            if lang == "zh" else
            "# Fetch this case's data files when they are not already next to the notebook.\n")
    src = (note +
           "import os, urllib.parse, urllib.request\n"
           f"BASES = [\n    {bases[0]!r},\n    {bases[1]!r},\n]\n"
           f"FILES = [\n    {listing},\n]\n"
           "for f in FILES:\n"
           "    if os.path.exists(f):\n"
           "        continue\n"
           "    os.makedirs(os.path.dirname(f) or '.', exist_ok=True)\n"
           "    for b in BASES:\n"
           "        try:\n"
           "            urllib.request.urlretrieve(b + urllib.parse.quote(f), f)\n"
           "            break\n"
           "        except Exception:\n"
           "            continue\n"
           "missing = [f for f in FILES if not os.path.exists(f)]\n"
           "print(len(FILES) - len(missing), '/', len(FILES), 'data file(s) ready')\n"
           "if missing:\n"
           "    print('NOT FETCHED:', missing)")
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": as_source(src)}


def colab_ready(nb, case_slug, lang, strict, repo='', branch='main'):
    for c in nb.get("cells", []):
        src = "".join(c.get("source", []))
        if c.get("cell_type") == "code" and "conda create" in src:
            c["source"] = as_source("# No conda here; install this case's requirements with pip\n"
                                    "!pip install -q -r requirements.txt")
            c["outputs"] = []
        elif c.get("cell_type") == "markdown" and "conda" in src.lower():
            c["source"] = as_source("## 安装依赖\n运行下面的单元格，把本案例的依赖装进当前运行环境。"
                                    "不需要切换环境或更换 kernel。" if lang == "zh" else
                                    "## Install Dependencies\nRun the cell below to install this "
                                    "case's requirements into the runtime. No environment switch "
                                    "or kernel change is needed.")
    if case_slug in PATCHES:
        apply_patches(nb, case_slug, strict)
    inline_attachments(nb)
    head = "".join("".join(c.get("source", [])) for c in nb.get("cells", [])[:4])
    if "pip install" not in head:
        nb["cells"][:0] = [
            {"cell_type": "markdown", "metadata": {}, "source": [INSTALL_MD[lang]]},
            install_cell(imports_of(nb)),
        ]
    if lang == "zh" and "matplotlib" in "".join(
            "".join(c.get("source", [])) for c in nb.get("cells", []) if c.get("cell_type") == "code"):
        prefer_bundled_font(nb)
        if not any(FONT_FILE in "".join(c.get("source", [])) for c in nb.get("cells", [])[:5]):
            nb["cells"].insert(2, font_cell(repo, branch))
    md = nb.setdefault("metadata", {})
    md["colab"] = {"provenance": [], "toc_visible": True}
    md["kernelspec"] = dict(KERNEL)
    md.pop("language_info", None)
    return nb


def banner_first(nb, lang):
    """The setup cells land above the case's banner (logo + title image), so the
    notebook opened on a pip cell. Lift the banner back to the top, but only when
    everything above it is a cell this script added."""
    def ours(c):
        src = "".join(c.get("source", []))
        return (src == INSTALL_MD[lang] or src.startswith("# COPT Python API")
                or FONT_FILE in src or "BASES = [" in src)
    for i, c in enumerate(nb["cells"][:8]):
        src = "".join(c.get("source", []))
        if c.get("cell_type") == "markdown" and re.search(r"!\[[^\]]*\]\(|<img", src):
            if i and all(ours(p) for p in nb["cells"][:i]):
                nb["cells"].insert(0, nb["cells"].pop(i))
            return nb
        if not ours(c):
            return nb
    return nb


def load_manifest():
    zh = {}
    for line in (ROOT / "manifest_zh.tsv").read_text().splitlines():
        if line.strip():
            cid, title, path = line.split("\t")
            zh[cid] = {"title": title, "zip": path.rsplit("/", 1)[-1]}
    rows = []
    for line in (ROOT / "manifest.tsv").read_text().splitlines():
        if not line.strip():
            continue
        cid, title, diff, scene, path = line.split("\t")
        rows.append({"id": cid, "slug": slug(title),
                     "title": {"en": title, "zh": zh[cid]["title"]},
                     "difficulty": diff, "scene": scene,
                     "zip": {"en": path.rsplit("/", 1)[-1], "zh": zh[cid]["zip"]},
                     "source": {
                         "en": f"https://www.cardopt.com/copt-document/detail?docType=4&id={cid}",
                         "zh": f"https://www.cardopt.com/copt-document/detail?docType=4&id={cid}"}})
    return rows


def build_one(case, lang, repo, branch):
    zf = zipfile.ZipFile(ZIPS[lang] / case["zip"][lang])
    names = [n for n in zf.namelist() if keep(n)]
    rel = strip_root(names)
    nbs = {n: r for n, r in rel.items() if r.endswith(".ipynb")}
    if not nbs:
        return None
    # Some upstream zips carry files already wrapped by a desktop DLP tool
    # (%TSD-Header). They are unreadable anywhere else and no notebook reads them.
    extras = {n: r for n, r in rel.items() if not r.endswith(".ipynb")
              and not zf.read(n).startswith(b"%TSD-Header")}
    name = case["slug"]

    flat = len(nbs) == 1 and not extras
    dest = (OUT / lang) if flat else (OUT / lang / name)
    dest.mkdir(parents=True, exist_ok=True)
    boot = data_cell(name, extras.values(), repo, branch, lang) if extras else None

    written = {}
    for n, r in nbs.items():
        out = dest / (name + ".ipynb") if flat else dest / r
        out.parent.mkdir(parents=True, exist_ok=True)
        nb = colab_ready(json.loads(zf.read(n).decode("utf-8")), name, lang, lang == "en", repo, branch)
        # Key the dedup on the data cell's own marker: the font cell also mentions
        # raw.githubusercontent, and matching on that silently skipped the data cell.
        if boot and not any("BASES = [" in "".join(c.get("source", []))
                            for c in nb["cells"][:6]):
            nb["cells"].insert(2, json.loads(json.dumps(boot)))
        banner_first(nb, lang)
        out.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
        written[r] = out
    for n, r in extras.items():
        out = dest / r
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(zf.read(n))
    return written[pick_primary(list(written))].relative_to(ROOT).as_posix()


STATUS_ICON = {"ok": "✅", "license": "\U0001f511", "issue": "⚠️"}


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


LEVEL = {"basic": ("Basic", "基础"), "intermediate": ("Intermediate", "进阶"),
         "advanced": ("Advanced", "高级")}
# cardopt's domain tags are inconsistent (and one is truncated), so fold them here
DOMAIN = {
    "Education": ("Education & Research", "教育科研"),
    "Education & Research": ("Education & Research", "教育科研"),
    "EnergyAndElectricity": ("Energy & Power", "能源电力"),
    "Finance": ("Finance", "金融"),
    "Healthcare & Medicine": ("Healthcare", "医疗健康"),
    "Manufacture": ("Manufacturing", "制造"),
    "PersonnelPlan": ("Workforce Planning", "人员规划"),
    "ProductionPlan": ("Production Planning", "生产计划"),
    "SupplyChainManagemen": ("Supply Chain & Logistics", "供应链与物流"),
    "Supply Chain & Logistics": ("Supply Chain & Logistics", "供应链与物流"),
    "Transportation": ("Transportation", "交通运输"),
    "Automatic Control": ("Automatic Control", "自动控制"),
}
MW_PROJECT = "https://www.heywhale.com/mw/project/"
COLAB_BADGE = "https://colab.research.google.com/assets/colab-badge.svg"


def load_modelwhale():
    """modelwhale.tsv: case id, Chinese title, public ModelWhale project id."""
    f = ROOT / "modelwhale.tsv"
    if not f.exists():
        return {}
    rows = [l.split("\t") for l in f.read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
    return {r[0]: r[2] for r in rows}


def note_zh(note):
    """status.tsv notes are English; the size facts translate mechanically."""
    s = note.replace("needs a licensed COPT — ", "")
    s = re.sub(r"(\w+) with (\d+) constraints x (\d+) variables", r"\1，\2 约束 × \3 变量", s)
    s = re.sub(r"(\w+) with (\d+) constraints", r"\1，\2 约束", s)
    s = re.sub(r", past the free (\d+)-(variable|constraint) cap",
               lambda m: f"，超出免费版 {m[1]} {'变量' if m[2] == 'variable' else '约束'}上限", s)
    s = s.replace(", past the free 10000 cap", "，超出免费版 10000 上限")
    return f"需要正式版 COPT 许可（{s}）"


def readme_en(cases, repo, branch):
    base = f"https://colab.research.google.com/github/{repo}/blob/{branch}/"
    status = load_status()
    L = ["# COPT Application Cases", "",
         "**English** · [中文](README.zh-CN.md)", "",
         "All application cases from the [COPT](https://www.cardopt.com/) documentation site, "
         "packaged to open and run in Google Colab with one click. Each notebook starts by "
         "running `pip install coptpy`. The bundled free license is size-limited (MIP 2000 "
         "variables / 2000 constraints, pure LP 10000 each) and needs no license file.", "",
         "✅ runs as is · \U0001f511 needs a licensed COPT (the model exceeds the free limits) "
         "· ⚠️ known glitch", "",
         "| | Case | Level | Domain | Run | Docs |", "|---|---|---|---|---|---|"]
    notes = []
    for c in cases:
        if not c["path"].get("en"):
            continue
        kind, note = status.get(c["title"]["en"], ("ok", ""))
        icon = STATUS_ICON.get(kind, "")
        link = base + c["path"]["en"].replace(" ", "%20")
        dom = DOMAIN.get(c["scene"], (c["scene"],))[0]
        L.append(f'| {icon} | {c["title"]["en"]} | {LEVEL[c["difficulty"]][0]} | {dom} | '
                 f'[![Open In Colab]({COLAB_BADGE})]({link}) | [link]({c["source"]["en"]}) |')
        if note:
            notes.append(f'- **{c["title"]["en"]}**: {note}')
    if notes:
        L += ["", "### Notes", ""] + notes
    L += ["", "## Rebuilding", "",
          "```bash", "python tools/copt_cases.py --out _zips --lang en",
          "python tools/copt_cases.py --out _zips_zh --lang zh",
          f"python tools/build_repo.py --repo {repo} --branch {branch}", "```", ""]
    return "\n".join(L)


def readme_zh(cases, repo, branch):
    status = load_status()
    mw = load_modelwhale()
    L = ["# COPT 应用案例", "",
         "[English](README.md) · **中文**", "",
         "[COPT](https://www.cardopt.com/) 官网的全部应用案例，已发布到 ModelWhale，"
         "点链接即可在线查看、一键运行。每本开头会执行 `pip install coptpy`，"
         "内置的免费许可有规模上限（MIP 2000 变量 / 2000 约束，纯 LP 各 10000），不需要许可文件。", "",
         "✅ 可直接运行 · \U0001f511 模型超出免费许可上限，需正式版许可 · ⚠️ 已知问题", "",
         "| | 案例 | 难度 | 领域 | 运行 | 文档 |", "|---|---|---|---|---|---|"]
    notes = []
    for c in cases:
        if not c["path"].get("zh"):
            continue
        kind, note = status.get(c["title"]["en"], ("ok", ""))
        icon = STATUS_ICON.get(kind, "")
        dom = DOMAIN.get(c["scene"], (c["scene"], c["scene"]))[1]
        pid = mw.get(c["id"])
        run = f"[在线运行]({MW_PROJECT}{pid})" if pid else "—"
        L.append(f'| {icon} | {c["title"]["zh"]} | {LEVEL[c["difficulty"]][1]} | {dom} | '
                 f'{run} | [链接]({c["source"]["zh"]}) |')
        if note:
            notes.append(f'- **{c["title"]["zh"]}**：{note_zh(note)}')
    if notes:
        L += ["", "### 说明", ""] + notes
    L += ["", "notebook 源文件在 `notebooks/zh/`，国内可从 "
          f"[Gitee 镜像](https://gitee.com/{repo}) 获取。", ""]
    return "\n".join(L)


def links_tsv(cases, repo, branch):
    """One flat table for the website: both run links per cardopt case id.
    Generated on every build; modelwhale.tsv stays the hand-kept input."""
    base = f"https://colab.research.google.com/github/{repo}/blob/{branch}/"
    mw = load_modelwhale()
    L = ["case_id\ttitle_en\ttitle_zh\tcolab\tmodelwhale"]
    for c in cases:
        colab = base + urllib.parse.quote(c["path"]["en"]) if c["path"].get("en") else ""
        pid = mw.get(c["id"])
        L.append("\t".join([c["id"], c["title"]["en"], c["title"]["zh"], colab,
                            MW_PROJECT + pid if pid else ""]))
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="tztgracious/copt-colab-cases")
    ap.add_argument("--branch", default="main")
    a = ap.parse_args()

    try:
        shutil.rmtree(OUT)
    except OSError:
        pass
    cases = load_manifest()
    for c in cases:
        c["path"] = {}
        for lang in ("en", "zh"):
            try:
                c["path"][lang] = build_one(c, lang, a.repo, a.branch)
            except Exception as e:                                    # noqa: BLE001
                c["path"][lang] = None
                print(f'FAIL [{lang}] {c["title"]["en"]}: {type(e).__name__}: {e}')
    (ROOT / "README.md").write_text(readme_en(cases, a.repo, a.branch), encoding="utf-8")
    (ROOT / "README.zh-CN.md").write_text(readme_zh(cases, a.repo, a.branch), encoding="utf-8")
    (ROOT / "links.tsv").write_text(links_tsv(cases, a.repo, a.branch), encoding="utf-8")
    for lang in ("en", "zh"):
        print(f'{sum(1 for c in cases if c["path"].get(lang))}/{len(cases)} {lang} notebooks')


if __name__ == "__main__":
    main()
