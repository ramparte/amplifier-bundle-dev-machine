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

## Post-Deployment Failure Patterns (March 2026)

After deploying dev machines to three projects (openM365, safeguard, universal-app),
several new failure patterns emerged that weren't present in the original word4 machine.

### New Failures Observed

| Observed Failure | Root Cause | Mechanism Added |
|------------------|-----------|-----------------|
| Container tools have broken shebangs after USER switch | Amplifier installed as root, shebangs point to `/root/.local/...` | Install amplifier AFTER `USER` switch so shebangs resolve to correct home |
| SSH git clones fail inside container | `openssh-client` not installed in image | Add `openssh-client` to system packages when bundle uses SSH git URLs |
| Named volume owned by root | `.amplifier` directory doesn't exist when Docker creates the named volume | Pre-create `~/.amplifier` directory before volume mount (Docker inherits ownership) |
| Config not seeded on first run | Entrypoint doesn't copy `settings.yaml` from `/config/` mount | Entrypoint must seed BOTH `keys.env` AND `settings.yaml` from `/config/` to `~/.amplifier/` |
| User creation fails on node base images | `useradd` fails if UID 1000 already exists as `node` | Use idempotent creation: `groupadd -f` + check `id -u` before `useradd` |
| Monitor log becomes root-owned after reboot | Docker writes to `monitor.log` as root during container restart | Monitor script self-heals ownership: `chown` at top of every run |
| Host cron survives reboot but container doesn't | Cron restarts with OS but container needs manual restart | Watchdog (cron) detects stopped container and auto-restarts |
| Cached bundle clone corrupted/incomplete | Network interruption during first-time bundle preparation | Amplifier detects invalid clones and retries; entrypoint retry loop handles transient failures |
| SSH_AUTH_SOCK not available in container | Host doesn't have SSH agent running (e.g., after reboot) | Compose uses `${SSH_AUTH_SOCK:-/dev/null}` fallback; container starts without SSH (push fails gracefully) |

### Template Gaps Discovered

1. **Dockerfile template was truncated** -- Missing the entire bottom half (user creation,
   tool installs, git config, ENTRYPOINT). The ROBUSTNESS-PLAN marked items as done but
   the template file itself was incomplete. **Lesson:** Verify template OUTPUT, not just
   checklist items.

2. **`{{username}}` undocumented** -- Used in Dockerfile template but not listed in
   `templates-reference.md`. **Lesson:** Every template variable must be documented.

3. **`openssh-client` not in default system packages** -- Required when the active bundle
   references private repos via SSH. **Lesson:** The machine generator should detect SSH
   git URLs in the host's `settings.yaml` and add `openssh-client` automatically.

### Updated Robustness Verification Checklist

Add these to the existing checklist:

**Container layer (additions):**
- [ ] Amplifier installed as non-root user (shebangs point to `$HOME/.local/bin/`)
- [ ] `openssh-client` installed if bundle uses SSH git URLs
- [ ] `~/.amplifier` directory pre-created before named volume mount
- [ ] Entrypoint seeds BOTH `keys.env` AND `settings.yaml` from `/config/`
- [ ] User creation is idempotent (handles pre-existing UID/GID)
- [ ] PATH includes `$HOME/.local/bin` for non-root tool installs

**Host monitoring layer (additions):**
- [ ] Monitor self-heals log file ownership at start of every run
- [ ] Watchdog self-heals its own log file ownership (added March 7, 2026)
- [ ] Watchdog handles container stopped state (not just crashed)

## Multi-Machine Operations Analysis (March 7, 2026)

After running three machines (openM365, safeguard, universal-app) concurrently for
several days, a cross-machine session analysis revealed new failure patterns not
present in the original single-machine word4 deployment.

### Cross-Machine Status Snapshot

| Machine | Status | Iterations | Success Rate | Root Issue |
|---------|--------|-----------|--------------|------------|
| **safeguard** | Healthy | 228 | 100% | None — reference model |
| **openM365** | Critical failure loop | 160 | 1.25% | Pyright build-gate + infinite retry |
| **universal-app** | Recovering | 14 | Mixed | Stale blockers + missing deps |

**Key insight:** Safeguard is the proof that the architecture works. Its 100% success
rate across 228 iterations, handling 120 rate-limit events automatically, demonstrates
that when the machine is set up correctly, it is genuinely robust. The other two
machines' failures are setup/configuration gaps, not architectural flaws.

### New Failure Patterns

#### Pattern 1: Build-Gate Infinite Retry Loop (Critical)

**Observed in:** openM365 — 158 consecutive failures burning API credits.

**What happened:** A working session introduced new imports (`pydantic`, `cryptography`,
`click`, `msal`) without adding them to the container's Python environment. The build
gate (pyright) found 100+ type errors. STATE.yaml was marked `blocked`. Every
subsequent iteration: read state → see blocked → check-health fails → recipe exits 1 →
entrypoint retries in 60s → repeat forever.

**Root cause:** No retry cap on the outer loop when a recipe STEP fails (as opposed to
transient API errors). The entrypoint correctly handles CF/API failures with backoff,
but a structural recipe failure (missing deps, broken build) gets the same retry
treatment as a transient error.

**Mechanism needed:** A `MAX_CONSECUTIVE_FAILURES` cap in the entrypoint. After N
consecutive recipe-level failures (not CF/API), the entrypoint should:
1. Log a clear alert: `"CRITICAL: $N consecutive recipe failures. Stopping."`
2. Touch the heartbeat file (so watchdog knows it's intentional)
3. Sleep indefinitely (or until STATE.yaml changes)

**Why this isn't just a "missing deps" problem:** Even with perfect dependency
management, a working session can always introduce a build-breaking change. The machine
must degrade gracefully rather than burn cycles indefinitely.

#### Pattern 2: HTTPS Clone Failures Inside Containers

**Observed in:** All three machines during initial setup.

**What happened:** Containers have SSH agent forwarding (for `git push`) but no HTTPS
credential helper. Amplifier's bundle/module system clones repos via HTTPS URLs by
default. Inside the container, these clones fail silently or hang waiting for
credentials.

**Root cause:** Two assumptions collided:
- Amplifier assumes HTTPS works for cloning (reasonable on a dev laptop)
- Containers have SSH but not HTTPS credentials (reasonable for Docker)

**Mechanism added:** Git URL rewrite in Dockerfile:
```bash
git config --global url."git@github.com:".insteadOf "https://github.com/"
```
This transparently rewrites all HTTPS GitHub URLs to SSH, using the forwarded SSH agent.

**Also required:** `openssh-client` in the system packages (needed by git's SSH
transport). Both are now in the Dockerfile template.

#### Pattern 3: pyyaml Missing from System Python

**Observed in:** openM365.

**What happened:** Recipe bash steps use `python3 -c "import yaml; ..."` to parse
STATE.yaml. The container has a virtualenv Python with pyyaml, but the system Python
(used by bash `python3`) doesn't have it. `ModuleNotFoundError: No module named 'yaml'`.

**Root cause:** The Dockerfile template installs tools in a virtualenv but recipe bash
steps invoke system python.

**Mechanism added:** `pip install --break-system-packages pyyaml` in the Dockerfile
template, ensuring system python can parse YAML in recipe bash steps.

#### Pattern 4: Empty Session Accumulation

**Observed in:** All three machines.

| Machine | Total Sessions | Empty | Empty % |
|---------|---------------|-------|---------|
| openM365 | 175 | 170 | 97% |
| safeguard | 539 | 374 | 69% |
| universal-app | 95 | 91 | 96% |

**What happens:** Each recipe iteration creates a session directory. If the recipe
completes quickly (no-op, fast exit, check-health failure), the session dir has an
empty transcript. Over time, hundreds of empty directories accumulate.

**Impact:** Disk bloat and noise in session listings. No functional harm.

**Mechanism needed:** Post-iteration cleanup hook that removes session directories
with 0-line transcripts. Or: the recipe framework should not create a session dir
until the first LLM turn actually occurs.

#### Pattern 5: Stale Blockers Preventing Machine Progress

**Observed in:** universal-app (F-096 Visual Theme Builder permanently blocked).

**What happens:** A feature is marked `blocked` with a detailed reason. The machine
correctly routes around it, but the feature sits permanently blocked because no
automated process validates whether the blocker is still real.

**Current mitigation:** The monitor template already auto-verifies BUILD-related
blockers (runs the build command, clears if it passes). But FEATURE-level blockers
(spec compliance, architectural issues) have no auto-verification path.

**Mechanism needed:** A blocker aging policy. Features blocked for >N epochs without
human attention should be flagged in the monitor log with increasing urgency, or
automatically moved to a "deferred" state so they don't clutter active feature counts.

### The Safeguard Success Pattern

Safeguard maintained 100% success across 228 iterations. Why?

1. **Clean dependency management** — All deps installed correctly from the start.
   Working sessions never introduced imports without corresponding installs.
2. **No build-breaking changes** — The project's tech stack (Python) has more
   forgiving type checking than openM365's TypeScript/pyright setup.
3. **Blocker-free operation** — STATE.yaml `blockers: []` throughout, so
   check-health always skipped cleanly.
4. **Rate limiting handled transparently** — 120 sessions hit rate limits but
   Amplifier's built-in retry logic recovered every time.

**Lesson:** The dev-machine architecture IS robust when properly configured. Most
failures are in the gap between "template generated" and "machine fully operational"
— the setup/configuration phase.

### Robustness Improvements Made (March 7, 2026)

| Fix | Applied To | Commit |
|-----|-----------|--------|
| Added `openssh-client` to system packages | Template + all 3 machines | `6f3ab26` / per-machine |
| Added git SSH URL rewrite | Template + all 3 machines | `6f3ab26` / per-machine |
| Added `pyyaml` to system python | openM365 (others already had it) | `01407f8` |
| Pre-seeded `.amplifier/cache` from host | All 3 machines (runtime) | — |
| Added log ownership self-heal to watchdog | Template | `47bcef6` |
| Cleared stale blockers in universal-app | universal-app STATE.yaml | — |

### Outstanding Items — All Resolved (March 7, 2026)

All five items were implemented on March 7, 2026. See "Robustness Mechanisms Implemented" section below for details.

1. ✅ **`MAX_CONSECUTIVE_FAILURES` cap in entrypoint** — `templates/scripts/entrypoint.sh`. Configurable via env var (default 5). Distinguishes structural failures (long-running + nonzero exit) from transient (CF / quick crash). On halt: writes `POST-MORTEM.md`, touches heartbeat, sleeps until `STATE.yaml` mtime changes.
2. ✅ **Empty session cleanup** — Post-session step in `templates/recipes/dev-machine-iteration.yaml`. Sweeps `~/.amplifier/sessions/` after every iteration; removes dirs where `events.jsonl` is absent, empty, or under 3 lines.
3. ✅ **Blocker aging policy** — `templates/scripts/dev-machine-monitor.sh`. Tracks `since` epoch field per blocker: INFO (1–5 epochs), WARNING (6–10), CRITICAL (11–19), AUTO-DEFER (20+). Existing BUILD-blocker auto-verify logic preserved.
4. ✅ **Post-mortem template** — `templates/POST-MORTEM.md`. Auto-populated by entrypoint on halt (timestamp, failure count, last log lines). Manual sections for root-cause classification and restart checklist.
5. ✅ **Smoke test recipe** — `templates/recipes/dev-machine-smoke-test.yaml`. Validates file existence, YAML validity, Docker config keys, `STATE.yaml` content, and robustness mechanism presence in scripts. Run before first machine start.

## Robustness Mechanisms Implemented (March 7, 2026)

Five mechanisms added to close the gaps identified in the multi-machine analysis above.
All are now standard in generated machine templates.

### Mechanism 1: MAX_CONSECUTIVE_FAILURES Cap (`entrypoint.sh`)

Turns the "openM365 burn loop" (158 consecutive failures burning API credits) into a cheap, loud halt.

**How it works:**
- Counts consecutive structural failures: exit nonzero after a long-running recipe (>30 s by default)
- Transient failures (CF preflight, quick crash <30 s) reset the counter instead of incrementing it
- At the cap: writes `POST-MORTEM.md` with timestamp and last log lines, touches heartbeat, enters `sleep 60` loop
- Auto-resumes when `STATE.yaml` is manually modified (mtime polling)

**Configuration:** `MAX_CONSECUTIVE_FAILURES` env var, default `5`.

**Why the structural/transient distinction matters:** A recipe that crashes in 4 seconds is almost certainly an API blip; a recipe that runs for 5 minutes and then exits 1 is almost certainly a build-gate failure. Treating them the same causes the burn loop. Treating them differently lets CF retries keep working while capping the structural retries.

### Mechanism 2: Empty Session Cleanup (`dev-machine-iteration.yaml`)

Addresses the 69–97% empty session rate observed across all machines.

Post-session step after every iteration:
- Finds all dirs in `~/.amplifier/sessions/`
- Removes any where `events.jsonl` is missing, 0 bytes, or fewer than 3 lines
- Silent when nothing to clean; no impact on real sessions

### Mechanism 3: Blocker Aging Policy (`dev-machine-monitor.sh`)

Prevents features from being permanently stuck (e.g., universal-app F-096 blocked indefinitely).

| Blocker Age | Severity | Action |
|-------------|----------|--------|
| 1–5 epochs | INFO | Log only |
| 6–10 epochs | WARNING | Log with emphasis |
| 11–19 epochs | CRITICAL | Log as urgent |
| 20+ epochs | AUTO-DEFER | Move feature to `deferred` status in STATE.yaml |

Requires blockers to carry a `since: <epoch>` field. The monitor computes age as `current_epoch - since`. Existing BUILD-blocker auto-verify logic (run build, clear on pass) is unchanged.

### Mechanism 4: Post-Mortem Template (`templates/POST-MORTEM.md`)

Replaces the current pattern of appending narrative sections to this document after every incident.

Auto-populated by entrypoint on halt:
- Machine name, timestamp, consecutive failure count, last recipe exit code
- Last 20 lines of entrypoint log

Manual sections (human fills in):
- Root cause classification: transient / structural / config / infra
- Steps taken to resolve
- Mechanism added or checklist item updated
- Restart checklist (confirm STATE.yaml fixed, clear failure count, restart container)

### Mechanism 5: Smoke Test Recipe (`templates/recipes/dev-machine-smoke-test.yaml`)

Automated pre-flight that catches setup gaps before the first overnight run.

Validates:
- All required template files exist (entrypoint, watchdog, monitor, docker-compose)
- `docker-compose.yaml` is valid YAML with `restart: unless-stopped` and `network_mode: host`
- `STATE.yaml` is present and parseable
- `entrypoint.sh` contains `MAX_CONSECUTIVE_FAILURES` logic
- `dev-machine-monitor.sh` contains blocker aging (`since` field) logic

Run once after `dev-machine-setup` and before `docker compose up -d`.

### Updated Robustness Verification Checklist (March 7, 2026 additions)

Add to the checklist in "Robustness Verification Checklist" above:

**Container layer:**
- [ ] `MAX_CONSECUTIVE_FAILURES` cap present in entrypoint (default 5, configurable via env)
- [ ] Entrypoint resumes from halt on `STATE.yaml` mtime change (no manual container restart needed)

**Operational layer:**
- [ ] Smoke test recipe run and passing before first `docker compose up -d`
- [ ] `POST-MORTEM.md` template present in project root
- [ ] Blockers in STATE.yaml carry `since: <epoch>` field (required for aging policy)
- [ ] Monitor blocker aging thresholds reviewed for project's epoch cadence

### The "First Night" Principle

Every new machine will fail on its first overnight run. This is not a prediction;
it is an observation from deploying four machines. The failures are always in the
gap between what the template provides and what the specific project needs:

- word4: CF backoff missing → 514-attempt incident
- openM365: pyyaml + SSH rewrite missing → clone failures + yaml parse errors
- safeguard: Initial user creation collision → container wouldn't start
- universal-app: Build command misconfigured → health check always fails

**Mitigation:** Accept that the first night will fail. Design the machine to fail
LOUDLY (not silently) and CHEAPLY (not burning API credits in tight loops). The
`MAX_CONSECUTIVE_FAILURES` cap is the key mechanism for this — it turns an expensive
silent failure into a cheap loud one.
