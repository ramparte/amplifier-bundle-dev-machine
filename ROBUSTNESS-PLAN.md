# Dev Machine Robustness Improvement Plan

Session: 2026-03-07
Tracking file for systematic hardening of dev-machine infrastructure.

## Status Key: [ ] pending, [~] in progress, [x] done, [-] skipped

---

## Phase 1: Fix the Factory (this bundle)

### 1A: Add Dockerfile template
- [x] Create `templates/dev-machine.Dockerfile`
- [x] Non-root user with `{{user_uid}}`/`{{user_gid}}`
- [x] pyyaml for system python
- [x] Pinned uv version (not :latest)
- [x] Generic dep install based on `{{base_image}}`/`{{install_command}}` variables
- [x] Node.js install conditional on `{{node_setup}}` variable
- [x] Amplifier install via uv
- [x] ENTRYPOINT pointing to entrypoint.sh
- [x] CMD running the build recipe

### 1B: Fix template bugs
- [x] `watchdog.sh:140` - Replace `origin/master` with dynamic branch detection
- [x] `entrypoint.sh:106-109` - Replace pnpm/Vite check with `{{install_deps_block}}`
- [x] `monitor.sh:37` - Already had `|| echo "?"` fallback (OK as-is)
- [x] `watchdog.sh:17` - Remove `set -euo pipefail` (unsuitable for watchdog)
- [x] Update `templates-reference.md` with 9 new variables

### 1C: Add permission self-healing to monitor template
- [x] Add log file ownership healing at top of monitor.sh
- [x] Add .git/objects ownership healing before git operations
- [x] Add source file ownership healing before auto-commit
- [x] Remove `set -e` from monitor (use explicit error handling)
- [x] Add auto-commit of orphaned work (from openM365's monitor)
- [x] Add STATE.yaml awareness for restart decisions
- [x] Add auto-push when unpushed > threshold
- [x] Add stale in-progress feature reset before restart
- [x] Add stale blocker auto-verification (build-related blockers)

### 1D: Update generate-machine mode to stamp out ALL infrastructure
- [x] Add Step 5: Generate Infrastructure Scripts (entrypoint, watchdog, monitor)
- [x] Add Step 5: Generate Docker Config (Dockerfile, docker-compose)
- [x] Add Step 9: Print cron setup instructions
- [x] Add Step 8: Extended verification with infrastructure file checks
- [x] Add Step 10: Report with infrastructure items

### 1E: Add robustness checklist to word4-lessons.md
- [x] Document the three-layer recovery stack
- [x] Document heartbeat coordination pattern
- [x] Document failure-to-mechanism mapping (10 entries)
- [x] Add verification checklist for generated machines (container/host/operational)
- [x] Document the "scar tissue" principle

---

## Phase 2: Fix Deployed Machines

### 2A: universal-app (was CRITICAL - zero safety net)
Container status: RUNNING -- files modified on disk, take effect on next rebuild
- [x] Add restart: unless-stopped to compose
- [x] Add network_mode: host to compose
- [x] Create non-root user in Dockerfile (UID 1000)
- [x] Add retry loop + heartbeat + CF preflight to entrypoint.sh
- [x] Create monitor.sh (ported from openM365, adapted for npm)
- [x] Add security hardening to compose (cap_drop: ALL, no-new-privileges)
- [x] Set up cron: `*/10 * * * *` monitor.sh (active immediately)
- [x] Add SSH agent socket forwarding to compose
- [x] Pin uv version to 0.10.4 (was :latest)
- [x] Created PENDING-INFRA-CHANGES.md (rebuild required for container changes)

### 2B: safeguard (not running - modified freely)
- [x] Add restart: unless-stopped to compose
- [x] Fix monitor.sh: complete rewrite (no set -euo pipefail, permission self-healing, STATE.yaml, auto-commit, auto-push)
- [x] Fix monitor.sh: log to .dev-machine/monitor.log (was /tmp)
- [x] Add retry loop + heartbeat + CF preflight to entrypoint.sh
- [x] Fix Dockerfile: add jq, mcp, aiohttp, beautifulsoup4, ddgs, primp, pydantic
- [x] Add SSH agent socket and known_hosts to compose

### 2C: openM365 (was running - now exited, modified freely)
- [x] Add network_mode: host to compose
- [x] Add retry loop + heartbeat + CF preflight to entrypoint.sh
- [x] Create non-root user in Dockerfile (UID 1000)
- [x] Switch from shared ~/.amplifier to named volume (openm365-amplifier-home)
- [x] Upgrade restart policy to unless-stopped
- [x] Add SSH agent socket forwarding
- [x] Add security hardening (cap_drop: ALL, no-new-privileges)
- [x] Pin uv version to 0.10.4 (was curl install)
- [x] Upgrade Node.js from 20 to 22
- [x] Remove fragile host-path symlink hack, use real path mount instead
- [x] Replace pip install with uv sync
- [x] Remove dangerous editable-install of host cache modules

---

## Phase 3: Structural Improvements

### 3A: Infrastructure health score in monitor template
- [ ] Self-diagnostic on first launch
- [ ] Check: restart policy, network_mode, user, heartbeat, SSH agent
- [ ] Output to monitor log on every run
Status: DEFERRED -- good idea but not blocking. Current monitors cover the critical cases.

### 3B: Smoke test recipe for generated machines
- [ ] Container restart recovery test
- [ ] Monitor detection test
- [ ] File permission test
- [ ] Push capability test
Status: DEFERRED -- requires a recipe that spins up a test container. Lower priority than fixing deployed machines.

### 3C: Document scar tissue pattern
- [x] Failure-to-mechanism mapping table (10 entries)
- [x] "Every mechanism maps to a specific failure" principle
- [x] Why new machines must inherit ALL three layers ("scar tissue principle")
- [x] Robustness verification checklist (container/host/operational layers)
Status: DONE -- added to word4-lessons.md as "Infrastructure Robustness (The Three-Layer Stack)"

---

## Notes

### Running containers (as of session start):
- universal-app-dev-machine-run-fbcbb8d1b921 (active, working on SearchModal)
- openm365-dev-machine-run-30cb502694d1 (just started)
- safeguard-dev-machine (completed/exited, not running)

### Strategy for running containers:
- Modify files on host (compose, Dockerfile, scripts)
- Changes take effect on NEXT container restart
- Do NOT docker compose down on running machines unless user approves
- Add note to STATE.yaml about pending infrastructure changes if needed
