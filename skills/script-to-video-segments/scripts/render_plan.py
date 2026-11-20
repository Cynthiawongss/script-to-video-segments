"""Render validated JSON to integrated, copyable segment prompts."""
import argparse
import json
from pathlib import Path
from check_plan import validate


def render(plan):
    result = validate(plan)
    if not result["valid"]:
        raise ValueError("; ".join(result["errors"]))
    lines = [f"# {plan['title']}", "", "Production plan only. No footage has been generated or verified.", "",
             f"Target: {plan['planning']['target_seconds']} s. Planning limit: {plan['planning']['max_segment_seconds']} s per segment.",
             f"Limit basis: {plan['planning']['limit_basis']}", ""]
    for warning in result["warnings"]:
        lines.extend([f"Review flag: {warning}", ""])
    if plan["omissions"]:
        lines.extend(["## Recorded omissions", ""])
        lines.extend(f"- {o['id']}: {o['authorization']}" for o in plan["omissions"])
        lines.append("")
    for seg in plan["segments"]:
        lines.extend([f"## {seg['id']} · {seg['duration']} seconds", "", "### Copyable prompt", ""])
        lines.extend(f"- {lid}: {plan['locks'][lid]}" for lid in seg["lock_ids"])
        lines.extend(["", "Opening state: " + "; ".join(f"{k}={v}" for k, v in seg["opening_state"].items()), ""])
        if seg["bridge"]:
            lines.extend(["Bridge: " + seg["bridge"], ""])
        for beat in seg["beats"]:
            lines.extend([f"**{beat['start']:g}–{beat['end']:g} s** — {beat['camera']} {beat['action']}", ""])
            lines.extend(f"{d['speaker']} ({d['id']}): “{d['text']}”" for d in beat["dialogue"])
            lines.extend(["Sound: " + beat["audio"], ""])
        lines.extend(["Closing state: " + "; ".join(f"{k}={v}" for k, v in seg["closing_state"].items()), "",
                      "Edit: match the accepted closing take to the next opening state; inspect props, screen direction, and audio at the cut.", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        content = render(json.loads(args.plan.read_text(encoding="utf-8")))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Cannot render: {exc}\n")
    print(args.output)


if __name__ == "__main__":
    main()
