# amplifier-bundle-dev-machine

An Amplifier bundle that helps you build autonomous development machines for your projects.

## Quick Start

1. Install the bundle in your Amplifier configuration
2. Run `/admissions` to evaluate your problem
3. Run `/machine-design` to design your machine
4. Run `/generate-machine` to stamp out the machine artifacts

## What It Does

This bundle guides you through a three-phase process:

**Phase 1: Admissions** -- Evaluates your problem across five gates (decomposability, verifiable correctness, sufficient architecture, functioning toolchain, spec quality). Each gate produces a 0-100% confidence score. Below 50% is a hard stop with remediation guidance.

**Phase 2: Machine Design** -- Runs a founding session where you design the machine: architecture spec, module boundaries, state schema, recipe configuration, working session protocol, and the first batch of feature specs.

**Phase 3: Generate Machine** -- Stamps out a `.dev-machine/` directory in your project repo containing all recipes, state files, and templates. The generated machine has zero runtime dependency on this bundle.

## Generated Output

```
your-project/
├── .dev-machine/
│   ├── build.yaml                  # Execution machine outer loop
│   ├── iteration.yaml              # Execution machine inner loop
│   ├── health-check.yaml           # Health check outer loop
│   ├── fix-iteration.yaml          # Health check fix cycle
│   ├── qa.yaml                     # QA machine outer loop (if applicable)
│   ├── qa-iteration.yaml           # QA machine inner loop (if applicable)
│   ├── working-session-instructions.md
│   └── feature-spec-template.md
├── STATE.yaml
├── CONTEXT-TRANSFER.md
└── SCRATCH.md
```

## The Pattern

Based on the word4 project: 278 features, 106 autonomous sessions, 5.5 days, ~89K LOC.

## License

MIT
