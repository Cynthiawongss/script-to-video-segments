"""Validate declared segment timing, dialogue coverage, and continuity state."""
import argparse
import json
import math
from pathlib import Path


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: expected nonempty text")
    return value


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label}: expected finite number")
    return value


def state(value, keys, label):
    if not isinstance(value, dict) or not value or set(value) != keys:
        raise ValueError(f"{label}: expected the same nonempty state keys throughout")
    for k, v in value.items():
        text(k, label)
        text(v, f"{label}.{k}")


def validate(plan):
    errors, warnings = [], []
    try:
        if not isinstance(plan, dict) or type(plan.get("schema_version")) is not int or plan["schema_version"] != 1:
            raise ValueError("expected an object with schema_version=1")
        text(plan["title"], "title")
        p = plan["planning"]
        target = number(p["target_seconds"], "target_seconds")
        cap = number(p["max_segment_seconds"], "max_segment_seconds")
        rate = number(p["max_units_per_second"], "max_units_per_second")
        if min(target, cap, rate) <= 0:
            raise ValueError("duration and speech thresholds must be positive")
        text(p["limit_basis"], "limit_basis")
        if p["speech_unit"] not in ("whitespace_words", "cjk_characters"):
            raise ValueError("unsupported speech_unit")
        locks = plan["locks"]
        if not isinstance(locks, dict) or not locks:
            raise ValueError("locks must be a nonempty object")
        for k, v in locks.items():
            text(k, "lock id")
            text(v, f"lock {k}")
        source = plan["source_dialogue"]
        if not isinstance(source, list):
            raise ValueError("source_dialogue must be a list (may be empty for a silent scene)")
        by_id = {}
        for line in source:
            if not isinstance(line, dict):
                raise ValueError("source dialogue entries must be objects")
            lid = text(line["id"], "dialogue id")
            if lid in by_id:
                errors.append(f"duplicate source dialogue id: {lid}")
            text(line["text"], f"{lid}.text")
            if line["speaker"] not in locks:
                errors.append(f"{lid}: speaker has no lock")
            by_id[lid] = line
        omissions = plan["omissions"]
        if not isinstance(omissions, list):
            raise ValueError("omissions must be a list")
        omitted = set()
        for item in omissions:
            lid = item["id"]
            text(item["authorization"], "omission authorization")
            if lid not in by_id or lid in omitted:
                errors.append(f"invalid or repeated omission: {lid}")
            omitted.add(lid)
        segments = plan["segments"]
        if not isinstance(segments, list) or not segments:
            raise ValueError("segments must be a nonempty list")
        first_state = segments[0]["opening_state"]
        if not isinstance(first_state, dict) or not first_state:
            raise ValueError("opening_state must be a nonempty object")
        keys = set(first_state)
        seen_segments, seen_lines = set(), []
        previous = None
        total = 0
        for segment in segments:
            sid = text(segment["id"], "segment id")
            if sid in seen_segments:
                errors.append(f"duplicate segment id: {sid}")
            seen_segments.add(sid)
            duration = number(segment["duration"], f"{sid}.duration")
            if duration <= 0 or duration > cap:
                errors.append(f"{sid}: duration must be positive and at most {cap}")
            total += duration
            ids = segment["lock_ids"]
            if not isinstance(ids, list) or any(not isinstance(i, str) for i in ids):
                raise ValueError(f"{sid}: lock_ids must be a list of strings")
            if set(ids) != set(locks) or len(ids) != len(set(ids)):
                errors.append(f"{sid}: include each applicable root lock exactly once")
            state(segment["opening_state"], keys, f"{sid}.opening_state")
            state(segment["closing_state"], keys, f"{sid}.closing_state")
            if not isinstance(segment["bridge"], str):
                raise ValueError(f"{sid}: bridge must be text, empty for continuous action")
            if previous is not None and previous != segment["opening_state"]:
                if not segment["bridge"].strip():
                    errors.append(f"{sid}: boundary state changed without a bridge")
                else:
                    warnings.append(f"{sid}: inspect the intentional bridge: {segment['bridge']}")
            beats = segment["beats"]
            if not isinstance(beats, list) or not beats:
                raise ValueError(f"{sid}: beats must be a nonempty list")
            end = 0
            previous_beat = segment["opening_state"]
            for index, beat in enumerate(beats):
                label = f"{sid}.beat{index+1}"
                start = number(beat["start"], f"{label}.start")
                stop = number(beat["end"], f"{label}.end")
                if abs(start-end) > 1e-6 or stop <= start or stop > duration + 1e-6:
                    errors.append(f"{label}: gap, overlap, or invalid interval")
                end = stop
                for key in ("camera", "action", "audio"):
                    text(beat[key], f"{label}.{key}")
                state(beat["state_in"], keys, f"{label}.state_in")
                state(beat["state_out"], keys, f"{label}.state_out")
                if beat["state_in"] != previous_beat:
                    errors.append(f"{label}: incoming state does not match previous state")
                previous_beat = beat["state_out"]
                lines = beat["dialogue"]
                if not isinstance(lines, list):
                    raise ValueError(f"{label}: dialogue must be a list")
                units = 0
                for line in lines:
                    lid = line["id"]
                    seen_lines.append(lid)
                    if lid not in by_id or line != by_id[lid]:
                        errors.append(f"{label}: unknown or changed dialogue {lid}")
                    speech = text(line["text"], f"{label}.dialogue.text")
                    units += len(speech.split()) if p["speech_unit"] == "whitespace_words" else len(''.join(speech.split()))
                if stop > start and units / (stop-start) > rate:
                    warnings.append(f"{label}: estimated speech load {units/(stop-start):.2f} units/s exceeds {rate}; read aloud")
            if abs(end-duration) > 1e-6:
                errors.append(f"{sid}: timeline does not cover segment duration")
            if previous_beat != segment["closing_state"]:
                errors.append(f"{sid}: last beat does not reach closing state")
            previous = segment["closing_state"]
        expected_lines = [line["id"] for line in source if line["id"] not in omitted]
        if seen_lines != expected_lines:
            errors.append(f"dialogue coverage/order mismatch: expected {expected_lines}, got {seen_lines}")
        if abs(total-target) > 1e-6:
            errors.append(f"total duration {total} does not match target {target}")
    except (ValueError, TypeError, KeyError, IndexError, AttributeError) as exc:
        errors.append(f"invalid plan: {exc}")
    return {"valid": not errors, "errors": errors, "warnings": warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.plan.read_text(encoding="utf-8")))
    except (OSError, ValueError) as exc:
        result = {"valid": False, "errors": [str(exc)], "warnings": []}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
