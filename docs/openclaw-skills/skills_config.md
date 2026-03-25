# Skills Config

All skills-related configuration lives under `skills` in `~/.openclaw/openclaw.json`.

## Example Configuration

```json
{
  "skills": {
    "allowBundled": ["gemini", "peekaboo"],
    "load": {
      "extraDirs": ["~/Projects/agent-scripts/skills", "~/Projects/oss/some-skill-pack/skills"],
      "watch": true,
      "watchDebounceMs": 250
    },
    "install": {
      "preferBrew": true,
      "nodeManager": "npm"
    },
    "entries": {
      "image-lab": {
        "enabled": true,
        "apiKey": { "source": "env", "provider": "default", "id": "GEMINI_API_KEY" },
        "env": {
          "GEMINI_API_KEY": "GEMINI_KEY_HERE"
        }
      },
      "peekaboo": { "enabled": true },
      "sag": { "enabled": false }
    }
  }
}
```

> **Note**: For built-in image generation/editing, prefer `agents.defaults.imageGenerationModel` plus the core `image_generate` tool. `skills.entries.*` is only for custom or third-party skill workflows.

**Examples:**

- Native Nano Banana-style setup: `agents.defaults.imageGenerationModel.primary: "google/gemini-3-pro-image-preview"`
- Native fal setup: `agents.defaults.imageGenerationModel.primary: "fal/fal-ai/flux/dev"`

## Fields

### Top-level Fields

| Field | Description |
|-------|-------------|
| `allowBundled` | Optional allowlist for bundled skills only. When set, only bundled skills in the list are eligible (managed/workspace skills unaffected). |
| `load.extraDirs` | Additional skill directories to scan (lowest precedence). |
| `load.watch` | Watch skill folders and refresh the skills snapshot (default: `true`). |
| `load.watchDebounceMs` | Debounce for skill watcher events in milliseconds (default: `250`). |
| `install.preferBrew` | Prefer brew installers when available (default: `true`). |
| `install.nodeManager` | Node installer preference (`npm` \| `pnpm` \| `yarn` \| `bun`, default: `npm`). This only affects skill installs; the Gateway runtime should still be Node (Bun not recommended for WhatsApp/Telegram). |
| `entries.<skillKey>` | Per-skill overrides. |

### Per-skill Fields (under `entries.<skillKey>`)

| Field | Description |
|-------|-------------|
| `enabled` | Set `false` to disable a skill even if it's bundled/installed. |
| `env` | Environment variables injected for the agent run (only if not already set). |
| `apiKey` | Optional convenience for skills that declare a primary env var. Supports plaintext string or SecretRef object (`{ source, provider, id }`). |

## Notes

- Keys under `entries` map to the skill name by default. If a skill defines `metadata.openclaw.skillKey`, use that key instead.
- Changes to skills are picked up on the next agent turn when the watcher is enabled.

## Sandboxed Skills + Env Vars

When a session is sandboxed, skill processes run inside Docker. The sandbox **does not** inherit the host `process.env`.

Use one of:

- `agents.defaults.sandbox.docker.env` (or per-agent `agents.list[].sandbox.docker.env`)
- Bake the env into your custom sandbox image

> **Note**: Global env and `skills.entries.<skill>.env/apiKey` apply to host runs only.

## Related

- [Skills](./skills.md) — Overview, loading, precedence, and gating rules
- [Creating Skills](./create_skills.md) — How to create your own skills
- ClawHub — Public skill registry
