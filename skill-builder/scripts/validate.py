#!/usr/bin/env python3
"""Check a skill folder against the Agent Skills format and common mistakes.

Usage:  python3 validate.py path/to/your-skill

Prints ERROR lines (the skill will not load or will break) and TIP lines
(it loads, but it will work worse). Exits 1 if there are errors.
Needs only Python 3, no extra packages.
"""
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Result:
    errors: list = field(default_factory=list)
    tips: list = field(default_factory=list)


def read_frontmatter(text):
    """Return (fields, body) or (None, text) when there is no frontmatter block."""
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.S)
    if not m:
        return None, text
    fields = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if km:
            value = km.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            fields[km.group(1)] = value
    return fields, text[m.end():]


def check(folder):
    folder = Path(folder)
    result = Result()
    skill_md = folder / "SKILL.md"
    if not skill_md.is_file():
        result.errors.append(f"No SKILL.md in {folder}. Every skill needs one, spelled exactly SKILL.md.")
        return result
    text = skill_md.read_text(encoding="utf-8")
    fields, body = read_frontmatter(text)
    if fields is None:
        result.errors.append("SKILL.md must start with a frontmatter block between two --- lines.")
        return result
    check_fields(fields, result)
    check_name(fields.get("name", ""), folder, result)
    check_description(fields.get("description", ""), result)
    check_placeholders(text, result)
    check_files(folder, body, result)
    lines = text.count("\n") + 1
    if lines > 500:
        result.tips.append(f"SKILL.md is {lines} lines. Keep it under 500: move detail into files in references/ and point to them.")
    return result


def check_files(folder, body, result):
    """Every file the skill points to (a Markdown link or a `scripts/...` path) has to exist."""
    links = re.findall(r"\]\(([^)#\s]+)", body)
    paths = re.findall(r"`((?:scripts|references|assets)/[^`\s]+)`", body)
    for ref in dict.fromkeys(links + paths):
        if re.match(r"^[a-z]+:", ref):
            continue
        if not (folder / ref).exists():
            result.errors.append(f"SKILL.md points to {ref}, but that file is not in the skill folder.")

def check_description(desc, result):
    if not desc:
        result.errors.append("The frontmatter has no description. It is how the AI decides when to use the skill, so it is required.")
        return
    if desc in (">", "|", ">-", "|-"):
        result.tips.append("The description is spread over several lines. Some tools only read one line: put it on a single line.")
        return
    if len(desc) > 1024:
        result.errors.append(f"description is {len(desc)} characters; the maximum is 1024.")
    elif len(desc) > 200:
        result.tips.append(f"description is {len(desc)} characters. The format allows 1024, but Claude's help pages ask for 200 or fewer: "
                           "shorten it, or at least make the first 200 characters say what it does and when to use it.")
    if "<" in desc or ">" in desc:
        result.errors.append("description may not contain < or >.")
    if not re.search(r"\bwhen\b", desc, re.I):
        result.tips.append("Say when to use the skill in the description, e.g. 'Use when someone asks for ...'. That sentence is what makes the AI pick it.")
    if re.search(r"\b(I|I'm|I'll|my)\b|\byou can\b", desc):
        result.tips.append("Write the description in the third person ('Builds ...', 'Use when ...'), not with I or you.")


def check_placeholders(text, result):
    prose = re.sub(r"`[^`\n]*`", "", text)  # a marker in `code` is a mention, not a gap
    for marker in ("[FILL IN", "[TODO"):
        count = prose.count(marker)
        if count:
            result.errors.append(f"{count} unfilled {marker}...] placeholder(s) left in SKILL.md.")
    if "<!--" in prose:
        result.tips.append("SKILL.md still has <!-- guidance comments --> from the template. Delete them once the section is filled in.")

OFFICIAL_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def check_fields(fields, result):
    extra = sorted(set(fields) - OFFICIAL_FIELDS)
    if extra:
        result.tips.append(f"Frontmatter field(s) {', '.join(extra)} are not in the Agent Skills format. Claude Code accepts them, "
                           "but an upload to claude.ai fails on them. Remove them if the skill will be uploaded.")


def check_name(name, folder, result):
    if not name:
        result.errors.append("The frontmatter has no name. Add a line like: name: meta-campaign")
        return
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        result.errors.append(f"name '{name}' may only use lowercase letters, numbers and single hyphens (meta-campaign, not Meta Campaign).")
    if len(name) > 64:
        result.errors.append(f"name is {len(name)} characters; the maximum is 64.")
    for word in ("claude", "anthropic"):
        if word in name:
            result.errors.append(f"name may not contain the reserved word '{word}'.")
    if folder.name != name:
        result.errors.append(f"The folder is called '{folder.name}' but the name is '{name}'. They have to be the same.")


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[2])
        return 2
    result = check(argv[1])
    for e in result.errors:
        print(f"ERROR  {e}")
    for t in result.tips:
        print(f"TIP    {t}")
    if result.errors:
        print(f"\n{len(result.errors)} error(s). Fix these before you use or share the skill.")
        return 1
    print("\nNo errors." + (f" {len(result.tips)} tip(s) above." if result.tips else " The skill is ready to test."))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
