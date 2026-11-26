"""Behaviour tests for skill-builder/scripts/validate.py (run: python3 -m unittest discover tests)."""
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skill-builder" / "scripts" / "validate.py"
sys.path.insert(0, str(SCRIPT.parent))

import validate  # noqa: E402

GOOD = """\
---
name: meta-campaign
description: Builds a new Meta campaign the way our senior does it. Use when someone asks to set up, plan or structure a Meta or Facebook ads campaign.
---

# Meta campaign

Steps go here.
"""


def make_skill(tmp, folder="meta-campaign", text=GOOD, extra=None):
    d = Path(tmp) / folder
    d.mkdir()
    if text is not None:
        (d / "SKILL.md").write_text(textwrap.dedent(text), encoding="utf-8")
    for rel, body in (extra or {}).items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    return d


class Basics(unittest.TestCase):
    def test_a_good_skill_has_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = validate.check(make_skill(tmp))
            self.assertEqual(result.errors, [])

    def test_a_folder_without_skill_md_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = validate.check(make_skill(tmp, text=None))
            self.assertTrue(any("SKILL.md" in e for e in result.errors))

    def test_cli_exits_1_on_errors_and_0_when_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = subprocess.run([sys.executable, str(SCRIPT), str(make_skill(tmp))], capture_output=True, text=True)
            bad = subprocess.run([sys.executable, str(SCRIPT), str(make_skill(tmp, folder="empty", text=None))], capture_output=True, text=True)
        self.assertEqual(good.returncode, 0, good.stdout)
        self.assertEqual(bad.returncode, 1, bad.stdout)


def with_name(name):
    return GOOD.replace("name: meta-campaign", f"name: {name}")


class Name(unittest.TestCase):
    def errors_for(self, name, folder=None):
        with tempfile.TemporaryDirectory() as tmp:
            return validate.check(make_skill(tmp, folder=folder or name.strip() or "x", text=with_name(name))).errors

    def test_missing_name_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = GOOD.replace("name: meta-campaign\n", "")
            errors = validate.check(make_skill(tmp, text=text)).errors
        self.assertTrue(any("name" in e for e in errors), errors)

    def test_capitals_and_spaces_are_errors(self):
        self.assertTrue(self.errors_for("Meta Campaign", folder="meta-campaign"))

    def test_name_over_64_characters_is_an_error(self):
        self.assertTrue(self.errors_for("a" * 65))

    def test_64_characters_is_fine(self):
        self.assertEqual(self.errors_for("a" * 64), [])

    def test_hyphen_at_start_or_double_hyphen_is_an_error(self):
        self.assertTrue(self.errors_for("-meta"))
        self.assertTrue(self.errors_for("meta--campaign"))

    def test_name_must_match_the_folder(self):
        errors = self.errors_for("meta-campaign", folder="meta-ads")
        self.assertTrue(any("folder" in e for e in errors), errors)

    def test_reserved_words_are_errors(self):
        self.assertTrue(self.errors_for("claude-helper"))
        self.assertTrue(self.errors_for("anthropic-tools"))


GOOD_DESC = "Builds a new Meta campaign the way our senior does it. Use when someone asks to set up, plan or structure a Meta or Facebook ads campaign."


def with_description(desc):
    return GOOD.replace(GOOD_DESC, desc)


class Description(unittest.TestCase):
    def run_check(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            return validate.check(make_skill(tmp, text=text))

    def test_missing_description_is_an_error(self):
        result = self.run_check(GOOD.replace(f"description: {GOOD_DESC}\n", ""))
        self.assertTrue(any("description" in e for e in result.errors), result.errors)

    def test_over_1024_characters_is_an_error(self):
        result = self.run_check(with_description("Use when " + "x" * 1020))
        self.assertTrue(any("1024" in e for e in result.errors), result.errors)

    def test_angle_brackets_are_an_error(self):
        result = self.run_check(with_description("Builds <campaigns>. Use when asked."))
        self.assertTrue(result.errors)

    def test_no_when_clause_gives_a_tip(self):
        result = self.run_check(with_description("Builds a new Meta campaign the way our senior does it."))
        self.assertEqual(result.errors, [])
        self.assertTrue(any("when" in t.lower() for t in result.tips), result.tips)

    def test_first_person_gives_a_tip(self):
        result = self.run_check(with_description("I build Meta campaigns. Use when asked for a Meta campaign."))
        self.assertTrue(any("third person" in t for t in result.tips), result.tips)

    def test_over_200_characters_gives_a_tip(self):
        result = self.run_check(with_description("Builds things. Use when asked. " + "x" * 200))
        self.assertEqual(result.errors, [])
        self.assertTrue(any("200" in t for t in result.tips), result.tips)

    def test_a_field_claude_ai_rejects_gives_a_tip(self):
        result = self.run_check(GOOD.replace("---\n\n#", "argument-hint: campaign name\n---\n\n#"))
        self.assertEqual(result.errors, [])
        self.assertTrue(any("argument-hint" in t for t in result.tips), result.tips)

    def test_the_six_official_fields_give_no_tip(self):
        extra = "license: MIT\ncompatibility: Needs Python 3\nmetadata:\n  author: zeb\nallowed-tools: Read\n"
        result = self.run_check(GOOD.replace("---\n\n#", extra + "---\n\n#"))
        self.assertEqual(result.tips, [])

    def test_a_good_description_gives_no_tips(self):
        self.assertEqual(self.run_check(GOOD).tips, [])


class Placeholders(unittest.TestCase):
    def test_unfilled_template_text_is_an_error(self):
        text = GOOD.replace("Steps go here.", "1. [FILL IN: the first step]")
        with tempfile.TemporaryDirectory() as tmp:
            errors = validate.check(make_skill(tmp, text=text)).errors
        self.assertTrue(any("FILL IN" in e for e in errors), errors)

    def test_a_placeholder_mentioned_in_code_formatting_is_not_a_gap(self):
        text = GOOD.replace("Steps go here.", "Leave a visible `[FILL IN: ...]` gap when unsure.")
        with tempfile.TemporaryDirectory() as tmp:
            errors = validate.check(make_skill(tmp, text=text)).errors
        self.assertEqual(errors, [])


    def test_leftover_template_guidance_comments_give_a_tip(self):
        text = GOOD.replace("Steps go here.", "<!-- One step per action. -->\n1. Do the thing.")
        with tempfile.TemporaryDirectory() as tmp:
            result = validate.check(make_skill(tmp, text=text))
        self.assertEqual(result.errors, [])
        self.assertTrue(any("<!--" in t for t in result.tips), result.tips)


class Files(unittest.TestCase):
    def test_a_link_to_a_missing_file_is_an_error(self):
        text = GOOD.replace("Steps go here.", "Read [the checklist](references/checklist.md) first. Then run `scripts/build.py`.")
        with tempfile.TemporaryDirectory() as tmp:
            errors = validate.check(make_skill(tmp, text=text, extra={"references/checklist.md": "x"})).errors
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("scripts/build.py", errors[0])

    def test_links_to_existing_files_and_websites_are_fine(self):
        text = GOOD.replace("Steps go here.", "See [docs](https://example.com/a.md) and [checklist](references/checklist.md).")
        with tempfile.TemporaryDirectory() as tmp:
            errors = validate.check(make_skill(tmp, text=text, extra={"references/checklist.md": "x"})).errors
        self.assertEqual(errors, [])

    def test_a_very_long_skill_md_gives_a_tip(self):
        text = GOOD + "line\n" * 520
        with tempfile.TemporaryDirectory() as tmp:
            tips = validate.check(make_skill(tmp, text=text)).tips
        self.assertTrue(any("500" in t for t in tips), tips)


class Repo(unittest.TestCase):
    def test_the_template_people_download_is_the_one_the_skill_uses(self):
        public = (ROOT / "template" / "SKILL.md").read_text(encoding="utf-8")
        bundled = (ROOT / "skill-builder" / "assets" / "skill-template.md").read_text(encoding="utf-8")
        self.assertEqual(public, bundled, "Copy template/SKILL.md to skill-builder/assets/skill-template.md")

    def test_the_unfilled_template_is_caught(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = (ROOT / "template" / "SKILL.md").read_text(encoding="utf-8")
            errors = validate.check(make_skill(tmp, folder="anything", text=text)).errors
        self.assertTrue(any("FILL IN" in e for e in errors), errors)

    def test_the_shipped_skills_pass(self):
        for folder in [ROOT / "skill-builder", *sorted((ROOT / "examples").glob("*/"))]:
            with self.subTest(folder.name):
                self.assertEqual(validate.check(folder).errors, [])


if __name__ == "__main__":
    unittest.main()
