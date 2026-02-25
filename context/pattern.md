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