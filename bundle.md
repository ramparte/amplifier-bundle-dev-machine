---
bundle:
  name: dev-machine
  version: 0.1.0
  description: |
    Guides users through evaluating a problem for autonomous development,
    designing a development machine, and generating machine artifacts.
    Based on the proven pattern from word4 (278 features, 106 sessions, 5.5 days).

includes:
  - behavior: ./behaviors/dev-machine.yaml

agents:
  include:
    - admissions-advisor
    - machine-designer
    - machine-generator

context:
  include:
    - "@dev-machine:context/pattern.md"
    - "@dev-machine:context/gate-criteria.md"
---

# Dev Machine Bundle

Build autonomous development machines for your projects.

This bundle provides three modes that guide you through a hard-gated progression:

1. **`/admissions`** -- Evaluate whether your problem is suitable for an autonomous development machine. Produces a confidence-scored assessment across five gates.
2. **`/machine-design`** -- Run a founding session to design your machine: architecture spec, module boundaries, state schema, recipe configuration, and first batch of feature specs.
3. **`/generate-machine`** -- Stamp out the `.dev-machine/` directory in your project with all recipes, state files, and templates ready to run.

The generated machine lives in your project repo with zero runtime dependency on this bundle.

## The Pattern

The autonomous development machine pattern was proven by the word4 project:
- 278 features implemented autonomously
- 106 working sessions across 5.5 days
- ~89,000 lines of TypeScript
- 3,714 passing tests
- 445 git commits

The pattern works by running disposable working sessions that read state from files,
do bounded work (3-5 features), persist state, and exit. No session runs long enough
to degrade. The recipe orchestrator is lightweight -- it doesn't accumulate LLM context.
The "memory" lives in STATE.yaml and CONTEXT-TRANSFER.md.

@dev-machine:context/pattern.md
