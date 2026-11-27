# Writing guide

How to write a skill that the AI picks at the right moment and then follows well. Sources: the Agent Skills format (agentskills.io/specification), Anthropic's skill authoring best practices (platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) and Anthropic's own skill-creator.

## Contents

- The description
- The name
- The body
- Steps
- Examples and templates
- Files next to SKILL.md
- What to leave out

## The description

The description is the only part of a skill the AI sees before it decides to use it. Every installed skill's name and description sit in the AI's context all the time; the rest loads only when the skill fires. So the description decides whether the skill is ever used.

- Write it as **"Does X. Use when Y."** Third person for what it does ("Writes the weekly report", not "I plan" or "You can use this to"), then the moments it should fire.
- Put every trigger in the description, none in the body. The body is only read after the choice is made.
- Use the words people actually type, including the cases where they never say the domain word: "...or when someone asks for the Monday update".
- Lean a little pushy. AI models tend to skip skills they could have used, so name the situations clearly.
- Keep it to one line and 200 characters or fewer. The format allows 1,024, but Claude's help pages ask for 200, and a short description is easier to pick out from a hundred others.
- No `<` or `>`.

## The name

- Lowercase letters, numbers and single hyphens, up to 64 characters: `weekly-report`, `launch-email`.
- The folder has exactly the same name. An upload fails if they differ.
- Say what it does. Avoid `helper`, `tools`, `utils`.
- The words `claude` and `anthropic` are reserved.

## The body

- Keep `SKILL.md` under 500 lines. Move detail that only some runs need into `references/` and say when to read it: "Read `references/charts.md` when the report needs charts."
- Assume the AI is already smart. For each paragraph, ask whether it changes what the AI would do without it. If not, cut it.
- Explain why. "Check last week's numbers first, because every comparison in the report builds on them" handles cases a bare rule never covered. Writing ALWAYS or NEVER in capitals is a sign the reason is missing.
- Say what to do, not what to avoid. Name the target behaviour, and keep a "never" only for a hard limit you can't phrase another way.
- Use one word for one thing all the way through. If it's a "brief" in step 2, it's not a "plan" in step 4.
- Give one default way and an escape for the exception, not a menu of five options.
- Leave out anything that will go stale, like "as of this month" or a price. If it must be there, put it in its own clearly dated section.
- Use forward slashes in paths: `references/specs.md`.

## Steps

- Number them, in the order the expert does them.
- Match how strict each step is to how fragile it is. Where many approaches work, describe the goal. Where one wrong move breaks things, give exact steps, a template or a script.
- End each step on something checkable: "Done when the conversion event is confirmed firing." A vague end ("once you understand the audience") gets rushed.
- Build in a check-and-fix loop for anything that can be verified: run the check, fix, run it again.
- Under each step, write what good looks like and the usual mistake. That's where the expert's judgement lives.

## Examples and templates

- One real example of finished work teaches more than a page of rules. The AI copies an example better than it follows a description of one.
- For a fixed output format, write the format out as a template in the skill.
- Use examples the expert signed off on. An example the AI invented from general knowledge teaches it average work.

## Files next to SKILL.md

| Folder | For | Loaded |
|---|---|---|
| `references/` | Detail only some runs need: specs, long checklists, edge cases | Only when SKILL.md sends the AI there |
| `scripts/` | Code for what must come out exactly the same every time | Run; only the output enters the conversation |
| `assets/` | Files the output uses: templates, logos, fonts | Used, not read |

- Link every file straight from `SKILL.md`, one level deep. A file that is only linked from another reference file may only get skimmed.
- Give any reference file over 100 lines a short contents list at the top, like this one.

## What to leave out

- Brand, audience and product details. They belong in the team's context files, which the skill names. Then one update reaches every skill.
- Background the AI already knows ("A report summarises results").
- Notes about how the skill was made. Credits go in the README, not in `SKILL.md`.
