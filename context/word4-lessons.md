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