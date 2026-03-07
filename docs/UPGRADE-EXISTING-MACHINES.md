# Upgrading Existing Dev Machines

This guide is for dev machines that were generated BEFORE the robustness hardening
(March 2026). New machines generated with the updated templates get all of this
automatically.

## What Changed

The templates were hardened based on failure patterns observed across word4, openM365,
safeguard, and universal-app. Key improvements:

| Layer | What | Why |
|-------|------|-----|
| **Dockerfile** | Non-root user (UID 1000), pinned uv 0.10.4, jq | Root-owned files break git ops; unpinned uv breaks builds |
| **docker-compose** | host networking, `restart: unless-stopped`, named volume for .amplifier, SSH agent, security hardening | CF bot-detection on bridge NAT; no auto-recovery; shared host cache causes editable-install conflicts; can't push from container |
| **entrypoint** | Retry loop with CF preflight, heartbeat file, silent failure detection | Single-shot exec dies permanently on transient API errors |
| **monitor** | Permission self-healing, STATE.yaml awareness, auto-commit, auto-push, log rotation | Root-owned logs kill cron silently; blind restarts waste tokens; orphaned work lost |

## Quick Upgrade Checklist

For each existing machine, apply these changes in order:

### 1. Dockerfile Changes

Add non-root user AFTER all root-level installs, BEFORE the entrypoint COPY:

```dockerfile
# -- Non-root user (UID/GID must match host for bind-mount permissions) --------
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd -g ${USER_GID} devmachine \
    && useradd -m -u ${USER_UID} -g ${USER_GID} -s /bin/bash \
         -d /home/samschillace samschillace

# Copy root's tool installations to new user
RUN cp -r /root/.local /home/samschillace/.local \
    && chown -R ${USER_UID}:${USER_GID} /home/samschillace/.local

USER samschillace
```

Pin uv version:
```dockerfile
# Replace: COPY --from=ghcr.io/astral-sh/uv:latest ...
# With:
COPY --from=ghcr.io/astral-sh/uv:0.10.4 /uv /uvx /usr/local/bin/
```

Add jq to apt-get install:
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl ca-certificates jq \
    && rm -rf /var/lib/apt/lists/*
```

Update entrypoint COPY with chown:
```dockerfile
COPY --chown=1000:1000 entrypoint.sh /home/samschillace/entrypoint.sh
```

### 2. docker-compose Changes

Add these to your `services.dev-machine` section:

```yaml
    # Container name (required for monitor to find it)
    container_name: YOUR-PROJECT-dev-machine

    # Host networking prevents CF bot-detection from Docker bridge NAT
    network_mode: host

    # Auto-recovery from crashes and reboots
    restart: unless-stopped

    # Security hardening
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
```

Switch from shared host .amplifier to named volume:
```yaml
    volumes:
      # REMOVE THIS (causes editable-install conflicts):
      # - ${HOME}/.amplifier:${HOME}/.amplifier
      
      # ADD THESE:
      # Named volume for Amplifier runtime (container builds its own cache)
      - YOUR-PROJECT-amplifier-home:/home/samschillace/.amplifier
      # Host config (read-only)
      - ${HOME}/.amplifier/keys.env:/config/keys.env:ro
      - ${HOME}/.amplifier/settings.yaml:/config/settings.yaml:ro
      # SSH agent for git push
      - ${SSH_AUTH_SOCK}:/run/ssh-agent.sock:ro
      - ${HOME}/.ssh/known_hosts:/home/samschillace/.ssh/known_hosts:ro

    environment:
      - SSH_AUTH_SOCK=/run/ssh-agent.sock

# Top-level volumes declaration:
volumes:
  YOUR-PROJECT-amplifier-home:
```

### 3. Entrypoint: Add Retry Loop

Replace the single-shot `exec amplifier tool invoke recipes ...` at the end of
your entrypoint.sh with the retry loop pattern. The key pieces:

```bash
# -- Heartbeat for watchdog coordination ---
HEARTBEAT="/path/to/project/.dev-machine/.dev-machine-heartbeat"

# -- CF preflight check ---
cf_preflight() {
    HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' \
        -H "x-api-key: ${ANTHROPIC_API_KEY:-}" \
        -H "anthropic-version: 2023-06-01" \
        -H "content-type: application/json" \
        -d '{"model":"claude-sonnet-4-20250514","max_tokens":1,"messages":[{"role":"user","content":"hi"}]}' \
        https://api.anthropic.com/v1/messages 2>/dev/null || echo "000")
    [ "$HTTP_CODE" != "403" ] && [ "$HTTP_CODE" != "000" ]
}

# -- Infinite retry loop ---
while true; do
    if ! cf_preflight; then
        echo "CF blocked. Backing off..."
        sleep 900
        continue
    fi
    touch "$HEARTBEAT"
    amplifier tool invoke recipes operation=execute recipe_path=.dev-machine/build.yaml
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        echo "Recipe failed ($EXIT_CODE). Retrying in 60s..."
        sleep 60
        continue
    fi
    echo "Completed. Cooldown 60s..."
    sleep 60
done
```

Also: Remove `set -euo pipefail` from the entrypoint. The retry loop needs
explicit error handling, not bail-on-error.

### 4. Monitor: Replace or Create

If you have a monitor.sh, check for these anti-patterns:
- `set -euo pipefail` at the top (will silently die on any error)
- Logging to `/tmp/` (lost on reboot)
- No permission self-healing
- Blind restart without checking STATE.yaml

Replace with the template from `templates/scripts/dev-machine-monitor.sh` in
this bundle, adapting the PROJECT_DIR, CONTAINER, and IMAGE variables.

Key features the new monitor has:
- Self-heals root-owned log files and .git/objects
- Reads STATE.yaml before restarting (won't restart if all done or blocked)
- Auto-commits orphaned work when container is stopped
- Resets stale in-progress features to pending before restart
- Auto-pushes when unpushed commits exceed threshold
- Log rotation at 500 lines

### 5. Cron Setup

Ensure your crontab has entries for the monitor:

```bash
# Add to crontab (crontab -e):
*/10 * * * * /path/to/project/.dev-machine/monitor.sh
```

Verify with: `crontab -l | grep your-project`

### 6. Fix Existing Permissions

Before rebuilding, fix any root-owned files from previous container runs:

```bash
cd /path/to/your/project

# Fix .git/objects (most common issue)
docker run --rm -v "$(pwd):$(pwd)" -w "$(pwd)" \
    --entrypoint bash YOUR-IMAGE-NAME \
    -c "chown -R $(id -u):$(id -g) $(pwd)/.git"

# Fix source files
docker run --rm -v "$(pwd):$(pwd)" -w "$(pwd)" \
    --entrypoint bash YOUR-IMAGE-NAME \
    -c "chown -R $(id -u):$(id -g) $(pwd)/src $(pwd)/tests $(pwd)/STATE.yaml"
```

### 7. Rebuild and Restart

```bash
cd /path/to/your/project
docker compose build
docker compose up -d
```

## Verification

After upgrading, verify these are all true:

```bash
# Container running with restart policy
docker inspect YOUR-CONTAINER --format '{{.HostConfig.RestartPolicy.Name}}'
# Expected: unless-stopped

# Running as non-root
docker exec YOUR-CONTAINER whoami
# Expected: samschillace (not root)

# Host networking
docker inspect YOUR-CONTAINER --format '{{.HostConfig.NetworkMode}}'
# Expected: host

# SSH agent available
docker exec YOUR-CONTAINER ssh -T git@github.com 2>&1 | head -1
# Expected: "Hi username! ..." (not "Permission denied")

# Monitor cron active
crontab -l | grep your-project
# Expected: */10 or */15 entry

# Heartbeat being touched
ls -la .dev-machine/.dev-machine-heartbeat
# Expected: recent timestamp
```

## Reference

Full template files are in this bundle's `templates/` directory:
- `templates/dev-machine.Dockerfile`
- `templates/docker-compose.dev-machine.yaml`
- `templates/scripts/entrypoint.sh`
- `templates/scripts/dev-machine-monitor.sh`
- `templates/scripts/dev-machine-watchdog.sh`

The `context/word4-lessons.md` file has the full failure-to-mechanism mapping
that motivated these changes.
