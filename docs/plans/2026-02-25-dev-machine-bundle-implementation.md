# Dev Machine Bundle Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Build an Amplifier bundle that guides users through evaluating a problem, designing an autonomous development machine, and generating machine artifacts into their project repo.

**Architecture:** Three modes (`/admissions`, `/machine-design`, `/generate-machine`) form a hard-gated progression. Each mode is powered by a dedicated agent. The bundle includes pattern documentation extracted from word4, and real parameterized recipe templates that the generator stamps into the user's `.dev-machine/` directory. The generated machine has zero runtime dependency on this bundle.

**Tech Stack:** Amplifier bundle (markdown + YAML). No application code. Files are: bundle manifest, agent system prompts, mode definitions, context documents, and parameterized recipe templates with `{{variable}}` placeholders.

---

## Task Overview

| Group | Tasks | Description |
|-------|-------|-------------|
| 1 | 1 | Repo scaffold (bundle.md, README, directory structure) |
| 2 | 4 | Pattern context files |
| 3 | 8 | Template files (STATE.yaml, recipes, session protocol) |
| 4 | 2 | Admissions mode + agent |
| 5 | 2 | Machine design mode + agent |
| 6 | 2 | Machine generation mode + agent |
| 7 | 1 | Verification |

**Total: 20 tasks**

---

## Group 1: Repo Scaffold

### Task 1: Create bundle.md, README.md, and directory structure

**Files:**
- Create: `bundle.md`
- Create: `README.md`
- Create: `behaviors/dev-machine.yaml`
- Create: `agents/` (directory)
- Create: `modes/` (directory)
- Create: `context/` (directory)
- Create: `templates/` (directory)
- Create: `templates/recipes/` (directory)

**Step 1: Create directory structure**
Run:
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
mkdir -p agents modes context templates/recipes behaviors docs/plans
```
Expected: directories created, no output.

**Step 2: Create `bundle.md`**

Create file `bundle.md` with this exact content:

```markdown
---
bundle:
  name: dev-machine
  version: 0.1.0
  description: |
    Guides users through evaluating a problem for autonomous development,
    designing a development machine, and generating machine artifacts.
    Based on the proven pattern from word4 (278 features, 106 sessions, 5.5 days).

includes:
  - behavior: ./behaviors/dev-machine.yaml

agents:
  include:
    - admissions-advisor
    - machine-designer
    - machine-generator

context:
  include:
    - "@dev-machine:context/pattern.md"
    - "@dev-machine:context/gate-criteria.md"
---

# Dev Machine Bundle

Build autonomous development machines for your projects.

This bundle provides three modes that guide you through a hard-gated progression:

1. **`/admissions`** -- Evaluate whether your problem is suitable for an autonomous development machine. Produces a confidence-scored assessment across five gates.
2. **`/machine-design`** -- Run a founding session to design your machine: architecture spec, module boundaries, state schema, recipe configuration, and first batch of feature specs.
3. **`/generate-machine`** -- Stamp out the `.dev-machine/` directory in your project with all recipes, state files, and templates ready to run.

The generated machine lives in your project repo with zero runtime dependency on this bundle.

## The Pattern

The autonomous development machine pattern was proven by the word4 project:
- 278 features implemented autonomously
- 106 working sessions across 5.5 days
- ~89,000 lines of TypeScript
- 3,714 passing tests
- 445 git commits

The pattern works by running disposable working sessions that read state from files,
do bounded work (3-5 features), persist state, and exit. No session runs long enough
to degrade. The recipe orchestrator is lightweight -- it doesn't accumulate LLM context.
The "memory" lives in STATE.yaml and CONTEXT-TRANSFER.md.

@dev-machine:context/pattern.md
```

**Step 3: Create `behaviors/dev-machine.yaml`**

Create file `behaviors/dev-machine.yaml` with this exact content:

```yaml
# Dev Machine behavior -- mounts modes and tools
hooks:
  - module: hooks-mode
    source: git+https://github.com/microsoft/amplifier-bundle-modes@main#subdirectory=modules/hooks-mode
    config:
      search_paths:
        - "@dev-machine:modes"

tools:
  - module: tool-mode
    source: git+https://github.com/microsoft/amplifier-bundle-modes@main#subdirectory=modules/tool-mode
    config:
      gate_policy: "warn"
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
  - module: tool-search
    source: git+https://github.com/microsoft/amplifier-module-tool-search@main
  - module: tool-bash
    source: git+https://github.com/microsoft/amplifier-module-tool-bash@main
```

**Step 4: Create `README.md`**

Create file `README.md` with this exact content:

```markdown
# amplifier-bundle-dev-machine

An Amplifier bundle that helps you build autonomous development machines for your projects.

## Quick Start

1. Install the bundle in your Amplifier configuration
2. Run `/admissions` to evaluate your problem
3. Run `/machine-design` to design your machine
4. Run `/generate-machine` to stamp out the machine artifacts

## What It Does

This bundle guides you through a three-phase process:

**Phase 1: Admissions** -- Evaluates your problem across five gates (decomposability, verifiable correctness, sufficient architecture, functioning toolchain, spec quality). Each gate produces a 0-100% confidence score. Below 50% is a hard stop with remediation guidance.

**Phase 2: Machine Design** -- Runs a founding session where you design the machine: architecture spec, module boundaries, state schema, recipe configuration, working session protocol, and the first batch of feature specs.

**Phase 3: Generate Machine** -- Stamps out a `.dev-machine/` directory in your project repo containing all recipes, state files, and templates. The generated machine has zero runtime dependency on this bundle.

## Generated Output

```
your-project/
├── .dev-machine/
│   ├── build.yaml                  # Execution machine outer loop
│   ├── iteration.yaml              # Execution machine inner loop
│   ├── health-check.yaml           # Health check outer loop
│   ├── fix-iteration.yaml          # Health check fix cycle
│   ├── qa.yaml                     # QA machine outer loop (if applicable)
│   ├── qa-iteration.yaml           # QA machine inner loop (if applicable)
│   ├── working-session-instructions.md
│   └── feature-spec-template.md
├── STATE.yaml
├── CONTEXT-TRANSFER.md
└── SCRATCH.md
```

## The Pattern

Based on the word4 project: 278 features, 106 autonomous sessions, 5.5 days, ~89K LOC.

## License

MIT
```

**Step 5: Verify structure**
Run:
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
find . -type f | sort
```
Expected: All created files listed.

**Step 6: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add -A && git commit -m "feat: scaffold bundle structure with bundle.md, README, and behavior"
```

---

## Group 2: Pattern Context Files

### Task 2: Create `context/pattern.md`

**Files:**
- Create: `context/pattern.md`

This is the core pattern documentation extracted from word4. It teaches the agents (and the user) the proven autonomous development machine pattern.

**Step 1: Create `context/pattern.md`**

Create file `context/pattern.md` with this exact content:

```markdown
# The Autonomous Development Machine Pattern

## Core Insight

Two problems compound to kill autonomous AI development:

1. **Specs not factored for autonomous consumption.** Human-written specs assume context and judgment. AI agents need specs that are self-contained, complete, and machine-actionable.
2. **No resilient orchestrator that can cold-start.** Long-running AI sessions degrade. You need disposable sessions that read state from files, do bounded work, persist state, and exit.

## Eight Components

### 1. Progressive Specification Design

Three layers of specs, each gating the next:

**Layer 1 -- System Spec ("The Constitution")**
- Written once, reviewed thoroughly, rarely changed
- Defines: data model, module boundaries, technology choices, key interfaces
- Reviewed antagonistically before any implementation begins
- Prevents drift across hundreds of features

**Layer 2 -- Component Specs**
- One per major component/module
- Written just-in-time, only for the component about to be implemented
- Reviewed against Layer 1 before implementation

**Layer 3 -- Work Order Specs (Feature Specs)**
- Lightweight, machine-actionable feature specs
- Written in batches just before implementation
- Must include: interfaces, acceptance criteria, edge cases, files to modify

**Gating rule:** Layer N+1 cannot be written until Layer N is approved.

### 2. YAML State Persistence

State lives in files, not in any session's memory.

**STATE.yaml (machine-readable truth):**
- Current phase/epoch
- Every work item with status, timestamps, commit hashes
- Blockers list (presence halts the machine)
- `next_action` field (tells next session exactly what to do)
- Updated after EVERY feature, not batched

**CONTEXT-TRANSFER.md (human-readable handoff):**
- Reverse-chronological stack of session summaries
- Design decisions not in specs
- Test count progressions
- Known limitations and deferred work

**SCRATCH.md (ephemeral working memory):**
- Disposable between sessions
- Working memory for the current session

**Cardinal rule:** Never two work items without a state update between them.

### 3. Recipe-Driven Iteration

A lightweight recipe orchestrator manages heavyweight but disposable working sessions.

**Outer loop:**
1. Read state file
2. Check for blockers (halt if found)
3. Dispatch fresh working session (inner loop)
4. After session exits, re-read state
5. If healthy, loop back to step 3
6. Max N iterations before requiring human check-in

**Inner loop:**
1. Orient: read state via bash/python, extract structured data
2. Work: spawn fresh agent (zero context) with instructions + state file paths
3. Verify: run build/type checks as a structural gate
4. Post-session: re-read state, emit structured JSON for outer loop

### 4. Working Session Protocol

Each session follows a strict protocol:

**Orientation (read-only):**
1. Read STATE.yaml -- current phase, what's done, what's next
2. Read CONTEXT-TRANSFER.md -- recent decisions, context from prior sessions
3. Read architecture spec -- the constitution
4. Read relevant module spec
5. Read feature specs marked "ready"

**Work loop (per feature):**
1. Mark feature in-progress in STATE.yaml with timestamp
2. Read the full feature spec
3. Write failing tests (RED)
4. Implement minimal code (GREEN)
5. Run tests AND build -- both must pass
6. Spawn fresh sub-agent for antagonistic review (zero shared context)
7. Fix review findings, re-run tests
8. Commit with conventional message
9. Mark done in STATE.yaml with commit hash
10. Record design decisions in CONTEXT-TRANSFER.md

**Stop conditions:**
- Blocker you can't resolve
- Spec ambiguity requiring human judgment
- Tests failing after 2-3 attempts
- Losing coherence (repeating, going in circles)
- Completed 3-5 features (keep sessions bounded)

### 5. Antagonistic Review

Every implementation is reviewed by a fresh agent with no shared context.

Three levels:
1. **Spec review** (before implementation): separate agent reviews each spec
2. **Implementation review** (after each feature): fresh sub-agent reads spec + diff
3. **Epoch review** (at phase boundaries): broader structural review

### 6. Three-Tier Testing

| Tier | Scope | When | Speed |
|------|-------|------|-------|
| 1 | Unit tests per feature | After every feature | Seconds |
| 2 | Module integration tests | At epoch boundaries | Under a minute |
| 3 | System integration + visual | At phase boundaries | Minutes |

Tests are written BEFORE implementation (TDD). Both test runner and build/type checker must pass.

### 7. Health Check Machine

A dedicated fix loop for when the execution machine produces errors its own validation doesn't catch:
1. Run full build + test, capture all errors to scratch file
2. If clean: exit
3. Dispatch surgical fix session (read errors, fix them, commit)
4. Re-run build + test
5. Loop until clean or max iterations

### 8. QA Machine (Optional)

A parallel recipe loop for visual and interactive testing:
- **Visual layer:** screenshot capture + structural analysis + comparison against reference
- **Interactive layer:** browser automation interacting like a real user

Same stateless pattern: read QA state, test one area, persist findings, exit.

## When the Pattern Applies

The pattern works when:
- **Decomposable:** hundreds of small, independently testable units of work
- **Verifiable:** automated verification (tests, type checks, visual comparison)
- **Constitutionalizable:** a stable architecture document prevents drift
- **Parallelizable in time:** features implementable sequentially without human judgment on every decision

## When It Doesn't Apply

- **Research-oriented:** you don't know what to build
- **Every feature requires novel design judgment:** features don't follow patterns
- **Verification is subjective:** "correct" can't be machine-verified
- **Too small:** overhead not justified for <100 features

## Key Invariants

1. State in files, not context
2. Sessions are disposable
3. The recipe is the machine
4. Specs are for machines
5. Antagonistic review catches drift
6. Build gates are redundant on purpose
7. The QA machine is separate
8. Bounded sessions beat long sessions

## Proven Results (word4)

| Metric | Value |
|--------|-------|
| Calendar time | 5.5 days |
| Features completed | 278 |
| Working sessions | 106 |
| QA sessions | 14 |
| Git commits | 445 |
| Tests passing | 3,714 |
| Lines of code | ~89,000 |
```

**Step 2: Verify file exists**
Run:
```bash
wc -l ~/dev/ANext/amplifier-bundle-dev-machine/context/pattern.md
```
Expected: approximately 170 lines.

**Step 3: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add context/pattern.md && git commit -m "feat: add pattern context document"
```

---

### Task 3: Create `context/gate-criteria.md`

**Files:**
- Create: `context/gate-criteria.md`

**Step 1: Create `context/gate-criteria.md`**

Create file `context/gate-criteria.md` with this exact content:

```markdown
# Admissions Gate Criteria

Five gates determine whether a problem is suitable for an autonomous development machine.
Each gate produces a 0-100% confidence score.

## Scoring Rules

- **Below 50%:** Hard stop. The problem cannot proceed until this gate is remediated. Provide specific remediation guidance.
- **50-75%:** Proceed with caution. Flag the risk explicitly. The user decides whether to continue.
- **Above 75%:** Confident. Proceed.

The admissions advisor MUST be transparent about scores. No rounding up. No optimism bias.
If three or more gates are below 75%, recommend the user address them before proceeding.

---

## Gate 1: Decomposability

**Question:** Can the problem be broken into hundreds of small, independently implementable and testable units of work?

**High confidence (75-100%) signals:**
- Clear module/component boundaries already exist or are obvious
- Features within modules are independent (minimal cross-cutting concerns)
- Each feature can be specified in <2 pages
- Features follow repeating patterns (CRUD, UI components, API endpoints)
- The user can list 10+ concrete features off the top of their head

**Medium confidence (50-74%) signals:**
- Modules are identifiable but boundaries are fuzzy
- Some features have deep cross-module dependencies
- The user can describe features but they vary widely in scope
- Some features require coordinated changes across 3+ modules

**Low confidence (0-49%) signals:**
- The problem is a single monolithic algorithm or pipeline
- Features are deeply interconnected (changing one breaks many)
- Most features require novel design, not pattern application
- The user describes the work as "it all has to come together at once"
- Fewer than 50 identifiable features

**Remediation:** Identify natural boundaries. Consider breaking the problem into a smaller initial scope. Look for the "inner loop" that can be built first.

---

## Gate 2: Verifiable Correctness with Speed

**Question:** Can each unit of work be verified automatically with fast feedback?

**High confidence (75-100%) signals:**
- Established test framework exists for the tech stack
- Test execution takes seconds (unit) to minutes (integration)
- Type system catches structural errors (TypeScript, Rust, Go, etc.)
- CI/CD pipeline exists or can be trivially set up
- Clear definition of "correct" for each feature type

**Medium confidence (50-74%) signals:**
- Test framework exists but coverage is minimal
- Some features have clear correctness criteria, others are subjective
- Build/test cycle takes 2-5 minutes
- Type system is present but loosely used

**Low confidence (0-49%) signals:**
- No test framework or testing culture
- Correctness is primarily visual/subjective (design work, creative writing)
- Build/test cycle takes >10 minutes
- No type system and dynamic language with no linting
- "You have to run it and look at it to know if it's right"

**Remediation:** Set up a test framework. Add a type checker or linter. Define acceptance criteria templates. Consider if the verification gap can be addressed by a QA machine.

---

## Gate 3: Sufficient Architecture

**Question:** Is there enough architectural clarity to write a "constitution" that prevents drift across hundreds of features?

**High confidence (75-100%) signals:**
- Clear data model exists or can be defined
- Technology choices are made and rationale is understood
- Module boundaries are defined with explicit interfaces
- Key patterns are established (state management, data flow, error handling)
- The user can explain the system's architecture in 10 minutes

**Medium confidence (50-74%) signals:**
- Data model exists but has known gaps
- Some technology choices are tentative
- Module boundaries are roughly known but interfaces aren't formalized
- Some patterns are established, others are ad hoc
- "We know roughly how it works but haven't written it down"

**Low confidence (0-49%) signals:**
- No data model -- "we'll figure it out as we go"
- Technology choices are still being evaluated
- No module boundaries -- "it's all one thing right now"
- No established patterns
- The user can't explain the architecture without hand-waving

**Remediation:** Run a focused architecture session. You don't need everything -- you need enough to write a 30-50 page constitution that covers data model, module boundaries, technology choices, and key interfaces. The architecture can be progressive (design the first 3 modules well enough to start, design more later).

**Important:** Architecture does NOT need to be exhaustive. The word4 project had a 947-line architecture spec, but it was written in 1 hour and evolved. "Sufficient" means: enough to prevent drift, not enough to anticipate everything.

---

## Gate 4: Functioning Toolchain

**Question:** Do the build and test commands work? Can a fresh session run them?

**High confidence (75-100%) signals:**
- `build_command` runs and succeeds from a clean state
- `test_command` runs and reports results
- Commands are fast (<2 minutes for build, <5 minutes for full test suite)
- No manual setup required beyond initial clone
- CI/CD is configured or trivially configurable

**Medium confidence (50-74%) signals:**
- Build command works but is slow (>5 minutes)
- Test command works but only for some modules
- Some manual setup required (environment variables, local services)
- "It works on my machine" but setup isn't documented

**Low confidence (0-49%) signals:**
- No build command exists yet
- No test command exists yet
- Setup requires multiple manual steps that aren't documented
- The project hasn't been bootstrapped (no package.json, Cargo.toml, etc.)
- "We haven't set up the project yet"

**Remediation:** Bootstrap the project scaffold. This CAN be the machine's first task -- but the toolchain must work before the machine can build features. Set up: package manager, build command, test runner, type checker. Verify they run cleanly.

---

## Gate 5: Spec Quality

**Question:** Can initial feature specs be written at sufficient quality for machine consumption?

**High confidence (75-100%) signals:**
- Existing specs (PRDs, user stories) contain concrete details
- Features can be specified with: interfaces, acceptance criteria, edge cases, files to modify
- The user has domain knowledge to review specs for accuracy
- Spec writing follows a repeatable template
- A sample spec can be written and reviewed in <15 minutes

**Medium confidence (50-74%) signals:**
- Specs exist but are high-level ("add user authentication")
- Features can be described but acceptance criteria are vague
- Domain knowledge exists but isn't documented
- "We know what we want but haven't written it down precisely"

**Low confidence (0-49%) signals:**
- No specs exist -- "we're making it up as we go"
- Features can't be described without extensive discussion
- No domain expert available to review specs
- Requirements change frequently and unpredictably
- "We'll know it when we see it"

**Remediation:** Write 3-5 sample specs using the feature spec template. Have a domain expert review them. If the specs are too vague, the problem may need more product definition before a machine can build it.

---

## Assessment Output Format

The admissions advisor produces a `.dev-machine-assessment.md` file:

```
# Dev Machine Assessment

**Project:** [name]
**Date:** [ISO date]
**Overall Verdict:** PROCEED / PROCEED WITH CAUTION / NOT READY

## Gate Scores

| Gate | Score | Verdict |
|------|-------|---------|
| 1. Decomposability | XX% | PASS/CAUTION/FAIL |
| 2. Verifiable Correctness | XX% | PASS/CAUTION/FAIL |
| 3. Sufficient Architecture | XX% | PASS/CAUTION/FAIL |
| 4. Functioning Toolchain | XX% | PASS/CAUTION/FAIL |
| 5. Spec Quality | XX% | PASS/CAUTION/FAIL |

## Per-Gate Analysis

### Gate 1: Decomposability (XX%)
[Evidence and reasoning]

### Gate 2: Verifiable Correctness (XX%)
[Evidence and reasoning]

...

## Remediation Plan (if any gates < 50%)
[Specific steps to address failing gates]

## Recommended Next Steps
[What to do next based on the assessment]
```
```

**Step 2: Verify file exists**
Run:
```bash
wc -l ~/dev/ANext/amplifier-bundle-dev-machine/context/gate-criteria.md
```
Expected: approximately 180 lines.

**Step 3: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add context/gate-criteria.md && git commit -m "feat: add admissions gate criteria context"
```

---

### Task 4: Create `context/templates-reference.md`

**Files:**
- Create: `context/templates-reference.md`

**Step 1: Create `context/templates-reference.md`**

Create file `context/templates-reference.md` with this exact content:

```markdown
# Template Reference

This document explains how the recipe and file templates work. The machine generator
uses these templates to produce project-specific machine artifacts.

## Template Variable Syntax

All templates use `{{variable_name}}` for placeholders. These are replaced with
project-specific values during generation.

## Required Variables

The following variables MUST be defined during machine design. The generator will
refuse to proceed if any are missing.

| Variable | Description | Example |
|----------|-------------|---------|
| `project_name` | Short project identifier | `word4`, `my-api`, `acme-app` |
| `project_dir` | Absolute path to project root | `~/dev/my-project` |
| `state_file` | Path to STATE.yaml (relative to project root) | `./STATE.yaml` |
| `context_file` | Path to CONTEXT-TRANSFER.md (relative to project root) | `./CONTEXT-TRANSFER.md` |
| `specs_dir` | Path to specs directory (relative to project root) | `./specs` |
| `build_command` | Command to build/compile the project | `pnpm build`, `cargo build`, `make` |
| `test_command` | Command to run tests | `pnpm test`, `cargo test`, `pytest` |
| `architecture_spec` | Path to architecture spec | `./specs/architecture.md` |

## Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `type_check_command` | Separate type check command (if different from build) | same as `build_command` |
| `max_features_per_session` | Features per working session | `3-5` |
| `max_outer_iterations` | Max outer loop iterations | `50` |
| `max_fix_iterations` | Max health check iterations | `10` |
| `session_timeout` | Working session timeout (seconds) | `3600` |
| `build_timeout` | Build check timeout (seconds) | `300` |
| `module_size_threshold` | LOC threshold for module health check | `10000` |
| `file_size_threshold` | LOC threshold for file health check | `1000` |
| `qa_enabled` | Whether to generate QA machine recipes | `false` |
| `qa_url` | URL for QA testing (if qa_enabled) | none |
| `commit_prefix` | Conventional commit scope prefix | `feat` |
| `error_pattern` | Regex for build error detection | depends on language |

## Template Files

### Recipes (in `.dev-machine/`)
- `build.yaml` -- execution machine outer loop (from `dev-machine-build.yaml`)
- `iteration.yaml` -- execution machine inner loop (from `dev-machine-iteration.yaml`)
- `health-check.yaml` -- health check outer loop (from `dev-machine-health-check.yaml`)
- `fix-iteration.yaml` -- health check fix cycle (from `dev-machine-fix-iteration.yaml`)
- `qa.yaml` -- QA machine outer loop (from `dev-machine-qa.yaml`, if `qa_enabled`)
- `qa-iteration.yaml` -- QA machine inner loop (from `dev-machine-qa-iteration.yaml`, if `qa_enabled`)

### State Files (at project root)
- `STATE.yaml` -- machine-readable project state (from `templates/STATE.yaml`)
- `CONTEXT-TRANSFER.md` -- session handoff document (from `templates/CONTEXT-TRANSFER.md`)
- `SCRATCH.md` -- ephemeral working memory (from `templates/SCRATCH.md`)

### Protocol Files (in `.dev-machine/`)
- `working-session-instructions.md` -- session protocol (from `templates/working-session-instructions.md`)
- `feature-spec-template.md` -- template for writing feature specs (from `templates/feature-spec-template.md`)

## How Generation Works

1. The machine generator reads the design document (`.dev-machine-design.md`)
2. Extracts all variable values from the design
3. For each template file:
   a. Reads the template from `templates/`
   b. Replaces all `{{variable}}` placeholders with project-specific values
   c. Writes the result to the appropriate location in the project
4. Creates the `.dev-machine/` directory structure
5. Writes STATE.yaml, CONTEXT-TRANSFER.md, and SCRATCH.md at the project root
6. Reports what was generated and the command to start the machine

## Template Customization

Templates are designed to work as-is for most projects. Customization happens through variables,
not by modifying template structure. The structural patterns (orient -> work -> verify loops,
state persistence, antagonistic review) are proven and should not be changed.

Domain-specific artifacts (architecture spec, module specs, feature specs) are created during
the machine design phase, not from templates.
```

**Step 2: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add context/templates-reference.md && git commit -m "feat: add templates reference context"
```

---

### Task 5: Create `context/word4-lessons.md`

**Files:**
- Create: `context/word4-lessons.md`

**Step 1: Create `context/word4-lessons.md`**

Create file `context/word4-lessons.md` with this exact content:

```markdown
# Lessons from word4

Practical lessons from building a web-based Microsoft Word clone autonomously
in 5.5 days: 278 features, 106 sessions, ~89K LOC.

## What Failed Before word4

### wordbs: "The Enterprise Overreach" (150K LOC attempt)
- Tried to build everything at once (OT engine, canvas rendering, OOXML, mail merge)
- Drowned in its own complexity before producing anything usable
- **Lesson:** You cannot design the whole system upfront. Complexity kills front-loaded architecture.

### word3: "Ruthless Simplicity" (8K LOC, 486 tests)
- Clean architecture with immutable document model, command pattern, DOM rendering
- CRDT integration broke the working editor -- designed without CRDTs in mind
- Specs weren't factored for autonomous AI continuation
- **Lesson 1:** CRDT/collaboration strategy must be baked in from the start
- **Lesson 2:** Specs must be written for machine consumption -- complete, decomposed, independently actionable

### word4 planning: "The Unexecuted Plan"
- Right instinct (CRDT-first design with validation gates) but never executed
- Design existed only as documents with no execution mechanism
- **Lesson:** Plans without execution infrastructure are inert. You need a recipe, an orchestrator, a loop.

### amplifier-tui: "The Proven Model" (525K LOC, 38-hour session)
- 167 commits, 440 subagent spawns, 25 feature epochs
- Orchestrator + subagent pattern worked
- **But:** 13K-line god file accumulated. Context "tiredness" after 38 hours. No structured handoff.
- **Lesson:** The model works, but it breaks when a single session runs too long. Solution: disposable sessions.

## What Worked in word4

### 1. Progressive Architecture (not exhaustive)
- 947-line architecture spec written in ~1 hour
- Module specs written just-in-time, not all upfront
- Feature specs in batches of 5-15, just before implementation
- Architecture evolved but the core was stable

### 2. Disposable Sessions (106 sessions, not 1)
- Each session: read state, do 3-5 features, persist state, exit
- No session ran long enough to degrade
- Context freshness > context continuity
- Recipe orchestrator is lightweight (no LLM context accumulation)

### 3. Aggressive State Persistence
- STATE.yaml updated after EVERY feature (not batched)
- CONTEXT-TRANSFER.md grew to 6,258 lines of institutional memory
- Timestamps and commit hashes on every state transition
- Fresh session can orient in <30 seconds of file reading

### 4. TDD + Antagonistic Review
- Every feature: RED (failing tests) -> GREEN (minimal code) -> REVIEW (fresh agent)
- 3,714 tests by project end
- Both test runner AND build/type checker must pass
- Reviewer has zero shared context with builder

### 5. Health Check Machine
- Vitest (esbuild) doesn't type-check -- only tsc does
- Post-session build gate caught type errors the test runner missed
- Dedicated fix loop: detect errors, dispatch surgical fix session, verify, loop
- Every tech stack has blind spots -- identify them and add redundant gates

### 6. Structural Monitoring
- Module health check before each session: LOC per module, largest files
- Module > 10K LOC = hard stop (add blocker, refactor before continuing)
- File > 1K LOC = warning
- Prevents the god-file problem that plagued amplifier-tui

## Common Pitfalls

1. **Skipping the build gate.** Test runners may not type-check. Always run both.
2. **Batching state updates.** Update STATE.yaml after EACH feature, not at session end.
3. **Sessions too long.** Stop at 3-5 features. Context freshness matters.
4. **Specs too vague.** "Add authentication" is not a spec. Need interfaces, criteria, files.
5. **No antagonistic review.** Builder bias compounds over hundreds of features.
6. **No structural monitoring.** God files accumulate invisibly.
7. **Skipping the founding session.** The first session (architecture + initial specs) is crucial.

## Metrics to Expect

For a well-suited problem with 200+ features:
- ~50 features/day once the machine is running
- Working sessions completing 3-5 features each
- Occasional blockers requiring human judgment (1-2 per day)
- Health check runs needed every 10-20 sessions
- Feature specs written in batches of 5-15 every few phases
```

**Step 2: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add context/word4-lessons.md && git commit -m "feat: add word4 lessons context"
```

---

## Group 3: Template Files

### Task 6: Create `templates/STATE.yaml`

**Files:**
- Create: `templates/STATE.yaml`

**Step 1: Create `templates/STATE.yaml`**

Create file `templates/STATE.yaml` with this exact content:

```yaml
# =============================================================================
# {{project_name}} -- Machine State
# =============================================================================
# This file is the single source of truth for project status.
# Updated at every state transition. Any fresh session reads this to orient.
#
# Rules:
# - Update after EVERY feature (not batched)
# - Never two features without a state update between them
# - Blockers list halts the machine when present
# =============================================================================

phase: 1
phase_name: "Bootstrap"
epoch: 1
next_action: "Read architecture spec, write first batch of feature specs, begin implementation"
blockers: []

architecture_spec:
  status: "ready"    # ready | approved | needs-revision
  path: "{{architecture_spec}}"

module_specs: {}
  # Example:
  # module-name:
  #   status: "approved"
  #   path: "specs/modules/module-name.md"

features: {}
  # Example:
  # F-001-feature-name:
  #   name: "Feature Name"
  #   module: "module-name"
  #   status: "ready"          # ready | in-progress | done | blocked
  #   spec: "specs/features/module-name/F-001-feature-name.md"
  #   depends_on: []
  #   started_at: null
  #   completed_at: null
  #   commit: null

meta:
  project: "{{project_name}}"
  created: "{{timestamp}}"
  total_features_completed: 0
  last_updated: "{{timestamp}}"
  last_session: null
```

**Step 2: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add templates/STATE.yaml && git commit -m "feat: add STATE.yaml template"
```

---

### Task 7: Create `templates/CONTEXT-TRANSFER.md` and `templates/SCRATCH.md`

**Files:**
- Create: `templates/CONTEXT-TRANSFER.md`
- Create: `templates/SCRATCH.md`

**Step 1: Create `templates/CONTEXT-TRANSFER.md`**

Create file `templates/CONTEXT-TRANSFER.md` with this exact content:

```markdown
# {{project_name}} -- Context Transfer

> This file is the institutional memory of the project. Updated continuously.
> Each session reads this to understand recent decisions and context.
> Reverse-chronological: newest entries at the top.

---

## Founding Session -- Phase 1

### Architecture Decisions
- [Record architecture decisions made during the founding session here]

### Initial Module Structure
- [Record the module boundaries and their purposes]

### Technology Choices
- [Record key technology decisions and rationale]

### Known Constraints
- [Record any constraints identified during design]

### First Batch of Work
- [Record the features selected for the first phase]
```

**Step 2: Create `templates/SCRATCH.md`**

Create file `templates/SCRATCH.md` with this exact content:

```markdown
# {{project_name}} -- Scratch Pad

> Ephemeral working memory. Disposable between sessions.
> The next session may ignore this file.
> Persisted to disk for forensics if a session dies unexpectedly.

---

## Current Session Notes

[This space is for the current working session's temporary notes.]
```

**Step 3: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add templates/CONTEXT-TRANSFER.md templates/SCRATCH.md && git commit -m "feat: add CONTEXT-TRANSFER and SCRATCH templates"
```

---

### Task 8: Create `templates/working-session-instructions.md`

**Files:**
- Create: `templates/working-session-instructions.md`

This is generalized from word4's `specs/working-session-instructions.md`, replacing all word4-specific references with template variables.

**Step 1: Create `templates/working-session-instructions.md`**

Create file `templates/working-session-instructions.md` with this exact content:

```markdown
# Working Session Instructions

> Read this file at the start of every working session.
> You are a stateless agent. Everything you need to know is in the files.

## Your Role

You are a **working session** of the {{project_name}} development machine. You were spawned
by the meta-recipe to do a bounded unit of work. You start with zero context from previous
sessions. Your job is to:

1. Read state from files
2. Do a batch of work
3. Persist all state back to files
4. Exit cleanly

The next session will pick up exactly where you left off -- but only if you wrote
everything down.

## Orientation Procedure

Execute these steps in order before doing any work:

1. **Read `{{state_file}}`** -- Understand the current phase, what's done, what's
   next, and whether there are blockers.
2. **Read `{{context_file}}`** -- Understand recent decisions, context from
   prior sessions, and any known issues.
3. **Read `{{architecture_spec}}`** -- The overall system architecture. This is
   the constitution. All implementation must conform to it.
4. **Read the module spec** for the module you're working on. Check
   `{{state_file}}` `module_specs` to see which modules have specs written.
5. **Read feature specs** marked `ready` in `{{state_file}}` `features` section.

After orientation, you should know:
- What phase the project is in
- What work has been completed
- What work is ready to start
- What decisions have been made
- What the relevant specs say

## Module Health Check (Before Starting Work)

Before implementing features, check the health of the module you're about to work on.

**Thresholds:**
- Module > {{module_size_threshold}} LOC: DO NOT add features. Create a refactoring plan and add a blocker to {{state_file}}.
- Any file > {{file_size_threshold}} lines: Flag for decomposition. Can still add features but note it in {{context_file}}.

## Work Procedure

For each feature or task you pick up:

### 1. Mark In-Progress

Update `{{state_file}}` before starting any implementation:

```yaml
features:
  <feature-name>:
    status: "in-progress"
    started_at: "<ISO 8601 timestamp>"
```

### 2. Read the Feature Spec

Read the full feature specification. Understand the acceptance criteria, interfaces,
and constraints before writing any code.

### 3. Write Failing Tests (RED)

- Write tests that describe the expected behavior
- Run `{{test_command}}` to confirm they fail
- Tests should fail because the feature doesn't exist yet, not because of typos

### 4. Implement (GREEN)

- Write the minimal code to make the tests pass
- Do not add anything beyond what the spec requires

### 5. Verify BOTH Tests and Build

- Run `{{test_command}}` to confirm tests pass
- Run `{{build_command}}` to confirm compilation/type-checking is clean
- BOTH must pass before proceeding
- Do NOT skip the build step -- test runners may not catch all errors

### 6. Antagonistic Review

- Spawn a fresh sub-agent for review (delegate with context_depth="none")
- Provide it with: the feature spec, the diff of your changes, and the test results
- Ask it to find problems: spec violations, missing edge cases, incorrect types,
  untested code paths, naming inconsistencies
- Fix any legitimate issues it identifies
- Re-run tests after fixes

### 7. Commit

```bash
git add -A
git commit -m "{{commit_prefix}}(<module>): <feature-name>"
```

### 8. Mark Done

Update `{{state_file}}` after the commit:

```yaml
features:
  <feature-name>:
    status: "done"
    started_at: "<original timestamp>"
    completed_at: "<ISO 8601 timestamp>"
    commit: "<commit hash>"
```

Also update `meta.total_features_completed` and `meta.last_updated`.

### 9. Record Decisions

If you made any design decisions not already covered by the specs, immediately
record them in `{{context_file}}` under "Recent Decisions".

## State Persistence Rules

These are cardinal rules. Violating them breaks the development machine.

1. **Update {{state_file}} BEFORE starting work** -- Mark the feature as `in-progress`.
2. **Update {{state_file}} AFTER completing work** -- Mark the feature as `done` with commit hash.
3. **Never work on two features without a state update between them.**
4. **Design decisions not in spec -> record in {{context_file}} immediately.**
5. **Update `meta.last_updated` and `meta.last_session`** after each feature completion.

## When to Stop

Stop your session gracefully when any of these conditions are true:

- **Blocker you can't resolve** -- Add to `{{state_file}}` `blockers` list.
- **Spec ambiguity requiring human judgment** -- Add blocker.
- **Tests failing after 2-3 attempts** -- Something is wrong. Stop and document.
- **Repeating yourself or losing coherence** -- Stop immediately.
- **Completed {{max_features_per_session}} features** -- Stop even if more are ready.

When stopping:
1. Commit any completed work
2. Update {{state_file}} with correct statuses
3. Update {{context_file}} with summary
4. Exit

## What NOT to Do

- Don't modify modules you're not working on (unless spec authorizes it)
- Don't add unspecified features
- Don't skip tests
- Don't skip antagonistic review
- Don't batch state updates to the end
- Don't assume context from a "previous conversation" -- you have none
- Don't modify specs without authorization
```

**Step 2: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add templates/working-session-instructions.md && git commit -m "feat: add working session instructions template"
```

---

### Task 9: Create `templates/feature-spec-template.md`

**Files:**
- Create: `templates/feature-spec-template.md`

**Step 1: Create `templates/feature-spec-template.md`**

Create file `templates/feature-spec-template.md` with this exact content:

```markdown
# Feature Spec Template

> Use this template when writing feature specs for the development machine.
> Every field must be filled in. The machine implements specs literally.

---

# F-XXX: [Feature Name]

## 1. Overview

**Module:** [which module this feature belongs to]
**Priority:** [P0/P1/P2]
**Depends on:** [list feature IDs this depends on, or "none"]

[2-3 sentences: what this feature does and why it's needed]

## 2. Requirements

### Interfaces

```
[TypeScript/Python/Rust/etc. signatures for any new or modified interfaces]
[Include types, function signatures, class definitions]
```

### Behavior

- [Concrete behavior rule 1]
- [Concrete behavior rule 2]
- [Keyboard shortcuts, API responses, state transitions, etc.]

## 3. Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| AC-1 | [Specific, testable criterion] | [How to verify: unit test, integration test, manual check] |
| AC-2 | [Specific, testable criterion] | [How to verify] |
| AC-3 | [Specific, testable criterion] | [How to verify] |

## 4. Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| [Edge case 1] | [What should happen] |
| [Edge case 2] | [What should happen] |

## 5. Files to Create/Modify

| File | Action | Contents |
|------|--------|----------|
| `path/to/new-file.ts` | Create | [Description of what this file contains] |
| `path/to/existing.ts` | Modify | [Description of changes] |
| `tests/path/to/test.ts` | Create | [Tests for this feature] |

## 6. Dependencies

- [Package/library dependencies needed]
- [Or "No new dependencies"]

## 7. Notes

- [Implementation caveats]
- [Future work deferred]
- [Warnings about gotchas]
```

**Step 2: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add templates/feature-spec-template.md && git commit -m "feat: add feature spec template"
```

---

### Task 10: Create execution machine recipe templates (`templates/recipes/dev-machine-build.yaml` and `templates/recipes/dev-machine-iteration.yaml`)

**Files:**
- Create: `templates/recipes/dev-machine-build.yaml`
- Create: `templates/recipes/dev-machine-iteration.yaml`

These are generalized from `word4-build.yaml` and `word4-session-iteration.yaml`, preserving the exact structural patterns but replacing all word4-specific references with template variables.

**Step 1: Create `templates/recipes/dev-machine-build.yaml`**

Create file `templates/recipes/dev-machine-build.yaml` with this exact content:

```yaml
# =============================================================================
# {{project_name}}-build: The Development Machine Outer Loop
# =============================================================================
#
# This is the meta-recipe -- the "machine" itself. It reads project state,
# dispatches fresh working sessions, and loops until the project is complete
# or a blocker is hit.
#
# Each working session starts with zero context, reads STATE.yaml and
# CONTEXT-TRANSFER.md, does a bounded batch of work ({{max_features_per_session}} features),
# persists all state back to files, and exits.
#
# Usage:
#   amplifier recipe execute .dev-machine/build.yaml
#
# =============================================================================

name: "{{project_name}}-build"
description: "Outer orchestration loop for the {{project_name}} development machine. Reads state, dispatches working sessions, persists progress across context windows."
version: "1.0.0"
author: "{{project_name}} Development Machine"
tags: ["orchestration", "meta-recipe", "development-machine", "{{project_name}}"]

context:
  state_file: "{{state_file}}"
  context_file: "{{context_file}}"
  specs_dir: "{{specs_dir}}"
  status: "healthy"
  session_count: "0"

steps:
  # ---------------------------------------------------------------------------
  # Step 1: Read STATE.yaml and check for blockers
  # ---------------------------------------------------------------------------
  - id: "read-state"
    type: "bash"
    command: |
      python3 << 'PYEOF'
      import json, yaml
      try:
          with open("{{state_file}}") as f:
              state = yaml.safe_load(f)
          blockers = state.get("blockers", [])
          result = {
              "phase": state.get("phase", 0),
              "phase_name": state.get("phase_name", "unknown"),
              "epoch": state.get("epoch", 0),
              "next_action": state.get("next_action", ""),
              "blocker_count": len(blockers),
              "blockers": blockers,
              "status": "blocked" if blockers else "healthy"
          }
          print(json.dumps(result))
      except Exception as e:
          print(json.dumps({
              "status": "blocked",
              "blockers": ["Failed to read STATE.yaml: " + str(e)],
              "blocker_count": 1
          }))
      PYEOF
    output: "initial_state"
    parse_json: true

  # ---------------------------------------------------------------------------
  # Step 2: If blockers exist, print them and fail
  # ---------------------------------------------------------------------------
  - id: "check-health"
    type: "bash"
    condition: "{{initial_state.status}} == 'blocked'"
    command: |
      echo "BLOCKED: Cannot proceed. Blockers found:"
      printf '%s\n' '{{initial_state.blockers}}'
      echo ""
      printf '%s\n' "Resolve blockers in {{state_file}} and re-run."
      exit 1
    on_error: "fail"

  # ---------------------------------------------------------------------------
  # Step 3: Main work loop -- calls sub-recipe per iteration
  #
  # Each iteration: orient (read state) -> working session -> post-session check.
  # Loop exits when status becomes "blocked" or max iterations reached.
  # ---------------------------------------------------------------------------
  - id: "work-loop"
    type: "recipe"
    recipe: "./.dev-machine/iteration.yaml"
    context:
      state_file: "{{state_file}}"
      context_file: "{{context_file}}"
      specs_dir: "{{specs_dir}}"
      session_count: "{{session_count}}"
    output: "iteration_result"
    parse_json: true
    timeout: 4200
    on_error: "continue"
    while_condition: "{{status}} == 'healthy'"
    max_while_iterations: {{max_outer_iterations}}
    break_when: "{{status}} != 'healthy'"
    update_context:
      status: "{{iteration_result.iteration_result.status}}"
      session_count: "{{iteration_result.iteration_result.session_count}}"

  # ---------------------------------------------------------------------------
  # Step 4: Final summary
  # ---------------------------------------------------------------------------
  - id: "final-summary"
    type: "bash"
    command: |
      echo ""
      echo "========================================"
      echo "  {{project_name}} Development Machine -- Run Complete"
      echo "========================================"
      echo ""
      echo "  Sessions completed: {{session_count}}"
      echo "  Final status:       {{status}}"
      echo ""
      if [ "{{status}}" = "blocked" ]; then
        echo "  Stopped: BLOCKERS detected"
        echo "  Check {{state_file}} for blocker details."
      else
        echo "  Stopped: work loop exit (max iterations or no more work)"
      fi
      echo ""
      echo "  State file:    {{state_file}}"
      echo "  Context file:  {{context_file}}"
      echo ""
      echo "========================================"
    output: "summary"
```

**Step 2: Create `templates/recipes/dev-machine-iteration.yaml`**

Create file `templates/recipes/dev-machine-iteration.yaml` with this exact content:

```yaml
# =============================================================================
# {{project_name}}-session-iteration: Single iteration of the development machine loop
# =============================================================================
#
# Called by build.yaml in a while loop. Each invocation:
#   1. Reads STATE.yaml to orient (bash)
#   2. Dispatches a fresh working session (agent)
#   3. Runs build/type-check as a structural gate (bash)
#   4. Reads STATE.yaml again to check for blockers (bash)
#
# Returns structured JSON so the outer loop can update_context.
#
# =============================================================================

name: "{{project_name}}-session-iteration"
description: "Single iteration of the {{project_name}} development machine -- orient, work, check health."
version: "1.0.0"
tags: ["{{project_name}}", "iteration", "working-session"]

context:
  state_file: "{{state_file}}"
  context_file: "{{context_file}}"
  specs_dir: "{{specs_dir}}"
  session_count: "0"

steps:
  # Step 1: Orient -- read STATE.yaml before dispatching the working session
  - id: "orient"
    type: "bash"
    command: |
      python3 << 'PYEOF'
      import json, yaml
      try:
          with open("{{state_file}}") as f:
              state = yaml.safe_load(f)
          blockers = state.get("blockers", [])
          print(json.dumps({
              "phase": state.get("phase", 0),
              "phase_name": state.get("phase_name", "unknown"),
              "epoch": state.get("epoch", 0),
              "next_action": state.get("next_action", ""),
              "status": "blocked" if blockers else "healthy"
          }))
      except Exception as e:
          print(json.dumps({"status": "blocked", "error": str(e)}))
      PYEOF
    output: "orient_state"
    parse_json: true

  # Step 2: Dispatch fresh working session
  - id: "working-session"
    agent: "self"
    prompt: |
      You are a WORKING SESSION of the {{project_name}} development machine.
      You start with ZERO prior context. Your job: read state, do work, persist state, exit.

      START BY READING THESE FILES (in this order):
      1. {{state_file}} -- current phase, what's done, what's next
      2. {{context_file}} -- recent decisions and handoff context
      3. .dev-machine/working-session-instructions.md -- your detailed operating procedure

      THEN READ THE RELEVANT SPECS:
      4. {{architecture_spec}} -- the overall architecture (always read this)
      5. Module specs for whatever module you're working on (check {{state_file}} module_specs)
      6. Feature specs marked "ready" in {{state_file}} features section

      YOUR MISSION THIS SESSION:
      - Determine what work is ready from {{state_file}} (next_action + ready features)
      - Pick the next batch of ready work ({{max_features_per_session}} features or the current next_action)
      - For each piece of work:
        * Update {{state_file}} to mark it in-progress with timestamp
        * Write failing tests first (TDD)
        * Implement minimal code to pass tests
        * Run: {{test_command}}
        * Run: {{build_command}}
        * BOTH must pass before proceeding.
        * Spawn a fresh sub-agent for antagonistic review (give it the spec + your diff)
        * Fix any review issues found
        * Commit: {{commit_prefix}}(<module>): <description>
        * Update {{state_file}} to mark it done with commit hash
      - Update {{context_file}} with decisions made and work completed

      IF BLOCKED: add blocker to {{state_file}} blockers list, update {{context_file}}, stop.
      IF DEGRADATION DETECTED (repeating yourself, losing coherence): commit work, update state, stop.

      You are one session in a long chain. Persist everything to files.
      What you don't write down is lost forever.
    output: "session_result"
    timeout: {{session_timeout}}

  # Step 3: Structural build gate -- catches errors the agent may have missed
  - id: "build-check"
    type: "bash"
    command: |
      cd {{project_dir}}
      echo "=== POST-SESSION BUILD CHECK ==="
      if {{build_command}} 2>&1; then
        echo '{"build_status": "clean"}'
      else
        echo "BUILD FAILED -- errors detected after working session"
        echo "Adding blocker to {{state_file}}..."
        python3 -c "import yaml,datetime;f=open('{{state_file}}');s=yaml.safe_load(f);f.close();b=s.get('blockers') or [];b.append({'description':'{{build_command}} failed after working session','since':datetime.datetime.now().isoformat(),'severity':'high'});s['blockers']=b;f=open('{{state_file}}','w');yaml.dump(s,f,default_flow_style=False,sort_keys=False);f.close()"
        echo '{"build_status": "failed"}'
      fi
    output: "build_result"
    timeout: {{build_timeout}}

  # Step 4: Post-session -- re-read STATE.yaml to check health
  - id: "post-session"
    type: "bash"
    command: |
      python3 << 'PYEOF'
      import json, yaml
      try:
          with open("{{state_file}}") as f:
              state = yaml.safe_load(f)
          blockers = state.get("blockers", [])
          session_num = int("{{session_count}}") + 1
          print(json.dumps({
              "status": "blocked" if blockers else "healthy",
              "session_count": str(session_num),
              "next_action": state.get("next_action", ""),
              "total_features": state.get("meta", {}).get("total_features_completed", 0)
          }))
      except Exception as e:
          print(json.dumps({"status": "blocked", "session_count": "{{session_count}}"}))
      PYEOF
    output: "iteration_result"
    parse_json: true
```

**Step 3: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add templates/recipes/dev-machine-build.yaml templates/recipes/dev-machine-iteration.yaml && git commit -m "feat: add execution machine recipe templates (build + iteration)"
```

---

### Task 11: Create health check recipe templates (`templates/recipes/dev-machine-health-check.yaml` and `templates/recipes/dev-machine-fix-iteration.yaml`)

**Files:**
- Create: `templates/recipes/dev-machine-health-check.yaml`
- Create: `templates/recipes/dev-machine-fix-iteration.yaml`

Generalized from `word4-health-check.yaml` and `word4-fix-iteration.yaml`.

**Step 1: Create `templates/recipes/dev-machine-health-check.yaml`**

Create file `templates/recipes/dev-machine-health-check.yaml` with this exact content:

```yaml
# =============================================================================
# {{project_name}}-health-check: Systematic Build/Test Error Detection and Fixing
# =============================================================================
#
# Complementary to build.yaml (which builds features), this recipe FIXES things.
# It runs build and test, captures errors, spawns sessions to fix them, and
# loops until the codebase is clean.
#
# Flow:
#   1. Run build + test, capture output
#   2. If both pass clean: done, exit successfully
#   3. If errors exist: write findings to SCRATCH.md, dispatch fix iteration
#   4. Loop back to step 1 (max {{max_fix_iterations}} iterations)
#
# Usage:
#   amplifier recipe execute .dev-machine/health-check.yaml
#
# =============================================================================

name: "{{project_name}}-health-check"
description: "Systematic health check that detects build errors and test failures, spawns fixing sessions, and loops until the codebase is clean."
version: "1.0.0"
author: "{{project_name}} Health Check Machine"
tags: ["health-check", "qa", "build", "test", "{{project_name}}"]

context:
  status: "checking"
  iteration: "0"
  project_dir: "{{project_dir}}"

recursion:
  max_depth: 5
  max_total_steps: 200

steps:
  # ---------------------------------------------------------------------------
  # Step 1: Initial health check -- run build + test, write SCRATCH.md
  # ---------------------------------------------------------------------------
  - id: "initial-check"
    type: "bash"
    command: |
      cd {{project_dir}}
      echo "=== HEALTH CHECK -- INITIAL SCAN ==="

      # Run build and capture output
      BUILD_OUTPUT=$({{build_command}} 2>&1) || true
      BUILD_EXIT=$?

      # Run tests and capture output
      TEST_OUTPUT=$({{test_command}} 2>&1) || true
      TEST_EXIT=$?

      # Write findings to SCRATCH.md for the fixing session
      cat > SCRATCH.md << 'SCRATCH_HEADER'
      # Health Check Findings

      SCRATCH_HEADER

      echo "## Build Status" >> SCRATCH.md
      if [ "$BUILD_EXIT" -eq 0 ]; then
        echo "Build: CLEAN" >> SCRATCH.md
      else
        echo "Build: FAILED" >> SCRATCH.md
        echo "" >> SCRATCH.md
        echo "### Build Errors" >> SCRATCH.md
        echo '```' >> SCRATCH.md
        echo "$BUILD_OUTPUT" | tail -50 >> SCRATCH.md
        echo '```' >> SCRATCH.md
      fi

      echo "" >> SCRATCH.md
      echo "## Test Status" >> SCRATCH.md
      if [ "$TEST_EXIT" -eq 0 ]; then
        echo "Tests: PASSING" >> SCRATCH.md
      else
        echo "Tests: FAILING" >> SCRATCH.md
        echo "" >> SCRATCH.md
        echo "### Test Output (last 80 lines)" >> SCRATCH.md
        echo '```' >> SCRATCH.md
        echo "$TEST_OUTPUT" | tail -80 >> SCRATCH.md
        echo '```' >> SCRATCH.md
      fi

      # Determine overall status
      if [ "$BUILD_EXIT" -eq 0 ] && [ "$TEST_EXIT" -eq 0 ]; then
        echo '{"status": "clean", "build_errors": "0", "test_status": "passing"}'
      else
        echo "{\"status\": \"needs-fixing\", \"build_exit\": \"$BUILD_EXIT\", \"test_exit\": \"$TEST_EXIT\"}"
      fi
    output: "initial_result"
    parse_json: true
    timeout: {{build_timeout}}
    on_error: "continue"

  # ---------------------------------------------------------------------------
  # Step 2: Early exit if already clean
  # ---------------------------------------------------------------------------
  - id: "check-if-clean"
    type: "bash"
    condition: "{{initial_result.status}} == 'clean'"
    command: |
      echo "=== ALL CLEAN ==="
      echo "Build passes, tests pass. Codebase is healthy."
      echo '{"status": "done", "iteration": "0"}'
    output: "clean_signal"
    parse_json: true

  # ---------------------------------------------------------------------------
  # Step 3: Fix loop -- calls sub-recipe per iteration until clean or max
  # ---------------------------------------------------------------------------
  - id: "fix-loop"
    type: "recipe"
    recipe: "./.dev-machine/fix-iteration.yaml"
    context:
      project_dir: "{{project_dir}}"
      iteration: "{{iteration}}"
    output: "fix_result"
    parse_json: true
    timeout: 2400
    on_error: "continue"
    while_condition: "{{status}} == 'checking'"
    max_while_iterations: {{max_fix_iterations}}
    break_when: "{{status}} != 'checking'"
    update_context:
      status: "{{fix_result.verify_result.status}}"
      iteration: "{{fix_result.verify_result.iteration}}"

  # ---------------------------------------------------------------------------
  # Step 4: Final report
  # ---------------------------------------------------------------------------
  - id: "final-report"
    type: "bash"
    command: |
      echo "=== HEALTH CHECK COMPLETE ==="
      echo "Final status: {{status}}"
      echo "Iterations used: {{iteration}}"
      cat {{project_dir}}/SCRATCH.md 2>/dev/null || echo "(no SCRATCH.md)"
    output: "final_output"
```

**Step 2: Create `templates/recipes/dev-machine-fix-iteration.yaml`**

Create file `templates/recipes/dev-machine-fix-iteration.yaml` with this exact content:

```yaml
# =============================================================================
# {{project_name}}-fix-iteration: Single fix cycle for the health check loop
# =============================================================================
#
# Called by health-check.yaml in a while loop. Each invocation:
#   1. Reads SCRATCH.md to understand current errors (bash)
#   2. Spawns a fresh agent session to fix them (agent: self)
#   3. Re-runs build + test to verify and updates SCRATCH.md (bash)
#
# Returns JSON so the outer loop can update_context and decide whether
# to continue looping or exit.
#
# =============================================================================

name: "{{project_name}}-fix-iteration"
description: "Single iteration of the health check fix cycle -- read errors, fix them, verify."
version: "1.0.0"
tags: ["{{project_name}}", "health-check", "fix-iteration"]

context:
  project_dir: "{{project_dir}}"
  iteration: "0"

steps:
  # ---------------------------------------------------------------------------
  # Step 1: Read current errors from SCRATCH.md
  # ---------------------------------------------------------------------------
  - id: "read-errors"
    type: "bash"
    command: |
      cd {{project_dir}}
      ITER=$(({{iteration}} + 1))
      echo "=== FIX ITERATION $ITER ==="

      if [ -f SCRATCH.md ]; then
        SCRATCH_CONTENT=$(cat SCRATCH.md)
      else
        SCRATCH_CONTENT="No SCRATCH.md found. Running fresh check..."
      fi

      # Also grab raw build errors for structured data
      BUILD_OUTPUT=$({{build_command}} 2>&1) || true
      BUILD_ERRORS=$(echo "$BUILD_OUTPUT" | tail -30 | tr '\n' ' ' | sed 's/"/\\"/g')

      echo "{\"iteration\": \"$ITER\", \"scratch\": \"see SCRATCH.md\", \"build_errors_summary\": \"$BUILD_ERRORS\"}"
    output: "error_context"
    parse_json: true
    timeout: {{build_timeout}}
    on_error: "continue"

  # ---------------------------------------------------------------------------
  # Step 2: Fresh agent session to fix the errors
  # ---------------------------------------------------------------------------
  - id: "fix-session"
    agent: "self"
    prompt: |
      You are a HEALTH CHECK FIX SESSION for the {{project_name}} project.
      Working directory: {{project_dir}}
      This is fix iteration {{error_context.iteration}}.

      YOUR MISSION: Fix all build errors and test failures.

      START BY READING:
      1. ./SCRATCH.md -- contains the specific errors found by the health check
      2. The specific files mentioned in the error output

      FIXING STRATEGY:
      - Parse each error from SCRATCH.md
      - Group errors by file
      - For each file:
        * Read the file
        * Fix ALL errors in that file at once
        * After fixing each file, run: {{build_command}} 2>&1 | tail -20
        * Verify the errors in that file are resolved before moving on

      VALIDATION:
      - After all files are fixed, run: {{build_command}} 2>&1
      - Then run: {{test_command}} 2>&1
      - If build still fails, keep fixing (iterate on remaining errors)
      - If tests fail, read the test output and fix the failures

      COMMIT:
      - Once build and tests pass, commit:
        git add -A && git commit -m "fix: resolve build errors and test failures (health-check iteration {{error_context.iteration}})"

      UPDATE SCRATCH.md:
      - Append a section: "## Iteration {{error_context.iteration}} -- Fixes Applied"
      - List what you fixed and the final build/test status

      IMPORTANT:
      - Do NOT add new features. Only fix existing errors.
      - Do NOT refactor unless required to fix an error.
      - Be surgical -- minimal changes to resolve each error.
      - If you cannot fix an error, document it in SCRATCH.md as a known issue.
    output: "fix_result"
    timeout: 1800

  # ---------------------------------------------------------------------------
  # Step 3: Verify -- re-run build + test, update SCRATCH.md, output status
  # ---------------------------------------------------------------------------
  - id: "verify"
    type: "bash"
    command: |
      cd {{project_dir}}
      ITER={{error_context.iteration}}
      echo "=== POST-FIX VERIFICATION (iteration $ITER) ==="

      # Run build
      BUILD_OUTPUT=$({{build_command}} 2>&1) || true
      BUILD_EXIT=$?

      # Run tests
      TEST_OUTPUT=$({{test_command}} 2>&1) || true
      TEST_EXIT=$?

      # Update SCRATCH.md with verification results
      echo "" >> SCRATCH.md
      echo "## Verification After Iteration $ITER" >> SCRATCH.md
      echo "- Build exit code: $BUILD_EXIT" >> SCRATCH.md
      echo "- Test exit code: $TEST_EXIT" >> SCRATCH.md

      if [ "$BUILD_EXIT" -ne 0 ]; then
        echo "" >> SCRATCH.md
        echo "### Remaining Build Errors" >> SCRATCH.md
        echo '```' >> SCRATCH.md
        echo "$BUILD_OUTPUT" | tail -30 >> SCRATCH.md
        echo '```' >> SCRATCH.md
      fi

      # Output status for the outer loop
      if [ "$BUILD_EXIT" -eq 0 ] && [ "$TEST_EXIT" -eq 0 ]; then
        echo "{\"status\": \"done\", \"iteration\": \"$ITER\"}"
      elif [ "$ITER" -ge {{max_fix_iterations}} ]; then
        echo "{\"status\": \"max-iterations\", \"iteration\": \"$ITER\"}"
      else
        echo "{\"status\": \"checking\", \"iteration\": \"$ITER\"}"
      fi
    output: "verify_result"
    parse_json: true
    timeout: {{build_timeout}}
    on_error: "continue"
```

**Step 3: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add templates/recipes/dev-machine-health-check.yaml templates/recipes/dev-machine-fix-iteration.yaml && git commit -m "feat: add health check recipe templates (health-check + fix-iteration)"
```

---

### Task 12: Create QA machine recipe templates (`templates/recipes/dev-machine-qa.yaml` and `templates/recipes/dev-machine-qa-iteration.yaml`)

**Files:**
- Create: `templates/recipes/dev-machine-qa.yaml`
- Create: `templates/recipes/dev-machine-qa-iteration.yaml`

Generalized from `word4-qa.yaml` and `word4-qa-iteration.yaml`. These are optional and only generated when `qa_enabled` is true.

**Step 1: Create `templates/recipes/dev-machine-qa.yaml`**

Create file `templates/recipes/dev-machine-qa.yaml` with this exact content:

```yaml
# =============================================================================
# {{project_name}}-qa: The QA Machine Outer Loop
# =============================================================================
#
# Parallel QA machine that tests the running application:
#   Layer A (Visual Fidelity): Captures screenshots, analyzes layout, compares
#     against reference, fixes discrepancies.
#   Layer B (Interactive Correctness): Uses browser automation to interact with
#     the app (type, click, verify), fixes broken interactions.
#
# Each QA session starts with zero context, reads QA-STATE.yaml and
# QA-CONTEXT-TRANSFER.md, tests one area, persists state, and exits.
#
# Only generated when qa_enabled is true during machine design.
#
# Usage:
#   amplifier recipe execute .dev-machine/qa.yaml
#
# =============================================================================

name: "{{project_name}}-qa"
description: "QA machine: visual fidelity and interactive correctness testing. Reads state, dispatches testing sessions, persists progress across context windows."
version: "1.0.0"
author: "{{project_name}} QA Machine"
tags: ["qa", "testing", "visual-fidelity", "interactive-testing", "{{project_name}}"]

context:
  project_dir: "{{project_dir}}"
  qa_state_file: "{{qa_state_file}}"
  qa_context_file: "{{qa_context_file}}"
  status: "testing"
  session_count: "0"

steps:
  # ---------------------------------------------------------------------------
  # Step 1: Read QA-STATE.yaml and check for blockers
  # ---------------------------------------------------------------------------
  - id: "read-qa-state"
    type: "bash"
    command: |
      cd {{project_dir}}
      echo "=== QA MACHINE STARTING ==="
      python3 << 'PYEOF'
      import json, yaml
      try:
          with open("{{qa_state_file}}") as f:
              state = yaml.safe_load(f)
          blockers = state.get("blockers", [])
          result = {
              "phase": state.get("phase", "visual-fidelity"),
              "epoch": state.get("epoch", 0),
              "blocker_count": len(blockers),
              "blockers": blockers,
              "next_action": state.get("next_action", ""),
              "status": "blocked" if blockers else "testing"
          }
          print(json.dumps(result))
      except Exception as e:
          print(json.dumps({
              "status": "blocked",
              "blockers": ["Failed to read QA state: " + str(e)],
              "blocker_count": 1
          }))
      PYEOF
    output: "initial_state"
    parse_json: true

  # ---------------------------------------------------------------------------
  # Step 2: If blockers exist, print them and fail
  # ---------------------------------------------------------------------------
  - id: "check-blockers"
    type: "bash"
    condition: "{{initial_state.status}} == 'blocked'"
    command: |
      echo "BLOCKED: Cannot proceed. Blockers found:"
      echo "{{initial_state.blockers}}"
      echo ""
      echo "Resolve blockers in {{qa_state_file}} and re-run."
      exit 1
    on_error: "fail"

  # ---------------------------------------------------------------------------
  # Step 3: Main QA loop -- calls sub-recipe per iteration
  # ---------------------------------------------------------------------------
  - id: "qa-loop"
    type: "recipe"
    recipe: "./.dev-machine/qa-iteration.yaml"
    context:
      project_dir: "{{project_dir}}"
      qa_state_file: "{{qa_state_file}}"
      qa_context_file: "{{qa_context_file}}"
      session_count: "{{session_count}}"
    output: "iteration_result"
    parse_json: true
    timeout: 2400
    on_error: "continue"
    while_condition: "{{status}} == 'testing'"
    max_while_iterations: 20
    break_when: "{{status}} != 'testing'"
    update_context:
      status: "{{iteration_result.post_result.status}}"
      session_count: "{{iteration_result.post_result.session_count}}"

  # ---------------------------------------------------------------------------
  # Step 4: Final QA summary
  # ---------------------------------------------------------------------------
  - id: "final-summary"
    type: "bash"
    command: |
      cd {{project_dir}}
      echo ""
      echo "========================================"
      echo "  {{project_name}} QA Machine -- Run Complete"
      echo "========================================"
      echo ""
      echo "  Sessions completed: {{session_count}}"
      echo "  Final status:       {{status}}"
      echo ""
      echo "  QA state: {{qa_state_file}}"
      echo ""
      echo "========================================"
    output: "summary"
```

**Step 2: Create `templates/recipes/dev-machine-qa-iteration.yaml`**

Create file `templates/recipes/dev-machine-qa-iteration.yaml` with this exact content:

```yaml
# =============================================================================
# {{project_name}}-qa-iteration: Single iteration of the QA machine loop
# =============================================================================
#
# Called by qa.yaml in a while loop. Each invocation:
#   1. Reads QA-STATE.yaml to orient -- find the next untested area (bash)
#   2. Dispatches a fresh QA session to test/fix it (agent: self)
#   3. Re-reads QA-STATE.yaml to check progress and decide next step (bash)
#
# Returns structured JSON so the outer loop can update_context.
#
# =============================================================================

name: "{{project_name}}-qa-iteration"
description: "Single iteration of the {{project_name}} QA machine -- orient, test one area, fix if broken, verify."
version: "1.0.0"
tags: ["{{project_name}}", "qa", "iteration", "testing"]

context:
  project_dir: "{{project_dir}}"
  qa_state_file: "{{qa_state_file}}"
  qa_context_file: "{{qa_context_file}}"
  session_count: "0"

steps:
  # ---------------------------------------------------------------------------
  # Step 1: Orient -- read QA-STATE.yaml, find next untested area
  # ---------------------------------------------------------------------------
  - id: "orient"
    type: "bash"
    command: |
      cd {{project_dir}}
      SESSION=$(({{session_count}} + 1))
      echo "=== QA ITERATION $SESSION ==="

      python3 << 'PYEOF'
      import json, yaml, sys
      try:
          with open("{{qa_state_file}}") as f:
              state = yaml.safe_load(f)
          test_areas = state.get("test_areas", {})
          for name, info in test_areas.items():
              if info.get("status") in ("not-tested", "failing"):
                  print(json.dumps({
                      "next_test": name,
                      "status": "testing",
                      "all_areas": list(test_areas.keys())
                  }))
                  sys.exit(0)
          # All areas tested
          print(json.dumps({
              "next_test": None,
              "status": "done"
          }))
      except Exception as e:
          print(json.dumps({"status": "blocked", "error": str(e)}))
      PYEOF
    output: "orient_state"
    parse_json: true

  # ---------------------------------------------------------------------------
  # Step 2: Fresh QA agent session -- test one area, fix if broken
  # ---------------------------------------------------------------------------
  - id: "qa-session"
    agent: "self"
    condition: "{{orient_state.status}} == 'testing'"
    prompt: |
      You are a QA TESTING SESSION for the {{project_name}} project.
      You start with ZERO prior context. Your job: test one area, fix if broken, persist state, exit.
      Working directory: {{project_dir}}

      START BY READING THESE FILES (in this order):
      1. {{qa_state_file}} -- what's been tested, what's next
      2. {{qa_context_file}} -- previous QA findings

      ## Current Test Target
      Area/Case: {{orient_state.next_test}}

      ## Your Mission
      1. Test the area described in the QA state file
      2. If broken: read the relevant source files, fix the issue, re-test
      3. Run {{test_command}} && {{build_command}} after any code changes
      4. Commit fixes: fix(<module>): QA -- <description>

      ## State Persistence (CRITICAL)
      After testing the area/case:
      - Update {{qa_state_file}}: mark the area as "passing" or "failing" with issues list
      - Update {{qa_context_file}} with findings
      - If you fixed code: commit immediately

      ## When to Stop
      - You've tested the current area and either it passes or you've fixed it
      - You encounter a blocker you can't resolve -- add it to blockers in {{qa_state_file}}
      - Stop gracefully -- the outer recipe will continue with the next area
    output: "session_result"
    timeout: 1800

  # ---------------------------------------------------------------------------
  # Step 3: Post-session -- re-read QA-STATE.yaml, output status for outer loop
  # ---------------------------------------------------------------------------
  - id: "post-session"
    type: "bash"
    command: |
      cd {{project_dir}}
      python3 << 'PYEOF'
      import json, yaml
      try:
          with open("{{qa_state_file}}") as f:
              state = yaml.safe_load(f)
          blockers = state.get("blockers", [])
          session_num = int("{{session_count}}") + 1
          test_areas = state.get("test_areas", {})
          all_passing = all(a.get("status") == "passing" for a in test_areas.values())
          any_untested = any(a.get("status") in ("not-tested", "failing") for a in test_areas.values())

          if all_passing:
              status = "done"
          elif blockers:
              status = "blocked"
          elif any_untested:
              status = "testing"
          else:
              status = "done"

          print(json.dumps({
              "status": status,
              "session_count": str(session_num)
          }))
      except Exception as e:
          print(json.dumps({
              "status": "blocked",
              "session_count": str(int("{{session_count}}") + 1),
              "error": str(e)
          }))
      PYEOF
    output: "post_result"
    parse_json: true
```

**Step 3: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add templates/recipes/dev-machine-qa.yaml templates/recipes/dev-machine-qa-iteration.yaml && git commit -m "feat: add QA machine recipe templates (qa + qa-iteration)"
```

---

## Group 4: Admissions Mode + Agent

### Task 13: Create `modes/admissions.md`

**Files:**
- Create: `modes/admissions.md`

**Step 1: Create `modes/admissions.md`**

Create file `modes/admissions.md` with this exact content:

```markdown
---
mode:
  name: admissions
  description: Evaluate whether a problem is suitable for an autonomous development machine
  shortcut: admissions

  tools:
    safe:
      - bash
      - read_file
      - write_file
      - edit_file
      - glob
      - grep
      - delegate
      - mode

  default_action: allow
---

ADMISSIONS MODE activated. You are now evaluating whether this project is suitable for an autonomous development machine.

**Your mission:** Guide the user through the five admissions gates and produce a scored assessment.

## Prerequisites

Check if there's an existing assessment:
```bash
ls .dev-machine-assessment.md 2>/dev/null
```

If one exists, read it and ask the user if they want to re-evaluate or continue from where they left off.

## Gate Evaluation Process

Read `@dev-machine:context/gate-criteria.md` for the detailed gate criteria.

For each gate, have a focused conversation with the user:

### Gate 1: Decomposability
Ask the user:
- "Describe the major components/modules of what you're building"
- "Can you list 10+ concrete features?"
- "How independent are these features from each other?"

Examine the codebase if it exists:
- Look at directory structure, module boundaries
- Check for existing specs, README, architecture docs

Score: 0-100% with evidence.

### Gate 2: Verifiable Correctness with Speed
Ask/check:
- "What test framework do you use?"
- "How long does your test suite take?"
- "Do you have a type checker or linter?"

If codebase exists, verify:
- Run the test command and check it works
- Run the build command and check it works
- Check for existing tests

Score: 0-100% with evidence.

### Gate 3: Sufficient Architecture
Ask/check:
- "Do you have an architecture document?"
- "Can you describe module boundaries and key interfaces?"
- "What are your core technology choices?"

If docs exist, read them and assess completeness.

Score: 0-100% with evidence.

### Gate 4: Functioning Toolchain
Verify:
- Build command runs and succeeds
- Test command runs and reports results
- How fast is the cycle?

If no toolchain exists, assess how much work it would take to set up.

Score: 0-100% with evidence.

### Gate 5: Spec Quality
Assess:
- Do existing specs/PRDs have enough detail?
- Can a sample feature spec be written?
- Is there a domain expert available?

Score: 0-100% with evidence.

## Scoring Rules

- **Below 50%:** Hard stop. Provide specific remediation guidance for each failing gate.
- **50-75%:** Proceed with caution. Flag the risk.
- **Above 75%:** Confident.

Be transparent. No rounding up. No optimism bias.

## Output

After evaluating all five gates, write the assessment to `.dev-machine-assessment.md` using the format from `@dev-machine:context/gate-criteria.md`.

Present the results to the user with:
1. Per-gate scores and verdicts
2. Overall verdict (PROCEED / PROCEED WITH CAUTION / NOT READY)
3. Remediation plan for any gates below 50%
4. Recommended next steps

If the verdict is PROCEED or PROCEED WITH CAUTION, tell the user: "Run `/machine-design` to begin designing your development machine."

Call `mode(operation="clear")` when done.

CRITICAL: Call mode(clear) BEFORE outputting the final assessment summary.
```

**Step 2: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add modes/admissions.md && git commit -m "feat: add /admissions mode"
```

---

### Task 14: Create `agents/admissions-advisor.md`

**Files:**
- Create: `agents/admissions-advisor.md`

**Step 1: Create `agents/admissions-advisor.md`**

Create file `agents/admissions-advisor.md` with this exact content:

```markdown
---
meta:
  name: admissions-advisor
  description: "Evaluates whether a project is suitable for an autonomous development machine. Runs the five-gate admissions process (decomposability, verifiable correctness, sufficient architecture, functioning toolchain, spec quality) with confidence scoring. Produces a .dev-machine-assessment.md file.\n\n<example>\nuser: 'Evaluate whether my project is ready for an autonomous dev machine'\nassistant: 'I will delegate to dev-machine:admissions-advisor to run the five-gate admissions evaluation.'\n<commentary>\nThe admissions advisor conducts a structured evaluation with confidence intervals and produces a scored assessment.\n</commentary>\n</example>"

tools:
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
  - module: tool-search
    source: git+https://github.com/microsoft/amplifier-module-tool-search@main
  - module: tool-bash
    source: git+https://github.com/microsoft/amplifier-module-tool-bash@main
---

# Admissions Advisor

You evaluate whether a project is suitable for an autonomous development machine.

**Execution model:** You run as a sub-session, conducting the five-gate admissions evaluation. You are thorough, honest, and transparent about confidence scores.

## Your Knowledge

You understand the autonomous development machine pattern:

@dev-machine:context/pattern.md
@dev-machine:context/gate-criteria.md
@dev-machine:context/word4-lessons.md

## Evaluation Approach

### Be Evidence-Based
- Read the codebase if one exists (directory structure, tests, build files)
- Run commands to verify the toolchain works
- Look for existing architecture docs, specs, README files
- Don't just take the user's word -- verify claims

### Be Honest
- No optimism bias. If a gate is failing, say so clearly.
- Below 50% is a hard stop -- provide specific remediation guidance
- 50-75% means caution -- flag the risk transparently
- Don't round up. A 48% is a 48%.

### Be Helpful
- For failing gates, provide concrete remediation steps
- Explain WHY each gate matters (reference word4 failures)
- Suggest the minimum viable path to passing each gate

## Output Format

Write `.dev-machine-assessment.md` in the project root using the assessment output format defined in the gate criteria document.

## Final Response Contract

Your response back to the delegating agent must include:
1. Overall verdict (PROCEED / PROCEED WITH CAUTION / NOT READY)
2. Per-gate scores
3. Key risks identified
4. Recommended next steps
```

**Step 2: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add agents/admissions-advisor.md && git commit -m "feat: add admissions-advisor agent"
```

---

## Group 5: Machine Design Mode + Agent

### Task 15: Create `modes/machine-design.md`

**Files:**
- Create: `modes/machine-design.md`

**Step 1: Create `modes/machine-design.md`**

Create file `modes/machine-design.md` with this exact content:

```markdown
---
mode:
  name: machine-design
  description: Design an autonomous development machine for your project (founding session)
  shortcut: machine-design

  tools:
    safe:
      - bash
      - read_file
      - write_file
      - edit_file
      - glob
      - grep
      - delegate
      - mode

  default_action: allow
---

MACHINE DESIGN MODE activated. This is the founding session for your development machine.

## Gate Check

First, verify that the admissions gate has been passed:

```bash
ls .dev-machine-assessment.md 2>/dev/null
```

If no assessment exists, tell the user: "Run `/admissions` first to evaluate your project. The machine design phase requires a passing admissions assessment."

If an assessment exists, read it and verify the overall verdict is PROCEED or PROCEED WITH CAUTION. If NOT READY, tell the user to address the remediation items first.

## Founding Session Process

This is a collaborative session. You will work WITH the user to design their machine.

Read `@dev-machine:context/pattern.md` for the full pattern reference.
Read `@dev-machine:context/templates-reference.md` for template variables.

### Phase 1: Gather Machine Configuration

Collect the required template variables through conversation:

1. **Project basics:**
   - `project_name`: short identifier
   - `project_dir`: absolute path
   - Technology stack overview

2. **Build/test toolchain:**
   - `build_command`: what builds/compiles the project
   - `test_command`: what runs tests
   - `type_check_command`: separate type checker (if any)
   - Verify these commands work by running them

3. **Spec infrastructure:**
   - `specs_dir`: where specs will live
   - `architecture_spec`: path for the architecture spec

4. **Machine tuning:**
   - `max_features_per_session`: features per session (default: 3-5)
   - `max_outer_iterations`: max outer loop iterations (default: 50)
   - `module_size_threshold`: LOC limit per module (default: 10000)
   - `qa_enabled`: whether QA machine is needed

### Phase 2: Architecture Spec (The Constitution)

Guide the user through writing or reviewing their architecture spec. It must cover:

1. **Data model** -- core types and data structures
2. **Module boundaries** -- what modules exist, their responsibilities, interfaces between them
3. **Technology choices** -- language, framework, key libraries, with rationale
4. **Key patterns** -- state management, data flow, error handling, testing approach
5. **Build/test/deploy** -- how the project is built, tested, and (eventually) deployed

The architecture spec should be:
- Complete enough to prevent drift across hundreds of features
- Concise enough for an agent to read in <2 minutes
- Written for machine consumption (explicit interfaces, not hand-wavy descriptions)

If the user has existing architecture docs, review and assess them. Suggest additions if needed.

Write the architecture spec to `{{specs_dir}}/architecture.md`.

### Phase 3: Module Specs

For each major module identified in the architecture:
- Define internal architecture
- Define public API and contracts with adjacent modules
- Define test strategy

Write module specs to `{{specs_dir}}/modules/<module-name>.md`.

### Phase 4: First Batch of Feature Specs

Write the first batch of feature specs (5-15 features) covering the bootstrap/foundation work.
Use the template from `@dev-machine:templates/feature-spec-template.md`.

Write feature specs to `{{specs_dir}}/features/<module>/<feature-id>.md`.

### Phase 5: Machine Design Document

Compile all decisions into `.dev-machine-design.md` at the project root:

```markdown
# {{project_name}} Development Machine Design

## Machine Configuration

| Variable | Value |
|----------|-------|
| project_name | ... |
| project_dir | ... |
| build_command | ... |
| test_command | ... |
| ... | ... |

## Architecture Summary
[Brief summary with pointer to full spec]

## Module Inventory
[List of modules with status]

## Initial Feature Backlog
[List of first-batch features]

## QA Configuration
[If qa_enabled: what to test and how]

## Bootstrap Plan
[What needs to happen before the machine can start running]
```

### Phase 6: Wrap Up

Tell the user:
1. What was created (architecture spec, module specs, feature specs, design doc)
2. "Run `/generate-machine` to generate the machine artifacts"

Call `mode(operation="clear")` when done.

CRITICAL: Call mode(clear) BEFORE outputting the wrap-up summary.
```

**Step 2: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add modes/machine-design.md && git commit -m "feat: add /machine-design mode"
```

---

### Task 16: Create `agents/machine-designer.md`

**Files:**
- Create: `agents/machine-designer.md`

**Step 1: Create `agents/machine-designer.md`**

Create file `agents/machine-designer.md` with this exact content:

```markdown
---
meta:
  name: machine-designer
  description: "Runs the founding session for an autonomous development machine. Designs the architecture spec, module boundaries, state schema, recipe configuration, and first batch of feature specs. Requires a passing admissions assessment.\n\n<example>\nuser: 'Design a development machine for my React app'\nassistant: 'I will delegate to dev-machine:machine-designer to run the founding session and design your machine.'\n<commentary>\nThe machine designer conducts a collaborative founding session, producing the architecture spec, module specs, and initial feature specs.\n</commentary>\n</example>"

tools:
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
  - module: tool-search
    source: git+https://github.com/microsoft/amplifier-module-tool-search@main
  - module: tool-bash
    source: git+https://github.com/microsoft/amplifier-module-tool-bash@main
---

# Machine Designer

You run the founding session for an autonomous development machine.

**Execution model:** You are a collaborative design partner. You work WITH the user to design their machine, not just generate boilerplate.

## Your Knowledge

@dev-machine:context/pattern.md
@dev-machine:context/gate-criteria.md
@dev-machine:context/templates-reference.md
@dev-machine:context/word4-lessons.md

## Design Principles

### Progressive, Not Exhaustive
- Design enough architecture to start. Don't try to anticipate everything.
- The word4 architecture spec was 947 lines, written in ~1 hour. It was sufficient.
- Module specs are written just-in-time, not all at once.

### Machine-Consumable Specs
- Specs must include: explicit interfaces, acceptance criteria, file paths, edge cases
- A working session agent must be able to read a spec and implement it without asking questions
- Use the feature spec template from templates/feature-spec-template.md

### Honest Assessment
- If the architecture has gaps, say so. Better to know now than after 50 features.
- If the user's tech stack has blind spots (like Vitest not type-checking), identify them for the health check machine configuration.

### Domain Expertise
- You understand many technology stacks and can provide informed recommendations
- Help the user identify their build/test blind spots
- Help decompose their problem into modules and features

## Outputs

By the end of the founding session, produce:
1. Architecture spec (`specs/architecture.md`)
2. Module specs (`specs/modules/<name>.md`) for the first modules
3. Feature specs (`specs/features/<module>/<id>.md`) for the first batch
4. Machine design document (`.dev-machine-design.md`) with all configuration

## Final Response Contract

Your response must include:
1. Summary of what was designed
2. List of all files created
3. Machine configuration variables collected
4. Recommended next step (run `/generate-machine`)
```

**Step 2: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add agents/machine-designer.md && git commit -m "feat: add machine-designer agent"
```

---

## Group 6: Machine Generation Mode + Agent

### Task 17: Create `modes/generate-machine.md`

**Files:**
- Create: `modes/generate-machine.md`

**Step 1: Create `modes/generate-machine.md`**

Create file `modes/generate-machine.md` with this exact content:

```markdown
---
mode:
  name: generate-machine
  description: Generate development machine artifacts into your project
  shortcut: generate-machine

  tools:
    safe:
      - bash
      - read_file
      - write_file
      - edit_file
      - glob
      - grep
      - delegate
      - mode

  default_action: allow
---

GENERATE MACHINE MODE activated. Generating development machine artifacts for your project.

## Gate Check

First, verify that the machine design exists:

```bash
ls .dev-machine-design.md 2>/dev/null
```

If no design exists, tell the user: "Run `/machine-design` first to design your development machine. Generation requires a completed design document."

If a design exists, read it and extract all template variables.

## Generation Process

Read `@dev-machine:context/templates-reference.md` for the full variable reference.

### Step 1: Read the Design Document

Read `.dev-machine-design.md` and extract all variable values into a structured map.

Verify all required variables are present:
- `project_name`, `project_dir`, `state_file`, `context_file`
- `specs_dir`, `build_command`, `test_command`, `architecture_spec`

If any required variables are missing, ask the user to provide them.

### Step 2: Create Directory Structure

```bash
mkdir -p .dev-machine
```

### Step 3: Generate Recipe Files

For each template in `@dev-machine:templates/recipes/`:

1. Read the template file
2. Replace all `{{variable}}` placeholders with values from the design
3. Write the result to `.dev-machine/<recipe-name>.yaml`

Generated files:
- `.dev-machine/build.yaml` (from `dev-machine-build.yaml`)
- `.dev-machine/iteration.yaml` (from `dev-machine-iteration.yaml`)
- `.dev-machine/health-check.yaml` (from `dev-machine-health-check.yaml`)
- `.dev-machine/fix-iteration.yaml` (from `dev-machine-fix-iteration.yaml`)

If `qa_enabled` is true, also generate:
- `.dev-machine/qa.yaml` (from `dev-machine-qa.yaml`)
- `.dev-machine/qa-iteration.yaml` (from `dev-machine-qa-iteration.yaml`)

### Step 4: Generate Protocol Files

From templates, generate:
- `.dev-machine/working-session-instructions.md` (from `working-session-instructions.md`)
- `.dev-machine/feature-spec-template.md` (from `feature-spec-template.md`)

### Step 5: Generate State Files

At the project root, generate:
- `STATE.yaml` (from `templates/STATE.yaml`)
- `CONTEXT-TRANSFER.md` (from `templates/CONTEXT-TRANSFER.md`)
- `SCRATCH.md` (from `templates/SCRATCH.md`)

For `{{timestamp}}`, use the current ISO 8601 timestamp.

### Step 6: Populate STATE.yaml

Read the architecture spec and feature specs created during machine design.
Update STATE.yaml with:
- `architecture_spec.status: "approved"`
- Module specs that were written (with `status: "approved"`)
- Feature specs from the first batch (with `status: "ready"`)
- `next_action` pointing to the first piece of work

### Step 7: Verify Generation

```bash
echo "=== Generated Machine Files ==="
find .dev-machine -type f | sort
echo ""
echo "=== State Files ==="
ls -la STATE.yaml CONTEXT-TRANSFER.md SCRATCH.md 2>/dev/null
echo ""
echo "=== Recipe Validation ==="
python3 -c "import yaml; [yaml.safe_load(open(f'.dev-machine/{r}')) for r in ['build.yaml','iteration.yaml','health-check.yaml','fix-iteration.yaml']]; print('All recipes parse as valid YAML')"
```

### Step 8: Report to User

Present:
1. All files generated with paths
2. The command to start the machine: `amplifier recipe execute .dev-machine/build.yaml`
3. The command to run health checks: `amplifier recipe execute .dev-machine/health-check.yaml`
4. If QA enabled: `amplifier recipe execute .dev-machine/qa.yaml`
5. Remind them they can modify the generated files -- they belong to the project now

Call `mode(operation="clear")` when done.

CRITICAL: Call mode(clear) BEFORE outputting the final report.
```

**Step 2: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add modes/generate-machine.md && git commit -m "feat: add /generate-machine mode"
```

---

### Task 18: Create `agents/machine-generator.md`

**Files:**
- Create: `agents/machine-generator.md`

**Step 1: Create `agents/machine-generator.md`**

Create file `agents/machine-generator.md` with this exact content:

```markdown
---
meta:
  name: machine-generator
  description: "Generates development machine artifacts from a validated design. Reads template files, replaces variables with project-specific values, and writes the complete .dev-machine/ directory plus state files. Requires a .dev-machine-design.md to exist.\n\n<example>\nuser: 'Generate the machine files for my project'\nassistant: 'I will delegate to dev-machine:machine-generator to stamp out the .dev-machine/ directory from the design.'\n<commentary>\nThe machine generator reads templates, applies variable substitution, and produces working recipe files.\n</commentary>\n</example>"

tools:
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
  - module: tool-search
    source: git+https://github.com/microsoft/amplifier-module-tool-search@main
  - module: tool-bash
    source: git+https://github.com/microsoft/amplifier-module-tool-bash@main
---

# Machine Generator

You generate development machine artifacts from a validated design document.

**Execution model:** You are a precise template engine. Read the design, read the templates, substitute variables, write files. No creative interpretation -- the design document is the specification.

## Your Knowledge

@dev-machine:context/templates-reference.md

## Template Sources

Read templates from the bundle's templates directory:
- `@dev-machine:templates/recipes/dev-machine-build.yaml`
- `@dev-machine:templates/recipes/dev-machine-iteration.yaml`
- `@dev-machine:templates/recipes/dev-machine-health-check.yaml`
- `@dev-machine:templates/recipes/dev-machine-fix-iteration.yaml`
- `@dev-machine:templates/recipes/dev-machine-qa.yaml` (if qa_enabled)
- `@dev-machine:templates/recipes/dev-machine-qa-iteration.yaml` (if qa_enabled)
- `@dev-machine:templates/STATE.yaml`
- `@dev-machine:templates/CONTEXT-TRANSFER.md`
- `@dev-machine:templates/SCRATCH.md`
- `@dev-machine:templates/working-session-instructions.md`
- `@dev-machine:templates/feature-spec-template.md`

## Generation Rules

1. **Read the design document first.** Extract ALL variable values before generating any files.
2. **Every `{{variable}}` must be replaced.** If a variable is referenced in a template but not defined in the design, STOP and report the missing variable.
3. **Preserve YAML structure.** After variable substitution, the recipe YAML must be valid. Validate with Python's yaml.safe_load().
4. **Use default values** for optional variables not specified in the design (see templates-reference.md).
5. **Write files atomically.** Generate all files, then verify all at once.

## Output Locations

| Template | Output |
|----------|--------|
| `dev-machine-build.yaml` | `.dev-machine/build.yaml` |
| `dev-machine-iteration.yaml` | `.dev-machine/iteration.yaml` |
| `dev-machine-health-check.yaml` | `.dev-machine/health-check.yaml` |
| `dev-machine-fix-iteration.yaml` | `.dev-machine/fix-iteration.yaml` |
| `dev-machine-qa.yaml` | `.dev-machine/qa.yaml` |
| `dev-machine-qa-iteration.yaml` | `.dev-machine/qa-iteration.yaml` |
| `STATE.yaml` | `./STATE.yaml` |
| `CONTEXT-TRANSFER.md` | `./CONTEXT-TRANSFER.md` |
| `SCRATCH.md` | `./SCRATCH.md` |
| `working-session-instructions.md` | `.dev-machine/working-session-instructions.md` |
| `feature-spec-template.md` | `.dev-machine/feature-spec-template.md` |

## Validation

After generation, verify:
1. All `.dev-machine/*.yaml` files parse as valid YAML
2. All state files exist and are non-empty
3. No remaining `{{` or `}}` in any generated file (all variables substituted)
4. Recipe files reference correct relative paths

```bash
# Validation script
python3 << 'PYEOF'
import yaml, glob, re

errors = []

# Check YAML validity
for f in glob.glob(".dev-machine/*.yaml"):
    try:
        with open(f) as fh:
            yaml.safe_load(fh)
    except Exception as e:
        errors.append(f"YAML parse error in {f}: {e}")

# Check for unsubstituted variables
for f in glob.glob(".dev-machine/*") + ["STATE.yaml", "CONTEXT-TRANSFER.md", "SCRATCH.md"]:
    try:
        with open(f) as fh:
            content = fh.read()
        remaining = re.findall(r'\{\{[^}]+\}\}', content)
        if remaining:
            errors.append(f"Unsubstituted variables in {f}: {remaining[:5]}")
    except:
        pass

if errors:
    print("VALIDATION FAILED:")
    for e in errors:
        print(f"  - {e}")
else:
    print("VALIDATION PASSED: All files valid, all variables substituted.")
PYEOF
```

## Final Response Contract

Your response must include:
1. List of all files generated with full paths
2. Validation results (PASS/FAIL)
3. The commands to run the machine
4. Any warnings or notes
```

**Step 2: Commit**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git add agents/machine-generator.md && git commit -m "feat: add machine-generator agent"
```

---

## Group 7: Verification

### Task 19: Verify complete bundle structure

**Files:**
- None created; this is a verification task.

**Step 1: Verify all files exist**
Run:
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
echo "=== FULL FILE INVENTORY ==="
find . -type f -not -path './.git/*' | sort
echo ""
echo "=== FILE COUNT ==="
find . -type f -not -path './.git/*' | wc -l
```

Expected output should list exactly these files (plus any LICENSE):
```
./README.md
./behaviors/dev-machine.yaml
./bundle.md
./agents/admissions-advisor.md
./agents/machine-designer.md
./agents/machine-generator.md
./context/gate-criteria.md
./context/pattern.md
./context/templates-reference.md
./context/word4-lessons.md
./docs/plans/2026-02-25-dev-machine-bundle-implementation.md
./modes/admissions.md
./modes/generate-machine.md
./modes/machine-design.md
./templates/CONTEXT-TRANSFER.md
./templates/SCRATCH.md
./templates/STATE.yaml
./templates/feature-spec-template.md
./templates/recipes/dev-machine-build.yaml
./templates/recipes/dev-machine-fix-iteration.yaml
./templates/recipes/dev-machine-health-check.yaml
./templates/recipes/dev-machine-iteration.yaml
./templates/recipes/dev-machine-qa-iteration.yaml
./templates/recipes/dev-machine-qa.yaml
./templates/working-session-instructions.md
```

**Step 2: Verify YAML files parse**
Run:
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
python3 << 'PYEOF'
import yaml, glob

files = glob.glob("templates/recipes/*.yaml") + ["templates/STATE.yaml", "behaviors/dev-machine.yaml"]
for f in sorted(files):
    try:
        with open(f) as fh:
            yaml.safe_load(fh)
        print(f"  PASS: {f}")
    except Exception as e:
        print(f"  FAIL: {f} -- {e}")
PYEOF
```
Expected: All files PASS.

**Step 3: Verify bundle.md frontmatter parses**
Run:
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
python3 << 'PYEOF'
import yaml

with open("bundle.md") as f:
    content = f.read()

# Extract YAML frontmatter
parts = content.split("---")
if len(parts) >= 3:
    frontmatter = yaml.safe_load(parts[1])
    print(f"Bundle name: {frontmatter['bundle']['name']}")
    print(f"Bundle version: {frontmatter['bundle']['version']}")
    print(f"Agents: {frontmatter['agents']['include']}")
    print("PASS: bundle.md frontmatter is valid")
else:
    print("FAIL: Could not extract frontmatter")
PYEOF
```
Expected:
```
Bundle name: dev-machine
Bundle version: 0.1.0
Agents: ['admissions-advisor', 'machine-designer', 'machine-generator']
PASS: bundle.md frontmatter is valid
```

**Step 4: Verify mode frontmatter parses**
Run:
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
python3 << 'PYEOF'
import yaml, glob

for f in sorted(glob.glob("modes/*.md")):
    with open(f) as fh:
        content = fh.read()
    parts = content.split("---")
    if len(parts) >= 3:
        fm = yaml.safe_load(parts[1])
        mode = fm.get("mode", {})
        print(f"  PASS: {f} -- /{mode.get('shortcut', '?')}")
    else:
        print(f"  FAIL: {f}")
PYEOF
```
Expected:
```
  PASS: modes/admissions.md -- /admissions
  PASS: modes/generate-machine.md -- /generate-machine
  PASS: modes/machine-design.md -- /machine-design
```

**Step 5: Verify agent frontmatter parses**
Run:
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
python3 << 'PYEOF'
import yaml, glob

for f in sorted(glob.glob("agents/*.md")):
    with open(f) as fh:
        content = fh.read()
    parts = content.split("---")
    if len(parts) >= 3:
        fm = yaml.safe_load(parts[1])
        meta = fm.get("meta", {})
        print(f"  PASS: {f} -- {meta.get('name', '?')}")
    else:
        print(f"  FAIL: {f}")
PYEOF
```
Expected:
```
  PASS: agents/admissions-advisor.md -- admissions-advisor
  PASS: agents/machine-designer.md -- machine-designer
  PASS: agents/machine-generator.md -- machine-generator
```

**Step 6: Verify recipe templates contain expected variables**
Run:
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
echo "=== Template Variables Used ==="
grep -ohP '\{\{[^}]+\}\}' templates/recipes/*.yaml | sort -u
```
Expected: A list of all template variables used across recipe templates, including at minimum:
- `{{build_command}}`
- `{{context_file}}`
- `{{project_dir}}`
- `{{project_name}}`
- `{{specs_dir}}`
- `{{state_file}}`
- `{{test_command}}`

**Step 7: Final commit (if any fixups were needed)**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git status
# If clean: no commit needed
# If changes exist: git add -A && git commit -m "fix: address verification findings"
```

---

### Task 20: Final review and tag

**Step 1: Review git log**
Run:
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git log --oneline
```
Expected: A clean sequence of commits, one per task group.

**Step 2: Verify no uncommitted changes**
Run:
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git status
```
Expected: `nothing to commit, working tree clean`

**Step 3: Tag the initial version**
```bash
cd ~/dev/ANext/amplifier-bundle-dev-machine
git tag v0.1.0
```

---

## Summary

| Task | Group | Description | Files |
|------|-------|-------------|-------|
| 1 | Scaffold | bundle.md, README, behaviors, directories | 3 files |
| 2 | Context | context/pattern.md | 1 file |
| 3 | Context | context/gate-criteria.md | 1 file |
| 4 | Context | context/templates-reference.md | 1 file |
| 5 | Context | context/word4-lessons.md | 1 file |
| 6 | Templates | templates/STATE.yaml | 1 file |
| 7 | Templates | templates/CONTEXT-TRANSFER.md + SCRATCH.md | 2 files |
| 8 | Templates | templates/working-session-instructions.md | 1 file |
| 9 | Templates | templates/feature-spec-template.md | 1 file |
| 10 | Templates | Execution machine recipes (build + iteration) | 2 files |
| 11 | Templates | Health check recipes (health-check + fix-iteration) | 2 files |
| 12 | Templates | QA machine recipes (qa + qa-iteration) | 2 files |
| 13 | Modes | modes/admissions.md | 1 file |
| 14 | Agents | agents/admissions-advisor.md | 1 file |
| 15 | Modes | modes/machine-design.md | 1 file |
| 16 | Agents | agents/machine-designer.md | 1 file |
| 17 | Modes | modes/generate-machine.md | 1 file |
| 18 | Agents | agents/machine-generator.md | 1 file |
| 19 | Verify | Structure + YAML validation | 0 files |
| 20 | Verify | Final review + tag | 0 files |

**Total: 23 files across 20 tasks**
