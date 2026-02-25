# Feature Spec Template

> Use this template when writing feature specs for the development machine.
> Every field must be filled in. The machine implements specs literally.

---

# F-XXX: [Feature Name]

## 1. Overview

**Module:** [which module this feature belongs to]
**Priority:** [P0/P1/P2]
**Depends on:** [list feature IDs this depends on, or "none"]

[2-3 sentences: what this feature does and why it's needed]

## 2. Requirements

### Interfaces

```
[TypeScript/Python/Rust/etc. signatures for any new or modified interfaces]
[Include types, function signatures, class definitions]
```

### Behavior

- [Concrete behavior rule 1]
- [Concrete behavior rule 2]
- [Keyboard shortcuts, API responses, state transitions, etc.]

## 3. Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| AC-1 | [Specific, testable criterion] | [How to verify: unit test, integration test, manual check] |
| AC-2 | [Specific, testable criterion] | [How to verify] |
| AC-3 | [Specific, testable criterion] | [How to verify] |

## 4. Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| [Edge case 1] | [What should happen] |
| [Edge case 2] | [What should happen] |

## 5. Files to Create/Modify

| File | Action | Contents |
|------|--------|----------|
| `path/to/new-file.ts` | Create | [Description of what this file contains] |
| `path/to/existing.ts` | Modify | [Description of changes] |
| `tests/path/to/test.ts` | Create | [Tests for this feature] |

## 6. Dependencies

- [Package/library dependencies needed]
- [Or "No new dependencies"]

## 7. Notes

- [Implementation caveats]
- [Future work deferred]
- [Warnings about gotchas]
