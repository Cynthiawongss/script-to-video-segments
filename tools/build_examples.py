"""Synchronize offline example pages and generated prompts from JSON fixtures."""
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def embed(folder, filename, page="index.html"):
    value = json.loads((folder / filename).read_text(encoding="utf-8"))
    payload = json.dumps(value, ensure_ascii=False).replace("<", "\\u003c")
    path = folder / page
    content = path.read_text(encoding="utf-8")
    content, count = re.subn(r'(<script id="fixture" type="application/json">).*?(</script>)',
                             lambda m: m[1] + payload + m[2], content, flags=re.S)
    if count != 1:
        raise ValueError(f"Expected one fixture block in {path}")
    path.write_text(content, encoding="utf-8")


def main():
    video = ROOT / "skills/script-to-video-segments/examples/the-last-label"
    sys.path.insert(0, str(ROOT / "skills/script-to-video-segments/scripts"))
    from render_plan import render
    plan = json.loads((video / "plan.json").read_text(encoding="utf-8"))
    (video / "segments.md").write_text(render(plan), encoding="utf-8")
    for page in ("index.html", "index.zh-CN.html"):
        embed(video, "plan.json", page)
    print("Updated both offline pages and segment prompts.")


if __name__ == "__main__":
    main()
