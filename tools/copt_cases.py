"""
Fetch the COPT 'Application Cases' notebooks from cardopt.com and make them Colab-ready.

API discovered on https://www.cardopt.com/copt-document/detail?docType=4&id=22 :
  GET /prod-api/website/solver/doc/listByParent?parentId=22&language=en
      -> data[].infoEn.formJson (a JSON *string*) -> fileUrl  (the case .zip)
                                 infoEn.title     (the case name)

Usage (local):
    python copt_cases.py --out ./cases                 # all 30 cases
    python copt_cases.py --out ./cases --only "Assignment Problem"
    python copt_cases.py --list
"""

import argparse
import io
import json
import os
import pathlib
import re
import urllib.request
import zipfile

API = "https://www.cardopt.com/prod-api/website/solver/doc/listByParent"
PARENT_ID = 22                      # "Application Cases" / 应用案例
UA = {"User-Agent": "Mozilla/5.0"}

INSTALL_MD = (
    "> **Run in Google Colab.** The next cell installs `coptpy`. The bundled free "
    "license allows up to 2000 variables and 2000 constraints, which covers every "
    "case in this collection. Then choose *Runtime > Run all*.\n"
)
INSTALL_CODE = ["# COPT Python API (free size-limited license, no license file needed)\n",
                "%pip install -q coptpy matplotlib\n"]


def _get(url, timeout=120):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def slug(title):
    return re.sub(r"_+", "_", re.sub(r"[^0-9A-Za-z一-鿿]+", "_", title)).strip("_")


def list_cases(parent_id=PARENT_ID, lang="en"):
    """Return [{'id', 'title', 'url'}] for every case that ships a .zip."""
    payload = json.loads(_get(f"{API}?parentId={parent_id}&language={lang}"))
    cases = []
    for d in payload["data"]:
        info = d.get("infoEn" if lang == "en" else "infoZh") or d.get("infoEn")
        if not info:
            continue
        try:
            form = json.loads(info.get("formJson") or "{}")
        except json.JSONDecodeError:
            form = {}
        url = form.get("fileUrl")
        if not url:
            continue
        cases.append({"id": d["id"],
                      "title": info.get("title") or form.get("title") or str(d["id"]),
                      "url": url})
    return cases


def make_colab_ready(nb):
    """Prepend the pip-install cell unless the notebook already has one."""
    head = "".join("".join(c.get("source", [])) for c in nb.get("cells", [])[:4])
    if "pip install" not in head:
        nb["cells"][:0] = [
            {"cell_type": "markdown", "metadata": {}, "source": [INSTALL_MD]},
            {"cell_type": "code", "execution_count": None, "metadata": {},
             "outputs": [], "source": INSTALL_CODE},
        ]
    nb.setdefault("metadata", {})["colab"] = {"provenance": [], "toc_visible": True}
    return nb


def fetch_case(case, out_dir):
    """Download one case zip, patch its notebook(s), write everything under out_dir."""
    zf = zipfile.ZipFile(io.BytesIO(_get(case["url"])))
    names = [n for n in zf.namelist()
             if not n.endswith("/") and "__MACOSX" not in n and not os.path.basename(n).startswith(".")]
    notebooks = [n for n in names if n.endswith(".ipynb")]
    extras = [n for n in names if n not in notebooks]

    name = slug(case["title"])
    dest = pathlib.Path(out_dir)
    if extras:                       # case ships data files -> keep them next to the notebook
        dest = dest / name
    dest.mkdir(parents=True, exist_ok=True)

    written = []
    for n in notebooks:
        nb = make_colab_ready(json.loads(zf.read(n).decode("utf-8")))
        out = dest / (f"{name}.ipynb" if len(notebooks) == 1 else pathlib.Path(n).name)
        out.write_text(json.dumps(nb, ensure_ascii=False), encoding="utf-8")
        written.append(out)
    for n in extras:
        out = dest / pathlib.Path(n).name
        out.write_bytes(zf.read(n))
        written.append(out)
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="./cases")
    ap.add_argument("--lang", default="en", choices=["en", "zh"])
    ap.add_argument("--only", nargs="*", default=None, help="case titles to fetch; default is all")
    ap.add_argument("--list", action="store_true", help="just print the case list")
    a = ap.parse_args()

    cases = list_cases(lang=a.lang)
    if a.list:
        for c in cases:
            print(f'{c["id"]:>4}  {c["title"]}')
        return
    if a.only:
        wanted = {t.lower() for t in a.only}
        cases = [c for c in cases if c["title"].lower() in wanted]

    for c in cases:
        try:
            files = fetch_case(c, a.out)
            print(f'ok   {c["title"]}: ' + ", ".join(str(f) for f in files))
        except Exception as e:                                   # noqa: BLE001
            print(f'FAIL {c["title"]}: {type(e).__name__}: {e}')


if __name__ == "__main__":
    main()
