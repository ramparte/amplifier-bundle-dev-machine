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
### 7. Content-Aware Health Checks (the blocker-rewrite loop)
- Module health check must NOT blindly re-block modules the machine is already working on
- **Anti-pattern:** Health check writes blocker for oversized module -> next session's pre-flight gate sees blocker -> exits -> entrypoint treats as crash -> backoff. Repeat forever.
- **Root cause in word4:** The bypass tried to look up a specific feature ID (`F-901`) at the wrong YAML path (`state['features']` instead of `run_to_conclusion.phase_b.items[]`), with the wrong key name, and the wrong status value. Three compounding bugs meant the bypass never fired.
- **Fix:** Content-aware bypass. Instead of looking up specific feature IDs (fragile, breaks when STATE.yaml structure evolves), check whether `next_action` already mentions the oversized module by name. If it does, the machine has a plan -- warn, don't block. Only block on *genuinely unplanned* oversized modules.
- **Principle:** Health checks should respect the machine's own planning. If the machine already knows about a problem and has instructions to address it, the health check should not override that decision.

## Infrastructure Robustness (The Three-Layer Stack)

### The Three-Layer Recovery Stack

Every robust dev machine needs three independent recovery layers. Each addresses a different failure class. Missing ANY layer creates a fragility gap that will eventually cause overnight failures.

| Layer | Runs | Frequency | What It Handles |
|-------|------|-----------|-----------------|
| **Entrypoint retry loop** | Inside container | Continuous | API blips, CF challenges, recipe crashes. Container never exits permanently. |
| **Watchdog** | Host cron | Every 15 min | Container crashes, OOM, host reboots. Restarts dead containers. |
| **Monitor** | Host cron | Every 10 min | Operational drift: stale blockers, unpushed commits, permission issues, orphaned work. |

### The Heartbeat Coordination Pattern

The **heartbeat file** (`.dev-machine-heartbeat`) is the critical coordination mechanism between layers:

1. The entrypoint touches the heartbeat file before every significant sleep (CF backoff, inter-session cooldown)
2. The watchdog checks heartbeat age before restarting:
   - Heartbeat fresh (<60 min) + 0% CPU = entrypoint is alive in CF backoff. DO NOT restart.
   - Heartbeat stale (>60 min) + 0% CPU = entrypoint is truly dead. Restart.
3. Without this coordination, the watchdog restarts containers during CF backoff, creating an infinite restart loop that makes CF blocks WORSE.

**This is non-obvious and critical.** Every new machine must have it.

### The Failure-to-Mechanism Map

Every robustness mechanism in word4 traces to a specific observed failure:

| Observed Failure | Mechanism Added |
|------------------|-----------------|
| Cloudflare blocking API during long runs | Pre-flight check, CF backoff tiers, mid-session scan, `network_mode: host` |
| Recipe exit 0 but silently failing (514-attempt incident) | Stdout inspection for "Recipe execution failed", treat as error |
| Watchdog restarting during CF backoff | Heartbeat file + watchdog heartbeat-age check |
| Root-owned files blocking host cron/monitors | Non-root container user + permission self-healing in monitor |
| Stale blockers trapping machine when build passes | Monitor auto-verifies and clears build blockers |
| Unpushed commits piling up (SSH agent death) | Monitor auto-push at >10 commits threshold |
| Orphaned work when container dies mid-feature | Monitor auto-commits dirty tree before restart |
| Agent implementing outside recipe (session drift) | AGENTS.md guardrails + container-check in recipes |
| `set -euo pipefail` in monitor killing it silently | Explicit per-command error handling (never set -e in monitors) |
| Container bridge NAT triggering CF bot detection | `network_mode: host` (uses real IP/fingerprint) |

### Robustness Verification Checklist

Before considering a generated machine production-ready, verify ALL of:

**Container layer:**
- [ ] Entrypoint has infinite retry loop (not bare `exec`)
- [ ] CF preflight check before each recipe attempt
- [ ] Heartbeat file touched before every sleep
- [ ] Silent failure detection (stdout scan for "Recipe execution failed")
- [ ] `restart: unless-stopped` in docker-compose
- [ ] `network_mode: host` in docker-compose
- [ ] Non-root user in Dockerfile (matching host UID/GID)

**Host monitoring layer:**
- [ ] Watchdog runs via cron every 15 min
- [ ] Watchdog is heartbeat-aware (won't restart during CF backoff)
- [ ] Monitor runs via cron every 10 min
- [ ] Monitor has permission self-healing
- [ ] Monitor has auto-commit for orphaned work
- [ ] Monitor has STATE.yaml awareness
- [ ] Monitor does NOT use `set -euo pipefail`

**Operational layer:**
- [ ] SSH agent socket forwarded to container (push capability)
- [ ] Named volume for `~/.amplifier` (not shared with host)
- [ ] Security hardening: `cap_drop: ALL`, `no-new-privileges`
- [ ] Git configured with safe.directory and dev-machine identity
- [ ] Build gate runs after every working session

### The "Scar Tissue" Principle

New machines MUST inherit ALL three layers. The temptation is to start simple ("we'll add monitoring later"). This always fails because:

1. The first overnight run without monitoring produces a subtle failure
2. The failure is only discovered the next morning
3. A monitor is hastily added, but without the heartbeat coordination
4. The hasty monitor conflicts with the entrypoint's backoff strategy
5. More failures ensue until the full three-layer stack is rebuilt

**Start with the full stack. You cannot incrementally arrive at robustness.**
