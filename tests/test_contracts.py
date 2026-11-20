"""Behavioral examples and intentional corruptions of the data contracts."""
import copy
import csv
import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


video = module("video_check", "skills/script-to-video-segments/scripts/check_plan.py")
sys.path.insert(0, str(ROOT / "skills/script-to-video-segments/scripts"))
from render_plan import render
VID = ROOT / "skills/script-to-video-segments/examples/the-last-label"


class VideoCases(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((VID / "plan.json").read_text(encoding="utf-8"))

    def test_valid_plan(self):
        self.assertEqual(video.validate(self.data), {"valid": True, "errors": [], "warnings": []})

    def test_rejects_lost_dialogue(self):
        self.data["segments"][0]["beats"][0]["dialogue"] = []
        self.assertFalse(video.validate(self.data)["valid"])

    def test_rejects_repeated_or_changed_dialogue(self):
        for change in ("repeat", "rewrite"):
            with self.subTest(change=change):
                data = copy.deepcopy(self.data)
                lines = data["segments"][0]["beats"][0]["dialogue"]
                if change == "repeat":
                    lines.append(copy.deepcopy(lines[0]))
                else:
                    lines[0]["text"] = "A new line that was never approved."
                self.assertFalse(video.validate(data)["valid"])

    def test_rejects_gap_and_overlap(self):
        for start in (3, 5):
            data = copy.deepcopy(self.data)
            data["segments"][0]["beats"][1]["start"] = start
            self.assertFalse(video.validate(data)["valid"])

    def test_rejects_boundary_drift(self):
        self.data["segments"][1]["opening_state"]["label"] = "missing"
        self.assertFalse(video.validate(self.data)["valid"])

    def test_rejects_internal_state_drift(self):
        self.data["segments"][1]["beats"][1]["state_in"]["screen"] = "room 99"
        self.assertFalse(video.validate(self.data)["valid"])

    def test_accepts_explicit_scene_change_with_review_flag(self):
        seg = self.data["segments"][2]
        seg["bridge"] = "Labelled next-day cut, same room."
        for state in [seg["opening_state"], seg["closing_state"]] + [b[k] for b in seg["beats"] for k in ("state_in", "state_out")]:
            state["light"] = "next morning from left"
        result = video.validate(self.data)
        self.assertTrue(result["valid"], result)
        self.assertTrue(result["warnings"])

    def test_rejects_duration_cap_and_total_overrun(self):
        self.data["planning"]["max_segment_seconds"] = 8
        self.assertFalse(video.validate(self.data)["valid"])
        self.data["planning"]["max_segment_seconds"] = 10
        self.data["planning"]["target_seconds"] = 25
        self.assertFalse(video.validate(self.data)["valid"])

    def test_speech_load_is_flag_not_fake_validation(self):
        self.data["planning"]["max_units_per_second"] = 1
        result = video.validate(self.data)
        self.assertTrue(result["valid"])
        self.assertTrue(result["warnings"])

    def test_silent_scene_is_valid(self):
        self.data["source_dialogue"] = []
        for seg in self.data["segments"]:
            for beat in seg["beats"]:
                beat["dialogue"] = []
        self.assertTrue(video.validate(self.data)["valid"])

    def test_bad_structure_returns_errors_instead_of_crashing(self):
        for data in ([], {}, {"schema_version": 1}, None):
            self.assertFalse(video.validate(data)["valid"])

    def test_renderer_refuses_invalid_plan(self):
        self.data["segments"][0]["beats"] = []
        with self.assertRaises(ValueError):
            render(self.data)

class PackageCases(unittest.TestCase):
    def test_offline_pages_embed_current_fixture(self):
        for folder, filename in ((VID, "plan.json"),):
            for page in ("index.html", "index.zh-CN.html"):
                html = (folder / page).read_text(encoding="utf-8")
                payload = re.search(r'<script id="fixture" type="application/json">(.*?)</script>', html, re.S)[1]
                self.assertEqual(json.loads(payload), json.loads((folder / filename).read_text(encoding="utf-8")))

    def test_generated_prompts_are_current(self):
        plan = json.loads((VID / "plan.json").read_text(encoding="utf-8"))
        self.assertEqual((VID / "segments.md").read_text(encoding="utf-8"), render(plan))

if __name__ == "__main__":
    unittest.main()
