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
