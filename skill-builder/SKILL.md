---
name: skill-builder
description: Interviews the person who does a task best, then writes, checks and tests a skill for it. Use when someone wants to turn a process or the way their senior works into a skill, or improve one.
---

# Skill builder

A skill is a folder with a `SKILL.md` file: written instructions an AI follows every time a certain task comes up, plus any files that task needs. This skill gets the process out of the head of the person who knows it best and into that folder, then proves it works before anyone relies on it.

The people using this are often marketers, founders and operators, not developers. Talk to them in plain words. When a term like frontmatter or folder structure comes up, explain it in the same sentence the first time.

Two branches:

- **New skill:** do steps 1 to 6.
- **Existing skill to improve or review:** read the skill, run step 4 on it, then go to step 5. Keep its name and folder name unchanged, because other skills, people and tools may call it by that name. If the checker flags the name itself, tell the user what a rename would break and let them decide.

## 1. Interview the expert

The interview is the heart of this skill: a skill is only as good as what you get out of the expert's head. A form filled in once gets the steps; an interview gets the reasons, the judgement calls and the mistakes, which are the parts a junior doesn't have.

If the conversation already shows the process (the user did the task with you, or pasted a playbook), take what you can from it and interview about the rest.

Run the interview in **rounds**. A round is one message with up to about six numbered questions, the ones whose answers change the skill most, so the expert can answer them in one go; long, rambling or dictated answers are fine. The rest wait for the next round. Then wait for the answers and build the next round from them. Ask only what a person can answer; look up anything you can find yourself, such as a file they mentioned.

**Round 1, the whole task:**

1. Which task should the skill handle, and what does finished look like?
2. What would someone type when they need it? Two or three real phrasings.
3. Walk me through the last time you did it, step by step, and why you do each step.
4. Where do juniors go wrong anywhere in the task, and what do you always check before it goes out?
5. Can you paste one piece of finished work you were happy with? The real thing, not an outline: its length and tone teach more than any rule.
6. What does the AI need to know that isn't about the task itself, such as brand, audience or product details? Which files hold that, and where are they?

**Every round after that digs into the answers you got:**

- For each step: why it's done, what good looks like, and where juniors or newcomers go wrong.
- Every "it depends": what it depends on, and what they do in each case.
- Every vague word ("make it punchy", "check it's right"): what exactly they look at to decide.
- Gaps: a step that seems to be missing, a tool or file they use without naming it, who signs off.
- Anything in the finished example that the steps don't explain.

Be relentless: one round rarely gets past the steps, and the second and third rounds are where the thinking comes out. Move to the recap when every section of `assets/skill-template.md` is answered or on the open-questions list, or when a round brings no new step, case or reason. After round 3, ask the expert whether to keep going. When they want to stop, go to the recap with what you have and put everything still unknown on the open-questions list.

Keep a list of **open questions**: everything the expert hasn't answered yet. An open question is never filled with a guess, because a guess in a skill gets repeated on every run.

**Recap before you write.** Send the process back, short and in the expert's own words: each step with its reason, the cases, the usual mistakes. Ask: "Is this how you do it? What's missing or wrong?" Apply their corrections. If a step or case changed, send back only that part once, then go on.

**Done when** the expert has confirmed the recap and every remaining unknown is on the open-questions list.

## 2. Decide the shape

- **One skill, one job.** If the interview turned up two tasks with different triggers, make two skills.
- **Name:** lowercase words joined by hyphens, saying what it does: `weekly-report`, `launch-email`. The folder gets the same name.
- **What goes where:**
  - `SKILL.md`: the steps and the rules every run needs. Keep it under 500 lines.
  - `references/`: detail only some runs need (a long checklist, platform specs, edge cases). `SKILL.md` says when to read each file.
  - `scripts/`: code for anything that must come out exactly the same every time (a calculation, a format check).
  - `assets/`: files the output uses (a template, a logo).
- **Brand and product knowledge stays outside the skill.** If the team keeps context files (brand, voice, audience, products), the skill names the ones to read for this task and says where they live, instead of copying them in. Then a brand update reaches every skill at once. Also decide what the skill does when a file is missing: usually it asks the user to paste the part it needs.
- **Script or not:** add a script to `scripts/` only where the AI has to be exact and tends not to be, like counting characters, adding up a budget or checking a format. Everything else stays as written steps.
- **Where to save it:** a folder named after the skill, in the user's working folder or wherever they keep the team's skills. Ask if it isn't obvious.

**Done when** you know the name, the folders it needs, which context files it points to and where it gets saved.

## 3. Write it

Copy `assets/skill-template.md` into the new folder as `SKILL.md` and fill it in. Read `references/writing-guide.md` before you write the description and the steps: the description decides whether the AI ever uses the skill, and the steps decide how well.

Write in the expert's words where you can. Use their phrases for what good looks like and for the mistakes. Explain why behind each rule; a model that understands the reason handles cases the rule never mentioned.

- **Order:** put the steps in the order they're actually done. If that differs from how the expert listed them ("I write the subject line last"), confirm the order with them.
- **Only what the expert said:** leave out a "Good looks like" or "Common mistake" line when the expert gave nothing for it. A mistake tied to one step goes under that step. A fact that trips people up anywhere in the task goes in Gotchas. Each one goes in one place, not both.
- **Steps a person has to do:** when a step needs a human (reading it on a phone, a final sign-off), write it as a hand-back: the skill tells the user to do it and what to look for.
- **Open questions** stay as `[FILL IN: question]` in the skill. The checker treats them as errors on purpose: a skill with open questions is a draft, not finished.

**Done when** every part of the template is either filled from the expert's answers or marked as an open question.

## 4. Check it

If you can run code, run the checker on the folder:

```
python3 scripts/validate.py path/to/the-skill
```

Fix every ERROR. For every TIP, fix it or tell the user why it can stay. If you can't run code, go through `references/checklist.md` by hand.

If the only errors left are open questions, send the expert the list in one message and fill in their answers. An open question is cleared only by the expert's answer, never by text written to make the checker pass. When the expert isn't available, go on to step 5 with the draft and say clearly that it isn't finished until those questions are answered.

**Done when** the checker shows no errors, or only open questions that are with the expert, and you have gone through each tip.

## 5. Test it on real work

1. Write two or three prompts the way a real team member would type them, with real-looking details. Show them to the user and adjust.
2. Give the test the context files the skill points to: the real ones, or a short sample from the user. Without them the test only shows the skill asking for its files.
3. Run each prompt with the skill. If you can start a separate agent or a fresh chat, run it there, so the test doesn't lean on what you already know from building it. To show what the skill adds, run the same prompt in a fresh chat without the skill and put the two outputs side by side.
4. Show the outputs to the expert and ask: would you sign off on this as your own work? Note every "no" and why.
5. Fix the skill for the pattern behind each "no", not only for that one prompt. Then run the prompts again.
6. Check the trigger: write three prompts that should use the skill and two close calls that shouldn't (same topic, different job). Read the description against each one and sharpen it until it fits all five. Keep the expert's own phrases, but when one also fits a different job (a "customer email" that could be a welcome email), make it more specific and check the change with the expert.

If the user wants a second opinion, have a different AI model review the skill and one output. A model rarely spots its own blind spots.

**Done when** the expert signs off on the outputs, or tells you to stop.

## 6. Hand it over

- Tell the user how to install it where they work. `references/install.md` covers Claude, Claude Code and the other tools that read this format.
- Zip the folder when they need to upload it.
- Tell them how the skill stays good: whenever it gets something wrong, add the mistake and the fix to its Gotchas section, the same way the expert would correct a junior.

**Done when** the user has the skill installed, or has the folder and knows how to install it.
