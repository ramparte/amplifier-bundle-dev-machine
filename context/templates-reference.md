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

| `container_name` | Docker container name for the dev machine | `myproject-dev-machine` |
| `image_name` | Docker image name (tagged on build) | `myproject-dev-machine:latest` |
| `bundle_dir` | Absolute path to the amplifier-bundle-dev-machine checkout | `/home/user/dev/amplifier-bundle-dev-machine` |
| `user_uid` | Host user UID (for Docker build arg USER_UID) | `1000` |
| `user_gid` | Host user GID (for Docker build arg USER_GID) | `1000` |
| `cf_backoff` | Cloudflare backoff seconds (entrypoint) | `900` |
| `cf_backoff_max` | Max CF preflight exponential backoff ceiling (seconds) | `2700` |
| `inter_session_cooldown` | Pause between successful sessions in seconds | `60` |

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

### Infrastructure Scripts (in project root or moved to `scripts/`)
- `scripts/entrypoint.sh` -- container entrypoint with CF-aware retry loop (from `templates/scripts/entrypoint.sh`)
- `scripts/dev-machine-watchdog.sh` -- host-side health watchdog with heartbeat-aware restart logic (from `templates/scripts/dev-machine-watchdog.sh`)
- `scripts/dev-machine-monitor.sh` -- diagnostic monitor with 5 failure-pattern detections (from `templates/scripts/dev-machine-monitor.sh`)

### Infrastructure Config (in project root)
- `docker-compose.dev-machine.yaml` -- Docker Compose config with host networking and volume structure (from `templates/docker-compose.dev-machine.yaml`)

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