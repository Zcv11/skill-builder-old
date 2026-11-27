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

OFFICIAL_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
BLOCK_MARKERS = (">", "|", ">-", "|-", ">+", "|+")


@dataclass
class Result:
    errors: list = field(default_factory=list)
    tips: list = field(default_factory=list)


# ---------------------------------------------------------------- reading the file

def read_frontmatter(text, result):
    """Return (fields, body). fields is None when there is no frontmatter block.

    A small reader for the simple YAML a skill uses: one key per line, plain or quoted
    values, > and | blocks, and nested maps (skipped). It reports the hand-written
    mistakes that make a real YAML parser fail or cut a value short.
    """
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.S)
    if not m:
        return None, text
    lines = m.group(1).splitlines()
    fields = {}
    i = 0
    while i < len(lines):
        km = re.match(r"^([A-Za-z0-9_-]+):(.*)$", lines[i])
        i += 1
        if not km:
            continue
        key, value = km.group(1), km.group(2).strip()
        if value in BLOCK_MARKERS:
            block = []
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            joiner = " " if value.startswith(">") else "\n"
            fields[key] = joiner.join(part for part in block if part)
        elif value[:1] in ("'", '"'):
            quote = value[0]
            while not _closes(value, quote) and i < len(lines) and lines[i].startswith((" ", "\t")):
                value += " " + lines[i].strip()
                i += 1
            end = _closing_index(value, quote)
            if end is None:
                result.errors.append(f"{key}: the opening {quote} is never closed.")
                fields[key] = value[1:]
            else:
                rest = value[end + 1:].strip()
                if rest and not rest.startswith("#"):
                    result.errors.append(f"{key}: there is text after the closing {quote}. Put the whole value inside the quotes.")
                fields[key] = value[1:end]
        else:
            _plain_value_problems(key, value, result)
            fields[key] = re.split(r"\s#", value, maxsplit=1)[0].strip()
    return fields, text[m.end():]


def _closing_index(value, quote):
    j = 1
    while j < len(value):
        if value[j] == "\\" and quote == '"':
            j += 2
            continue
        if value[j] == quote:
            if quote == "'" and value[j + 1:j + 2] == "'":  # '' is an escaped quote
                j += 2
                continue
            return j
        j += 1
    return None


def _closes(value, quote):
    return _closing_index(value, quote) is not None


def _plain_value_problems(key, value, result):
    if not value:
        return
    if ": " in value:
        result.errors.append(f"{key}: a colon followed by a space breaks the frontmatter. Put the whole value in double quotes.")
    if " #" in value:
        result.errors.append(f"{key}: ' #' starts a comment, so everything after it is lost. Put the whole value in double quotes.")
    if value[0] in "[{&*!|>%@`":
        result.errors.append(f"{key}: a value can't start with {value[0]}. Put the whole value in double quotes.")


def strip_fences(text):
    """Text inside ``` blocks is an example or a template, not instructions about files."""
    return re.sub(r"^[ \t]*```.*?^[ \t]*```[^\n]*$", "", text, flags=re.S | re.M)


# ---------------------------------------------------------------- the checks

def check(folder):
    folder = Path(folder)
    if folder.name == "SKILL.md" and folder.is_file():
        folder = folder.parent
    folder = folder.resolve()
    result = Result()
    skill_md = folder / "SKILL.md"
    if not skill_md.is_file():
        result.errors.append(f"No SKILL.md in {folder}. Every skill needs one, spelled exactly SKILL.md.")
        return result
    try:
        text = skill_md.read_bytes().decode("utf-8-sig")
    except UnicodeDecodeError:
        result.errors.append("SKILL.md isn't saved as UTF-8. Save it as UTF-8 (most editors have it under Save As or Encoding).")
        return result
    fields, body = read_frontmatter(text, result)
    if fields is None:
        result.errors.append("SKILL.md must start with a frontmatter block between two --- lines.")
        return result
    check_fields(fields, result)
    check_name(fields.get("name", ""), folder, result)
    check_description(fields.get("description", ""), result)
    check_placeholders(text, result)
    check_files(folder, body, result)
    lines = len(text.splitlines())
    if lines > 500:
        result.tips.append(f"SKILL.md is {lines} lines. Keep it under 500: move detail into files in references/ and point to them.")
    return result


def check_fields(fields, result):
    extra = sorted(set(fields) - OFFICIAL_FIELDS)
    if extra:
        result.tips.append(f"Frontmatter field(s) {', '.join(extra)} are not in the Agent Skills format. Claude Code accepts them, "
                           "but an upload to claude.ai fails on them. Remove them if the skill will be uploaded.")


def check_name(name, folder, result):
    if not name:
        result.errors.append("The frontmatter has no name. Add a line like: name: weekly-report")
        return
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        result.errors.append(f"name '{name}' may only use lowercase letters, numbers and single hyphens (weekly-report, not Weekly Report).")
    if len(name) > 64:
        result.errors.append(f"name is {len(name)} characters; the maximum is 64.")
    for word in ("claude", "anthropic"):
        if word in name:
            result.errors.append(f"name may not contain the reserved word '{word}'.")
    if folder.name != name:
        result.errors.append(f"The folder is called '{folder.name}' but the name is '{name}'. They have to be the same.")


def check_description(desc, result):
    if not desc:
        result.errors.append("The frontmatter has no description. It is how the AI decides when to use the skill, so it is required.")
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
    if re.search(r"(?<![\w/])(?:I'm|I'll|I|my)(?![\w/])", desc) or re.search(r"\byou can\b", desc, re.I):
        result.tips.append("Write the description in the third person ('Builds ...', 'Use when ...'), not with I or you.")


def check_placeholders(text, result):
    prose = re.sub(r"`[^`\n]*`", "", strip_fences(text))  # a marker in code is a mention or an example, not a gap
    for marker in ("[FILL IN", "[TODO"):
        count = prose.count(marker)
        if count:
            result.errors.append(f"{count} unfilled {marker}...] placeholder(s) left in SKILL.md.")
    if "<!--" in prose:
        result.tips.append("SKILL.md still has <!-- guidance comments --> from the template. Delete them once the section is filled in.")


def check_files(folder, body, result):
    """Every file the skill points to has to be in the skill folder, so it travels with the skill."""
    body = strip_fences(body)
    links = re.findall(r"\]\(([^)#\s]+)", body)
    paths = re.findall(r"(?<![\w/.-])((?:scripts|references|assets)/[\w./-]*[\w-])", body)
    for ref in dict.fromkeys(links + paths):
        if re.match(r"^[a-z]+:", ref):
            continue
        if ref.startswith(("../", "/", "~")):
            result.tips.append(f"SKILL.md points to {ref}, outside the skill folder. That file won't travel with the skill when it's "
                               "uploaded or shared: name it as a context file the user provides instead.")
            continue
        if not (folder / ref).exists():
            result.errors.append(f"SKILL.md points to {ref}, but that file is not in the skill folder.")


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
