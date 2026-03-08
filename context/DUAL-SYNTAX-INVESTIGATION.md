# {{variable}} Dual-Syntax Investigation

**Date**: 2026-03-07  
**Reported by**: Alpha-3  
**Status**: Confirmed latent bug

## The Problem

Recipe templates use `{{}}` syntax for BOTH:
1. **Generation-time variables** (replaced once when artifacts are generated)
   - Examples: `{{project_name}}`, `{{state_file}}`, `{{max_outer_iterations}}`
   - Defined in `templates-reference.md`

2. **Runtime variables** (evaluated dynamically when recipe executes)
   - Examples: `{{initial_state.status}}`, `{{session_count}}`, `{{status}}`
   - NOT in `templates-reference.md`
   - Must remain as `{{}}` in generated files

## The Bug

The validation step in `generate-machine.md` (Step 9) checks for "no remaining {{}}":

```bash
# This validation would FAIL incorrectly because it sees {{initial_state.status}}
# in the generated file and thinks generation is incomplete!
grep -r '{{' .dev-machine/ && echo "ERROR: Unsubstituted variables!" && exit 1
```

This false-positive validation failure would make machine generation appear broken even when it's correct.

## Root Cause

**No documented distinction mechanism in generator**. The instructions don't explicitly state:
- Which variables should be replaced
- Which should be left as-is
- How validation should handle runtime variables

The whitelist approach (only replace variables in `templates-reference.md`) is likely intended, but it's not enforced or validated correctly.

## Missing Documentation

1. `templates-reference.md`: No section listing "Variables NOT to Replace"
2. `generate-machine.md` Step 5: Vague about "replace all {{variable}} placeholders" without distinguishing types
3. `generate-machine.md` Step 9: Validation doesn't account for runtime variables

## Solution Required

### 1. Update `templates-reference.md`

Add a new section:
```markdown
## Runtime Variables (Do NOT Replace)

These variables are evaluated at **runtime** during recipe execution. They must remain 
as `{{}}` in the generated files:

| Variable | Description | First Used |
|----------|-------------|------------|
| `{{initial_state.status}}` | Project health status from STATE.yaml | `check-health` step |
| `{{initial_state.blockers}}` | Project blockers list from STATE.yaml | `check-health` step |
| `{{initial_state.phase}}` | Current project phase | iteration recipe |
| `{{session_count}}` | Session iteration counter | work-loop step |
| `{{status}}` | Current machine status (healthy/blocked) | while conditions |
| `{{iteration_result.*}}` | Output from previous iterations | loop context |

These follow the pattern `{{variable.path}}` and reference data from recipe context,
not project design. **Do not replace these during generation.**
```

### 2. Update `generate-machine.md` Step 5

Change from:
```markdown
Replace all `{{variable}}` placeholders with values from the design
```

To:
```markdown
Replace ONLY generation-time variables listed in `templates-reference.md` (required and optional sections).
Leave all other `{{}}` expressions untouched — these are runtime variables evaluated during recipe execution.

To be safe, use a whitelist approach: only replace variables you explicitly recognize from the reference.
```

### 3. Fix Validation (Step 9)

Change from:
```bash
# WRONG: detects runtime variables and fails
grep -r '{{' .dev-machine/ && echo "ERROR: Unsubstituted variables!" && exit 1
```

To:
```bash
# CORRECT: only check for unsubstituted generation-time variables
GENERATION_VARS="project_name|project_dir|state_file|context_file|specs_dir|build_command|test_command|architecture_spec|max_features_per_session|max_outer_iterations|max_fix_iterations|cf_backoff|base_image|uv_version|user_home|username|system_packages|container_name|image_name|node_setup|python_dev_tools"

UNREPLACED=$(grep -rE "{{($GENERATION_VARS)}}" .dev-machine/*.yaml)
if [ -n "$UNREPLACED" ]; then
    echo "ERROR: Unsubstituted generation-time variables found:"
    echo "$UNREPLACED"
    exit 1
fi

echo "✓ All generation-time variables have been replaced"
```

## Impact

- **Severity**: Medium (latent — only manifests during machine generation validation)
- **Affected code**: `generate-machine.md` mode (when users run `/generate-machine`)
- **User impact**: False validation failures claiming generation failed when it actually succeeded
- **Fix complexity**: Documentation update + validation logic fix

## Testing

After fix, verify:
1. Generated recipes contain `{{initial_state.status}}`, `{{session_count}}`, etc.
2. Validation passes (no false "Unsubstituted variables" errors)
3. Generated recipes execute successfully (runtime variables resolve correctly)
