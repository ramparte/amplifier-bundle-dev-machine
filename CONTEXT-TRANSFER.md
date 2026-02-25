# Dev Machine Bundle -- Context Transfer

> This document captures all design decisions and project state for
> `amplifier-bundle-dev-machine`. A fresh session reads this to continue.

## Current State

- **Repo:** `ramparte/amplifier-bundle-dev-machine`
- **Location:** `~/dev/ANext/amplifier-bundle-dev-machine`
- **Branch:** `main`
- **Status:** Plan written and committed. No implementation yet.
- **Plan:** `docs/plans/2026-02-25-dev-machine-bundle-implementation.md` (3,087 lines, 20 tasks, 7 groups)

## What This Project Is

An Amplifier bundle that generalizes the autonomous development machine pattern
proven by word4 (278 features, 106 sessions, 5.5 days, ~89K LOC). It helps
Amplifier users assess whether their problem fits, design a machine, and
generate the machine artifacts into their project repo.

**Target audience:** Amplifier users generally (not just Sam).

## Immediate Next Action

Execute the implementation plan. The plan is at:
`docs/plans/2026-02-25-dev-machine-bundle-implementation.md`

It has 20 tasks across 7 groups. Each task has exact file paths, complete file
content, and verification steps. Execute them in order, committing after each
logical unit.

The plan references word4 files for the recipe templates. Those are at:
`~/dev/ANext/word4/` -- specifically the recipe YAML files and
`specs/working-session-instructions.md`.

A prior attempt to run this via the `superpowers:recipes/subagent-driven-development.yaml`
recipe failed with a parsing error. Manual execution (reading the plan and
implementing task by task) is the recommended approach.

## Design Decisions (All Validated)

### Bundle Structure

Three modes, three agents, context files, and template files:

```
amplifier-bundle-dev-machine/
├── bundle.md                    # Bundle manifest
├── README.md
├── agents/
│   ├── admissions-advisor.md    # Evaluates problems, guides remediation
│   ├── machine-designer.md      # Runs the founding session
│   └── machine-generator.md     # Stamps out .dev-machine/ directory
├── modes/
│   ├── admissions.md            # /admissions mode
│   ├── machine-design.md        # /machine-design mode
│   └── generate-machine.md      # /generate-machine mode
├── context/
│   ├── pattern.md               # The proven autonomous dev machine pattern
│   ├── gate-criteria.md         # Five gates with confidence intervals
│   ├── templates-reference.md   # How templates work
│   └── word4-lessons.md         # What worked, what failed
├── templates/
│   ├── recipes/                 # 6 parameterized recipe YAML files
│   ├── STATE.yaml
│   ├── CONTEXT-TRANSFER.md
│   ├── SCRATCH.md
│   ├── working-session-instructions.md
│   └── feature-spec-template.md
└── docs/
    └── plans/
```

### Three Modes (Superpowers-style)

1. `/admissions` -- Evaluate the problem against 5 gates. Guided remediation
   if gaps exist. Hard stop below 50% confidence. Output: assessment file.
2. `/machine-design` -- Guided founding session. Requires passing assessment.
   Templated core from word4 pattern + domain-specific design. Output: design
   document.
3. `/generate-machine` -- Stamps out `.dev-machine/` directory. Requires
   validated design. Mechanical artifact generation.

### Five Admissions Gates (Confidence Intervals)

Each gate produces a 0-100% confidence score:
- Below 50%: HARD STOP, system will not proceed, user cannot override
- 50-100%: system proceeds but reports confidence transparently

1. **Decomposability** -- Can be broken into isolated units an LLM can handle
   in bounded sessions. Could be 5 units or 500.
2. **Verifiable correctness with speed** -- Automated verification with fast
   feedback. Hard-ish gate if cycle is very slow.
3. **Sufficient architecture** -- Progressive, not exhaustive. Enough to start,
   credible path to JIT detailed specs. Not "spec everything upfront."
4. **Functioning toolchain** -- Build/test commands work. Project scaffold can
   be the machine's first task, but tools must be installed.
5. **Spec quality** -- Initial specs meet the quality bar for machine
   consumption. Can be produced during the admissions process.

### Gate Enforcement

File-based with confidence intervals:
- Admissions produces `.dev-machine-assessment.md` with per-gate scores
- `/machine-design` checks for this file before allowing entry
- Machine design produces `.dev-machine-design.md`
- `/generate-machine` checks for this file before allowing entry

### Pre-existing Input

The system accepts existing artifacts (product specs, architecture docs,
existing codebases) as starting points. Reads and evaluates them against
criteria, gives credit where met, identifies gaps. Meets the user where
they are.

### Templated Core (NOT reinvented each time)

These come from the proven word4 pattern with light customization:
- STATE.yaml schema
- Working session instructions (protocol)
- CONTEXT-TRANSFER.md format
- Recipe structure (outer/inner loop, health check, QA)

### Domain-Specific (designed per-project in founding session)

- Architecture spec (the constitution) -- genuinely unique
- Module boundaries and spec templates
- First batch of specs
- QA machine configuration
- Bootstrap task (if needed)

### Generated Machine Location

Lives in `.dev-machine/` in the user's project repo:

```
project/
├── .dev-machine/
│   ├── build.yaml                    # Execution machine outer loop
│   ├── iteration.yaml                # Execution machine inner loop
│   ├── health-check.yaml             # Health check outer loop
│   ├── fix-iteration.yaml            # Health check fix cycle
│   ├── qa.yaml                       # QA machine outer loop
│   ├── qa-iteration.yaml             # QA machine inner loop
│   ├── working-session-instructions.md
│   └── feature-spec-template.md
├── STATE.yaml              # At project root (project state, not infra)
├── CONTEXT-TRANSFER.md     # At project root
└── SCRATCH.md              # At project root
```

No runtime dependency on the dev-machine bundle.

### Recipe Templates Are Real YAML (Core IP)

The 6 recipe template files are real, parameterized, working YAML -- not stubs.
They use `{{variable}}` placeholders (build_command, test_command, state_file,
project_dir, etc.) and are generalized from the word4 recipes which ran 106+
sessions successfully. The plan has the complete content for each.

## Key References

| Document | Location | What It Contains |
|----------|----------|-----------------|
| Implementation plan | `docs/plans/2026-02-25-dev-machine-bundle-implementation.md` | 20 tasks, complete file content for every artifact |
| word4 pattern doc | `~/dev/ANext/word4/docs/autonomous-development-machine-pattern.md` | The full pattern to adapt into context files |
| word4 recipes | `~/dev/ANext/word4/word4-build.yaml` etc. | The proven recipes to generalize into templates |
| word4 session instructions | `~/dev/ANext/word4/specs/working-session-instructions.md` | The proven session protocol to template |
| word4 critical assessment | `~/dev/ANext/word4/docs/critical-assessment.md` | Lessons learned for word4-lessons.md context |
| word4 architecture overview | `~/dev/ANext/word4/docs/architecture-overview.md` | Reference for what a good architecture doc looks like |

## Origin

This project was designed in a brainstorm session on 2026-02-25 (session
557a519f in the word4 project directory). The brainstorm covered:
- Who the users are (Amplifier users generally)
- The three-mode structure
- The five admissions gates with confidence intervals
- Hard gate philosophy (below 50% = stop, no override)
- Guided remediation (help users get ready, don't just reject)
- Templated core vs domain-specific design
- Pre-existing input acceptance
- Generated machine in `.dev-machine/` directory
- Recipe templates as the core IP (must be real YAML, not stubs)

All decisions were validated by the user (Sam Schillace / ramparte).
