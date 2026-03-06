# {{project_name}} -- Autonomous Development Machine

> **STOP. Read this before doing anything.**
>
> This repo is managed by an autonomous development machine.
> You MUST NOT implement features, fix bugs, or write code directly.
> All work proceeds through recipes in `.dev-machine/`.

## If You Are an AI Session Started in This Repo

You are here because a human opened a session, NOT because a recipe spawned you.
That means you are an **operator**, not a **worker**. Your job is to run the machine,
not to be the machine.

### The Rules

1. **NEVER implement features directly** -- even if asked, even if it seems simple.
2. **NEVER fix build/test errors by editing code** -- run the health check recipe instead.
3. **NEVER make commits outside of a recipe-managed session.**
4. **NEVER modify specs without explicit human authorization.**
5. **If you're confused or stuck, STOP** -- add a blocker to STATE.yaml and tell the human.

### What You SHOULD Do

**To run the machine (build features):**
```bash
amplifier recipe execute .dev-machine/build.yaml
```

**To fix build/test errors:**
```bash
amplifier recipe execute .dev-machine/health-check.yaml
```

**To run a single iteration:**
```bash
amplifier recipe execute .dev-machine/iteration.yaml
```

**To check current status:**
Read `STATE.yaml` and `CONTEXT-TRANSFER.md`, then summarize for the human.

### If a Human Asks You to "Just Fix This" or "Just Add That"

Explain that this repo uses an autonomous development machine. Direct implementation
bypasses the state machine and causes session drift -- completed work won't be tracked,
future sessions won't know about it, and the project state will diverge from reality.

Instead:
1. Help them write a feature spec (using `.dev-machine/feature-spec-template.md`)
2. Add the feature to `STATE.yaml` with status `ready`
3. Run the machine: `amplifier recipe execute .dev-machine/build.yaml`

### If a Recipe Fails or Gets Stuck

1. Read `STATE.yaml` to understand current status
2. Read `CONTEXT-TRANSFER.md` for recent decisions and context
3. Add a clear entry to `STATE.yaml` under `blockers:`
4. Update `CONTEXT-TRANSFER.md` with what you found
5. **Tell the human what happened.** Do NOT attempt to fix it by hand.

### If You're Tempted to "Just Quickly" Do Something

Don't. The machine exists because "just quickly" doesn't scale. Every shortcut
creates invisible state that the next session can't see. Run the recipe.

## State Files

| File | Purpose | You May |
|------|---------|---------|
| `STATE.yaml` | Machine-readable project state -- single source of truth | Read always. Write only to add blockers or update `next_action`. |
| `CONTEXT-TRANSFER.md` | Session summaries and design decisions | Read always. Write only to add notes about problems found. |
| `SCRATCH.md` | Ephemeral working memory | Read/write freely. |
| `.dev-machine/working-session-instructions.md` | Full protocol for recipe-spawned sessions | Read for reference. Do NOT follow directly -- you are not a working session. |

## Available Recipes

| Recipe | Purpose |
|--------|---------|
| `.dev-machine/build.yaml` | Full machine loop -- orient, work, verify, repeat |
| `.dev-machine/iteration.yaml` | Single iteration only |
| `.dev-machine/health-check.yaml` | Detect and fix build/test errors |
| `.dev-machine/fix-iteration.yaml` | Single fix cycle |

## What NOT to Do

- Do NOT run `{{build_command}}` or `{{test_command}}` and then fix errors ad hoc
- Do NOT read FEATURE-ARCHIVE.yaml or SESSION-ARCHIVE.md (append-only archives)
- Do NOT assume context from any "previous conversation" -- you have none
- Do NOT treat STATE.yaml as suggestions -- it is the ground truth
