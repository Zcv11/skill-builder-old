# Installing a skill

A skill is the same folder everywhere. Only where you put it differs. Each tool keeps its own copy, so a skill added in one place doesn't appear in the others.

## Claude (claude.ai and the Claude apps)

1. Turn on code execution: Settings > Capabilities.
2. Zip the skill folder so the folder itself sits at the top of the zip (the zip contains `weekly-report/SKILL.md`, not a loose `SKILL.md`).
3. Go to Customize > Skills, press +, choose Create skill > Upload a skill, and pick the zip.

Skills that point to brand or product files need those files nearby: put them in a Project's knowledge and use the skill inside that Project.

Custom skills work on every plan, Free included. On Team and Enterprise plans an owner can share a skill with the whole organisation. Claude's help pages explain the current steps if the menus have moved: support.claude.com, "Using skills in Claude".

## Claude Code

Copy the folder to one of these:

- `~/.claude/skills/weekly-report/` for yourself, in every project.
- `.claude/skills/weekly-report/` inside a project, for everyone who works in it. Commit it with the project.

Claude Code picks up new and changed skills while it runs. Type `/weekly-report` to run one by hand.

## Other tools that read the same format

| Tool | Where the folder goes |
|---|---|
| OpenAI Codex | `~/.agents/skills/` or `.agents/skills/` in the project |
| GitHub Copilot | `~/.copilot/skills/` or `.github/skills/` in the project |
| Cursor | `.cursor/skills/` or `.agents/skills/` in the project |
| Gemini CLI | `~/.gemini/skills/` or `.agents/skills/` in the project |

`.agents/skills/` inside a project works in most of them at once. These locations change as the tools update; each tool's own docs have the current list.

## Keeping a team on the same version

Keep the team's skills in one shared place, like a GitHub repository, and install from there. When the expert updates a skill, everyone gets the same new version instead of their own copy drifting.
