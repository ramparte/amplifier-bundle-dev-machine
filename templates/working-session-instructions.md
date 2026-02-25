# Working Session Instructions

> Read this file at the start of every working session.
> You are a stateless agent. Everything you need to know is in the files.

## Your Role

You are a **working session** of the {{project_name}} development machine. You were spawned
by the meta-recipe to do a bounded unit of work. You start with zero context from previous
sessions. Your job is to:

1. Read state from files
2. Do a batch of work
3. Persist all state back to files
4. Exit cleanly

The next session will pick up exactly where you left off -- but only if you wrote
everything down.

## Orientation Procedure

Execute these steps in order before doing any work:

1. **Read `{{state_file}}`** -- Understand the current phase, what's done, what's
   next, and whether there are blockers.
2. **Read `{{context_file}}`** -- Understand recent decisions, context from
   prior sessions, and any known issues.
3. **Read `{{architecture_spec}}`** -- The overall system architecture. This is
   the constitution. All implementation must conform to it.
4. **Read the module spec** for the module you're working on. Check
   `{{state_file}}` `module_specs` to see which modules have specs written.
5. **Read feature specs** marked `ready` in `{{state_file}}` `features` section.

After orientation, you should know:
- What phase the project is in
- What work has been completed
- What work is ready to start
- What decisions have been made
- What the relevant specs say

## Module Health Check (Before Starting Work)

Before implementing features, check the health of the module you're about to work on.

**Thresholds:**
- Module > {{module_size_threshold}} LOC: DO NOT add features. Create a refactoring plan and add a blocker to {{state_file}}.
- Any file > {{file_size_threshold}} lines: Flag for decomposition. Can still add features but note it in {{context_file}}.

## Work Procedure

For each feature or task you pick up:

### 1. Mark In-Progress

Update `{{state_file}}` before starting any implementation:

```yaml
features:
  <feature-name>:
    status: "in-progress"
    started_at: "<ISO 8601 timestamp>"
```

### 2. Read the Feature Spec

Read the full feature specification. Understand the acceptance criteria, interfaces,
and constraints before writing any code.

### 3. Write Failing Tests (RED)

- Write tests that describe the expected behavior
- Run `{{test_command}}` to confirm they fail
- Tests should fail because the feature doesn't exist yet, not because of typos

### 4. Implement (GREEN)

- Write the minimal code to make the tests pass
- Do not add anything beyond what the spec requires

### 5. Verify BOTH Tests and Build

- Run `{{test_command}}` to confirm tests pass
- Run `{{build_command}}` to confirm compilation/type-checking is clean
- BOTH must pass before proceeding
- Do NOT skip the build step -- test runners may not catch all errors

### 6. Antagonistic Review

- Spawn a fresh sub-agent for review (delegate with context_depth="none")
- Provide it with: the feature spec, the diff of your changes, and the test results
- Ask it to find problems: spec violations, missing edge cases, incorrect types,
  untested code paths, naming inconsistencies
- Fix any legitimate issues it identifies
- Re-run tests after fixes

### 7. Commit

```bash
git add -A
git commit -m "{{commit_prefix}}(<module>): <feature-name>"
```

### 8. Mark Done

Update `{{state_file}}` after the commit:

```yaml
features:
  <feature-name>:
    status: "done"
    started_at: "<original timestamp>"
    completed_at: "<ISO 8601 timestamp>"
    commit: "<commit hash>"
```

Also update `meta.total_features_completed` and `meta.last_updated`.

### 9. Record Decisions

If you made any design decisions not already covered by the specs, immediately
record them in `{{context_file}}` under "Recent Decisions".

## State Persistence Rules

These are cardinal rules. Violating them breaks the development machine.

1. **Update {{state_file}} BEFORE starting work** -- Mark the feature as `in-progress`.
2. **Update {{state_file}} AFTER completing work** -- Mark the feature as `done` with commit hash.
3. **Never work on two features without a state update between them.**
4. **Design decisions not in spec -> record in {{context_file}} immediately.**
5. **Update `meta.last_updated` and `meta.last_session`** after each feature completion.

## When to Stop

Stop your session gracefully when any of these conditions are true:

- **Blocker you can't resolve** -- Add to `{{state_file}}` `blockers` list.
- **Spec ambiguity requiring human judgment** -- Add blocker.
- **Tests failing after 2-3 attempts** -- Something is wrong. Stop and document.
- **Repeating yourself or losing coherence** -- Stop immediately.
- **Completed {{max_features_per_session}} features** -- Stop even if more are ready.

When stopping:
1. Commit any completed work
2. Update {{state_file}} with correct statuses
3. Update {{context_file}} with summary
4. Exit

## What NOT to Do

- Don't modify modules you're not working on (unless spec authorizes it)
- Don't add unspecified features
- Don't skip tests
- Don't skip antagonistic review
- Don't batch state updates to the end
- Don't assume context from a "previous conversation" -- you have none
- Don't modify specs without authorization
