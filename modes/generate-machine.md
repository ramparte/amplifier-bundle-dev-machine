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
