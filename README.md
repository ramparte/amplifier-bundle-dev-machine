# Dev Machine

An Amplifier bundle that helps you build autonomous development machines -- systems that implement software from specs in bounded, disposable, stateless LLM sessions orchestrated by YAML recipes.

**Proven at scale:** word4 shipped 278 features across 106 autonomous sessions in 5.5 days (~89K LOC, 3,714 tests, 445 commits). The same pattern has since been used to build amplifier-safeguard, openM365, and universal-app.

## The Core Idea

A dev machine is a loop:

```
read STATE.yaml --> pick next feature --> spawn zero-context session -->
implement from spec (TDD) --> verify build+test --> commit --> update state --> repeat
```

Every session is disposable. Every session reads the spec before writing code. Every session runs build and test before committing. The machine never improvises -- it implements what the spec says, or it stops and adds a blocker.

**The spec is the product.** The machine is just a loop that executes specs. If your specs are good, the machine builds good software. If your specs are vague, the machine builds vague software. Everything in this workflow exists to produce and consume high-quality specs.

---

## The Workflow

There are four phases. The first one is the most important.

### Phase 0: Brainstorm the Spec (`/brainstorm`)

> This is where you spend most of your time. Everything downstream depends on this.

Before touching any dev-machine tooling, open an Amplifier session and enter brainstorm mode:

```
/brainstorm
```

This is a collaborative design session where you and the AI work out:

- **What you're building** -- the product vision, user stories, core problem
- **The architecture** -- data model, module boundaries, technology choices, key patterns
- **The spec hierarchy** -- which modules exist, what their interfaces look like, what the first batch of features should be

The output of brainstorming is an **architecture spec** (the "constitution") and enough clarity to answer the five admissions gates. In word4, this took about an hour and produced a 947-line spec. In openM365, it produced a 2,226-line spec with constitutional markers. In safeguard, a tighter 485-line spec with explicit performance targets.

**What makes a good architecture spec:**

| Section | Purpose | Example |
|---------|---------|---------|
| Data model | Complete type definitions | Full TypeScript interfaces or Python dataclasses |
| Module boundaries | What owns what, dependency DAG | "renderer depends on document-model, never on crdt-engine" |
| Forbidden dependencies | What must NOT depend on what | Prevents architectural drift |
| Technology choices | Stack decisions with rationale | "Yjs for CRDT because X, not Automerge because Y" |
| Key patterns | How things flow through the system | Request lifecycle, event pipeline, state management |
| Performance targets | Measurable constraints | "< 50ms for document operations" |
| Explicit exclusions | What you're NOT building | Prevents scope creep in every downstream spec |

**Best practice from openM365:** Mark critical sections with `[CONSTITUTIONAL]` tags. These require human approval to change -- the machine cannot unilaterally modify them.

**Best practice from safeguard:** Include a "Not In Scope" section at every level. The architecture spec says what the system doesn't do. Module specs say what the module doesn't own. Feature specs say what the feature doesn't cover. This is the single most effective anti-gold-plating measure.

---

### Phase 1: Admissions (`/admissions`)

Once you have a solid spec from brainstorming, evaluate whether your project is ready for autonomous development:

```
/admissions
```

The admissions advisor runs your project through five gates:

| Gate | Question | What it checks |
|------|----------|----------------|
| 1. Decomposability | Can it break into hundreds of small units? | Feature count, independence, repeating patterns |
| 2. Verifiable Correctness | Can a machine verify its own work? | Test framework, build speed, automated checks |
| 3. Sufficient Architecture | Is there a constitution? | Architecture spec quality, module boundaries, data model |
| 4. Functioning Toolchain | Do build and test actually run? | `build_command` and `test_command` succeed from clean state |
| 5. Spec Quality | Can feature specs be written at machine quality? | Real interfaces, acceptance criteria, edge cases |

Each gate scores 0-100%. Below 50% on any gate is a **hard stop** -- the advisor will tell you exactly what to fix before proceeding. 50-75% means proceed with caution.

**Output:** `.dev-machine-assessment.md` in your project root.

**Real example -- safeguard scored 15% on Gate 4** because it had zero code, no build system, and no toolchain chosen. The assessment prescribed exactly what to do: choose the stack, scaffold the project, verify clean build/test. After remediation, the machine ran fine.

**What admissions is NOT:** A rubber stamp. The advisor reads your codebase, runs your commands, and evaluates your actual artifacts. It doesn't take your word for anything.

---

### Phase 2: Machine Design (`/machine-design`)

With admissions passed, design the machine itself:

```
/machine-design
```

This is a collaborative session (like brainstorming, but focused on the machine's configuration rather than the product). The designer collects:

**Required configuration:**

| Variable | What it is | Example |
|----------|-----------|---------|
| `project_name` | Short identifier | `word4`, `safeguard` |
| `project_dir` | Absolute path to project | `~/dev/my-project` |
| `build_command` | How to build | `pnpm build`, `uv run ruff check src/ && uv run pyright src/` |
| `test_command` | How to test | `pnpm test`, `uv run pytest tests/ -v` |
| `specs_dir` | Where specs live | `./specs` or `./docs/specs` |
| `architecture_spec` | Path to the constitution | `./specs/architecture.md` |
| `max_features_per_session` | Features per disposable session | 3-5 (default 3) |
| `qa_enabled` | Visual/integration QA? | `true` or `false` |

**Outputs:**
- `.dev-machine-design.md` -- the master design document with all config
- `specs/architecture.md` -- the constitution (if not already written during brainstorm)
- `specs/modules/*.md` -- module specs for first modules
- `specs/features/**/*.md` -- first batch of 5-15 feature specs

---

### Phase 3: Generate Machine (`/generate-machine`)

Stamp out the machine artifacts:

```
/generate-machine
```

This reads `.dev-machine-design.md` and generates everything the machine needs to run. No creative interpretation -- the design document is the specification.

**Generated output:**

```
your-project/
+-- .dev-machine/
|   +-- build.yaml                    # Outer loop: read state, dispatch sessions, repeat
|   +-- iteration.yaml                # Inner loop: orient, work, verify, archive
|   +-- health-check.yaml             # Fix loop: build+test until clean
|   +-- fix-iteration.yaml            # Surgical fix sessions
|   +-- qa.yaml                       # QA loop (if qa_enabled)
|   +-- qa-iteration.yaml             # QA sessions (if qa_enabled)
|   +-- working-session-instructions.md   # Protocol for recipe-spawned sessions
|   +-- feature-spec-template.md      # Template for writing new feature specs
+-- STATE.yaml                        # Machine-readable single source of truth
+-- CONTEXT-TRANSFER.md               # Human-readable session history
+-- SCRATCH.md                        # Ephemeral working memory
+-- AGENTS.md                         # AI guardrails (prevents direct code edits)
```

After generation, the machine is **completely independent** of this bundle. Zero runtime dependency.

---

## Running the Machine

Once generated, run the machine:

```bash
# Main build loop -- implements features from specs
amplifier recipe execute .dev-machine/build.yaml

# Health check -- fix build/test failures
amplifier recipe execute .dev-machine/health-check.yaml

# QA (if enabled) -- visual and integration testing
amplifier recipe execute .dev-machine/qa.yaml
```

**What happens during a build loop:**

1. Reads `STATE.yaml` to find features marked `ready`
2. Spawns a zero-context working session
3. The session orients itself by reading STATE.yaml, CONTEXT-TRANSFER.md, and the architecture spec
4. Picks up to `max_features_per_session` features
5. For each feature: reads spec, writes failing tests (RED), implements (GREEN), runs build+test, commits, updates state
6. Archives completed features, increments epoch, updates CONTEXT-TRANSFER.md
7. Repeats until all features are done or a blocker is hit

---

## Writing Feature Specs

This is the most important skill for operating a dev machine. The machine implements exactly what the spec says -- nothing more, nothing less.

### The Template

```markdown
# F-XXX: Feature Name

## 1. Overview
**Module:** module-name
**Priority:** P0 / P1 / P2
**Depends on:** F-YYY or none
**Estimated size:** S / M / L

Brief description: what this feature does and why it exists.

## 2. Requirements

### Interfaces
Real code signatures -- types, functions, classes. Not pseudocode.

### Behavior
Concrete rules the implementation must follow.

## 3. Acceptance Criteria
| # | Criterion | Verification |
|---|-----------|-------------|
| AC-1 | Specific, testable statement | unit test / integration test |

## 4. Edge Cases
| Case | Expected Behavior |
|------|------------------|
| Empty input | Returns empty list, does not throw |

## 5. Files to Create/Modify
| File | Action | Contents |
|------|--------|----------|
| src/auth/manager.py | Create | AuthManager class |

## 6. Not In Scope
What this feature explicitly does NOT cover, with forward
references to the feature that will handle it.

## 7. Notes
Non-obvious design choices, caveats, gotchas.
```

### What Makes a Spec Good Enough for a Machine

**Must have:**
- Real code signatures with types (not "a function that does X")
- Acceptance criteria that map directly to test assertions
- Explicit file paths (the machine needs to know where to write)
- Edge cases (the machine will not think of these on its own)

**Should have:**
- "Not In Scope" section (prevents gold-plating)
- Dependency declarations (the machine respects ordering)
- Size estimate (helps the machine plan session boundaries)

**Must NOT have:**
- Ambiguity that requires judgment ("make it feel responsive")
- Undeclared dependencies on features that don't exist yet
- Prose where code signatures should be

### Spec Quality Examples from Real Projects

**word4 F-010 (Yjs Document Binding):** 10 acceptance criteria each mapping to a unit test, 6 edge cases, 9 specific files listed with contents, references to architecture spec section 3.2.

**safeguard F-001 (Gateway App Skeleton):** Clear "What" paragraph, real Python classes with type annotations, minimal file table, explicit "Not In Scope" (e.g., "Database connection pool -- that's F-005/F-006").

**openM365 specs:** Evaluated at 80% quality even with only 5 of 156 written upfront -- because the architecture spec was detailed enough to function as a "super-spec" that constrained all downstream decisions.

### JIT vs. Upfront Spec Writing

You don't have to write all specs before starting the machine. The pattern that emerged across projects:

- **Architecture spec:** Written upfront during brainstorm. Immutable.
- **Module specs (1-2 pages each):** Written JIT when a module is first touched.
- **Feature specs (0.5-1 page each):** Written in batches of 5-15 before each machine run.

This is explicitly called "the word4 pattern" in openM365's design document. Keep the total context small: architecture + module spec + feature spec should be under 3,000 lines combined.

---

## The Three-Layer Spec Hierarchy

```
Architecture Spec ("The Constitution")        Written once during brainstorm
    |                                          Immutable without human approval
    v                                          Read by every session
Module Specs                                   Written JIT, one per module
    |                                          Interfaces, test strategy, dependencies
    v
Feature Specs                                  Written in batches before machine runs
                                               The atomic unit the machine implements
```

Each layer constrains the layer below it. A feature spec cannot violate the module spec. A module spec cannot violate the architecture. When a session discovers a conflict, it **stops and adds a blocker** -- it never resolves the conflict unilaterally.

---

## State Management

### STATE.yaml -- The Machine's Memory

```yaml
project: my-project
phase: 3
phase_name: "Phase 3: Core Features"
epoch: 45
next_action: "Implement F-042 through F-047"
blockers: []

architecture:
  spec: specs/architecture.md
  status: approved

modules:
  auth:
    spec: specs/modules/auth.md
    status: approved

features:
  F-042-session-management:
    name: Session Management
    module: auth
    status: ready
    spec: specs/features/auth/F-042-session-management.md
    depends_on: [F-041]
```

**Cardinal rules:**
- STATE.yaml is updated after every feature, not at session end
- Only `ready` and `in-progress` features live here -- completed features are archived to `FEATURE-ARCHIVE.yaml`
- If the machine hits a problem it can't resolve, it adds a `blocker` and stops

### CONTEXT-TRANSFER.md -- Session History

Human-readable record of what each session accomplished, what decisions were made, and what the next session should know. Old entries auto-archive to `SESSION-ARCHIVE.md` (keeps the last 5).

### SCRATCH.md -- Ephemeral

Working memory for the current session. Build errors, test output, in-progress notes. Disposable between sessions.

---

## How the Machine Protects Itself

### AGENTS.md -- The Guardrail

Every generated project gets an `AGENTS.md` with five immutable rules:

1. **NEVER** implement features directly
2. **NEVER** fix build/test errors by editing code -- run health check recipe
3. **NEVER** make commits outside recipe-managed sessions
4. **NEVER** modify specs without human authorization
5. If confused, **STOP** -- add a blocker to STATE.yaml

This exists because humans will open Amplifier sessions in the project repo and ask "just fix this." The AGENTS.md explains why that's dangerous:

> Direct implementation bypasses the state machine. Completed work won't be tracked, future sessions won't know about it, and the project state will diverge from reality.

### Structural Monitoring

The working session protocol enforces size discipline:
- **Module > 10,000 LOC:** Hard stop. Create a refactoring plan.
- **File > 1,000 lines:** Warning. Flag for decomposition.

### Build Gate

Every session runs `build_command` and `test_command` after every feature. If either fails, the session stops and records the failure. The health check recipe handles surgical fixes in a separate loop.

---

## Best Practices (Learned from Four Projects)

### On Specs

1. **Spend the time in brainstorm.** word4's founding session was ~1 hour for 947 lines. That hour determined the quality of 278 features.

2. **Specs are code signatures, not prose.** "A function that authenticates users" is useless. `async def authenticate(credentials: Credentials) -> AuthResult` is actionable.

3. **Include "Not In Scope" at every level.** Architecture, module, and feature specs should all say what they don't cover. Forward-reference the feature that will handle it.

4. **Mark constitutional sections.** openM365 uses `[CONSTITUTIONAL]` tags for sections that require human approval to change. This prevents the machine from drifting on fundamental decisions.

5. **Size discipline on specs.** Feature specs: 0.5-1 page. Module specs: 1-2 pages. If a feature spec is longer than a page, the feature is too big -- decompose it.

### On Machine Operation

6. **3-5 features per session, then dispose.** Long sessions accumulate context and degrade. Short sessions stay sharp.

7. **Run health check after every 10-20 build sessions.** Build errors compound. Catch them early.

8. **Blockers are good.** A machine that stops and asks for help is working correctly. A machine that improvises around ambiguity is dangerous.

9. **Archive aggressively.** Completed features go to `FEATURE-ARCHIVE.yaml`. Old sessions go to `SESSION-ARCHIVE.md`. Keep STATE.yaml under 300 lines.

10. **Don't skip admissions.** Safeguard scored 15% on the toolchain gate and had to remediate before the machine could run at all. Better to know upfront.

### On Adding Features Mid-Run

To add new features to a running machine:

1. Write the feature spec following the template in `.dev-machine/feature-spec-template.md`
2. Add the feature to `STATE.yaml` with `status: ready`
3. Run the machine -- it will pick it up on the next iteration

The machine reads STATE.yaml fresh at the start of every session. You can add, reorder, or remove features between sessions without any special procedure.

---

## Common Pitfalls

| Pitfall | What happens | Fix |
|---------|-------------|-----|
| Skipping brainstorm | Vague architecture, machine drifts | Spend the hour. The spec is the product. |
| Specs too vague | Machine makes bad choices, implements wrong thing | Real signatures, real acceptance criteria, real file paths |
| Sessions too long | Context degradation, sloppy commits | Keep `max_features_per_session` at 3-5 |
| Skipping build gate | Errors compound across sessions | Always verify build+test before committing |
| Batching state updates | Future sessions don't know what happened | Update STATE.yaml after every feature, not at session end |
| No antagonistic review | Bugs slip through | The machine runs a fresh zero-context review after each feature |
| No structural monitoring | God files, tangled modules | Enforce 10K LOC module limit, 1K line file limit |
| "Just fix this" in a human session | State diverges from reality | Use the health check recipe. Always. |

---

## Project Structure Evolution

The bundle evolved across four projects. If you're starting new, use the current pattern:

```
your-project/
+-- .dev-machine/                     # Machine artifacts (generated)
|   +-- build.yaml
|   +-- iteration.yaml
|   +-- health-check.yaml
|   +-- fix-iteration.yaml
|   +-- working-session-instructions.md
|   +-- feature-spec-template.md
+-- specs/                            # Spec tree (you write these)
|   +-- architecture.md               # The constitution
|   +-- modules/
|   |   +-- auth.md
|   |   +-- api.md
|   +-- features/
|       +-- auth/
|       |   +-- F-001-login.md
|       |   +-- F-002-session.md
|       +-- api/
|           +-- F-010-routes.md
+-- .dev-machine-assessment.md        # Admissions result
+-- .dev-machine-design.md            # Machine config
+-- STATE.yaml                        # Machine state
+-- CONTEXT-TRANSFER.md               # Session history
+-- SCRATCH.md                        # Ephemeral
+-- AGENTS.md                         # AI guardrails
+-- FEATURE-ARCHIVE.yaml             # Completed features
+-- SESSION-ARCHIVE.md               # Old session summaries
```

---

## Quick Reference

```bash
# Phase 0: Brainstorm your spec (most important step)
/brainstorm

# Phase 1: Evaluate readiness
/admissions

# Phase 2: Design the machine
/machine-design

# Phase 3: Generate artifacts
/generate-machine

# Run the machine
amplifier recipe execute .dev-machine/build.yaml

# Fix build/test failures
amplifier recipe execute .dev-machine/health-check.yaml

# Run QA (if enabled)
amplifier recipe execute .dev-machine/qa.yaml

# Add a new feature mid-run
# 1. Write spec in specs/features/<module>/F-XXX-name.md
# 2. Add to STATE.yaml with status: ready
# 3. Run the machine
```

---

## Installation

Add to your Amplifier bundle configuration:

```yaml
includes:
  - bundle: dev-machine
    source: git+https://github.com/ramparte/amplifier-bundle-dev-machine@main
```

Or run directly:

```bash
amplifier run --bundle git+https://github.com/ramparte/amplifier-bundle-dev-machine@main
```

## License

MIT
