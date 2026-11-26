---
name: skill-builder
description: Interviews the person who knows a task, then writes, checks and tests a skill for it. Use when someone wants to create or improve a skill, or make a process repeatable with AI.
---

# Skill builder

A skill is a folder with a `SKILL.md` file: written instructions an AI follows every time a certain task comes up, plus any files that task needs. This skill gets the process out of the head of the person who knows it best and into that folder, then proves it works before anyone relies on it.

The people using this are often marketers, founders and operators, not developers. Talk to them in plain words. When a term like frontmatter or folder structure comes up, explain it in the same sentence the first time.

Two branches:

- **New skill:** do steps 1 to 6.
- **Existing skill to improve or review:** read the skill, run step 4 on it, then go to step 5. Keep its name and folder name unchanged, because other skills, people and tools may call it by that name.

## 1. Get the process out of the expert's head

If the conversation already shows the process (the user did the task with you, or pasted a playbook), pull the answers from there first and only ask about the gaps.

Otherwise interview the person who does the task best. Ask in one message, not one question at a time:

1. Which task should the skill handle, and what does finished look like?
2. What would someone type when they need it? Ask for two or three real phrasings.
3. Walk me through the last time you did it, step by step. Why do you do each step?
4. Where do juniors or newcomers usually go wrong?
5. Can you share one example of finished work you were happy with?
6. What does the AI need to know that isn't about the task itself, such as brand, audience or product details? Where does that already live?

Ask "why" after every step they name. The reasons are what turn a checklist into the senior's thinking. When they say "it depends", ask what it depends on and write the cases down.

**Done when** you can fill every part of `assets/skill-template.md` without guessing. Anything still unknown stays a visible `[FILL IN: ...]` gap for the user, never an invented answer.

## 2. Decide the shape

- **One skill, one job.** If the interview turned up two tasks with different triggers, make two skills.
- **Name:** lowercase words joined by hyphens, saying what it does: `meta-campaign`, `weekly-report`. The folder gets the same name.
- **What goes where:**
  - `SKILL.md`: the steps and the rules every run needs. Keep it under 500 lines.
  - `references/`: detail only some runs need (a long checklist, platform specs, edge cases). `SKILL.md` says when to read each file.
  - `scripts/`: code for anything that must come out exactly the same every time (a calculation, a format check).
  - `assets/`: files the output uses (a template, a logo).
- **Brand and product knowledge stays outside the skill.** If the team keeps context files (brand, voice, audience, products), the skill names the ones to read for this task instead of copying them in. Then a brand update reaches every skill at once.

**Done when** you know the name, the folders it needs and which context files it points to.

## 3. Write it

Copy `assets/skill-template.md` into the new folder as `SKILL.md` and fill it in. Read `references/writing-guide.md` before you write the description and the steps: the description decides whether the AI ever uses the skill, and the steps decide how well.

Write in the expert's words where you can. Use their phrases for what good looks like and for the mistakes. Explain why behind each rule; a model that understands the reason handles cases the rule never mentioned.

**Done when** every `[FILL IN: ...]` is replaced and the expert's example is in the skill or in `references/`.

## 4. Check it

If you can run code, run the checker on the folder:

```
python3 scripts/validate.py path/to/the-skill
```

Fix every ERROR. For every TIP, fix it or tell the user why it can stay. If you can't run code, go through `references/checklist.md` by hand.

**Done when** the checker shows no errors and you have gone through each tip.

## 5. Test it on real work

1. Write two or three prompts the way a real team member would type them, with real-looking details. Show them to the user and adjust.
2. Run each prompt with the skill. If you can start a separate agent or a fresh chat, run it there, so the test doesn't lean on what you already know from building it. If you can, run the same prompt once without the skill too, so the user sees what the skill adds.
3. Show the outputs to the expert and ask: would you sign off on this as your own work? Note every "no" and why.
4. Fix the skill for the pattern behind each "no", not only for that one prompt. Then run the prompts again.
5. Check the trigger: write three prompts that should use the skill and two close calls that shouldn't (same topic, different job). Read the description against each one and sharpen it until it fits all five.

If the user wants a second opinion, have a different AI model review the skill and one output. A model rarely spots its own blind spots.

**Done when** the expert signs off on the outputs, or tells you to stop.

## 6. Hand it over

- Tell the user how to install it where they work. `references/install.md` covers Claude, Claude Code and the other tools that read this format.
- Zip the folder when they need to upload it.
- Tell them how the skill stays good: whenever it gets something wrong, add the mistake and the fix to its Gotchas section, the same way the expert would correct a junior.

**Done when** the user has the skill installed, or has the folder and knows how to install it.
