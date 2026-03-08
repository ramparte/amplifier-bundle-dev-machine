# Dev Machine Post-Mortem

## Automated Failure Report

> This section is populated automatically when the entrypoint halts due to MAX_CONSECUTIVE_FAILURES.

| Field | Value |
|-------|-------|
| Halt timestamp | `{{HALT_TIMESTAMP}}` |
| Consecutive failures | `{{FAILURE_COUNT}}` |
| Last exit code | `{{LAST_EXIT_CODE}}` |
| Machine uptime | `{{MACHINE_UPTIME}}` |
| Current epoch | `{{CURRENT_EPOCH}}` |

### Last Log Lines

```
{{LAST_LOG_LINES}}
```

### STATE.yaml at Halt

```yaml
{{STATE_AT_HALT}}
```

---

## Manual Analysis

> Fill this in when investigating the halt.

### Root Cause

_What was the underlying issue?_

### Classification

- [ ] Infrastructure (Docker, network, SSH, disk)
- [ ] Dependency (build tool, package registry, API)
- [ ] Code quality (tests failing, type errors, lint)
- [ ] Architecture (design issue the machine can't resolve)
- [ ] Configuration (wrong settings, missing env vars)
- [ ] Amplifier (framework bug, recipe issue, provider error)

### Resolution

_What was done to fix it?_

### Prevention

_What template/recipe change would prevent recurrence?_

### Restart Checklist

Before restarting the machine:
- [ ] Root cause identified and documented above
- [ ] Fix applied (to code, config, or template)
- [ ] STATE.yaml updated if needed (clear blockers, adjust feature status)
- [ ] Build passes locally
- [ ] Entrypoint halt cleared (delete or truncate this automated section)
