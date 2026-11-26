# Checklist

For when you can't run `scripts/validate.py`. Go through every line; the first two groups are what the script checks.

## The skill will break without these

- [ ] The file is called `SKILL.md`, in capitals, inside a folder.
- [ ] It starts with a frontmatter block: a `---` line, the fields, another `---` line.
- [ ] `name` uses only lowercase letters, numbers and single hyphens, is 64 characters or fewer, and doesn't contain `claude` or `anthropic`.
- [ ] The folder has exactly the same name as `name`.
- [ ] `description` is there, 1,024 characters or fewer, without `<` or `>`.
- [ ] Any value with a colon followed by a space, or with ` #` in it, is in double quotes.
- [ ] For an upload to claude.ai: the frontmatter has only `name`, `description` and, if needed, `license`, `compatibility`, `metadata` or `allowed-tools`.
- [ ] No `[FILL IN: ...]` or `[TODO]` gaps are left.
- [ ] Every file the skill mentions (`references/...`, `scripts/...`, `assets/...`) is in the folder.

## It works, but worse, without these

- [ ] The description is on one line and reads "Does X. Use when Y.", in the third person, in 200 characters or fewer.
- [ ] `SKILL.md` is under 500 lines.
- [ ] No `<!-- guidance comments -->` from the template are left.

## Only a person can check these

- [ ] One job. If the skill does two things with different triggers, it should be two skills.
- [ ] Every step ends on something you can check.
- [ ] Each rule says why.
- [ ] There is a real example of finished work the expert signed off on.
- [ ] Brand and product details are in context files the skill points to, not copied in.
- [ ] The Gotchas section has at least one real gotcha from the expert.
- [ ] The expert read an output and would sign it as their own work.
