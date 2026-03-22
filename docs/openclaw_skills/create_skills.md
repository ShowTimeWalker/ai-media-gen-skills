# Creating Skills

Skills teach the agent how and when to use tools. Each skill is a directory containing a `SKILL.md` file with YAML frontmatter and markdown instructions.

For how skills are loaded and prioritized, see [Skills](./skills.md).

## Create Your First Skill

### Step 1: Create the skill directory

Skills live in your workspace. Create a new folder:

```bash
mkdir -p ~/.openclaw/workspace/skills/hello-world
```

### Step 2: Write SKILL.md

Create `SKILL.md` inside that directory. The frontmatter defines metadata, and the markdown body contains instructions for the agent.

```yaml
---
name: hello_world
description: A simple skill that says hello.
---

# Hello World Skill

When the user asks for a greeting, use the `echo` tool to say
"Hello from your custom skill!".
```

### Step 3: Add tools (optional)

You can define custom tool schemas in the frontmatter or instruct the agent to use existing system tools (like `exec` or `browser`). Skills can also ship inside plugins alongside the tools they document.

### Step 4: Load the skill

Start a new session so OpenClaw picks up the skill:

```bash
# From chat
/new

# Or restart the gateway
openclaw gateway restart
```

Verify the skill loaded:

```bash
openclaw skills list
```

### Step 5: Test it

Send a message that should trigger the skill:

```bash
openclaw agent --message "give me a greeting"
```

Or just chat with the agent and ask for a greeting.

---

## Skill Metadata Reference

The YAML frontmatter supports these fields:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (snake_case) |
| `description` | Yes | One-line description shown to the agent |
| `metadata.openclaw.os` | No | OS filter (`["darwin"]`, `["linux"]`, etc.) |
| `metadata.openclaw.requires.bins` | No | Required binaries on PATH |
| `metadata.openclaw.requires.config` | No | Required config keys |

---

## Best Practices

- **Be concise** — instruct the model on what to do, not how to be an AI
- **Safety first** — if your skill uses `exec`, ensure prompts don't allow arbitrary command injection from untrusted input
- **Test locally** — use `openclaw agent --message "..."` to test before sharing
- **Use ClawHub** — browse and contribute skills at ClawHub

---

## Where Skills Live

| Location | Precedence | Scope |
|----------|------------|-------|
| `<workspace>/skills/` | Highest | Per-agent |
| `~/.openclaw/skills/` | Medium | Shared (all agents) |
| Bundled (shipped with OpenClaw) | Lowest | Global |
| `skills.load.extraDirs` | Lowest | Custom shared folders |

---

## Related

- [Skills](./skills.md) — Loading, precedence, and gating rules
- [Skills Config](./skills_config.md) — `skills.*` config schema
- ClawHub — Public skill registry
- Building Plugins — Plugins can ship skills
