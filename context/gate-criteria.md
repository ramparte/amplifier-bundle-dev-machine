# Admissions Gate Criteria

Five gates determine whether a problem is suitable for an autonomous development machine.
Each gate produces a 0-100% confidence score.

## Scoring Rules

- **Below 50%:** Hard stop. The problem cannot proceed until this gate is remediated. Provide specific remediation guidance.
- **50-75%:** Proceed with caution. Flag the risk explicitly. The user decides whether to continue.
- **Above 75%:** Confident. Proceed.

The admissions advisor MUST be transparent about scores. No rounding up. No optimism bias.
If three or more gates are below 75%, recommend the user address them before proceeding.

---

## Gate 1: Decomposability

**Question:** Can the problem be broken into hundreds of small, independently implementable and testable units of work?

**High confidence (75-100%) signals:**
- Clear module/component boundaries already exist or are obvious
- Features within modules are independent (minimal cross-cutting concerns)
- Each feature can be specified in <2 pages
- Features follow repeating patterns (CRUD, UI components, API endpoints)
- The user can list 10+ concrete features off the top of their head

**Medium confidence (50-74%) signals:**
- Modules are identifiable but boundaries are fuzzy
- Some features have deep cross-module dependencies
- The user can describe features but they vary widely in scope
- Some features require coordinated changes across 3+ modules

**Low confidence (0-49%) signals:**
- The problem is a single monolithic algorithm or pipeline
- Features are deeply interconnected (changing one breaks many)
- Most features require novel design, not pattern application
- The user describes the work as "it all has to come together at once"
- Fewer than 50 identifiable features

**Remediation:** Identify natural boundaries. Consider breaking the problem into a smaller initial scope. Look for the "inner loop" that can be built first.

---

## Gate 2: Verifiable Correctness with Speed

**Question:** Can each unit of work be verified automatically with fast feedback?

**High confidence (75-100%) signals:**
- Established test framework exists for the tech stack
- Test execution takes seconds (unit) to minutes (integration)
- Type system catches structural errors (TypeScript, Rust, Go, etc.)
- CI/CD pipeline exists or can be trivially set up
- Clear definition of "correct" for each feature type

**Medium confidence (50-74%) signals:**
- Test framework exists but coverage is minimal
- Some features have clear correctness criteria, others are subjective
- Build/test cycle takes 2-5 minutes
- Type system is present but loosely used

**Low confidence (0-49%) signals:**
- No test framework or testing culture
- Correctness is primarily visual/subjective (design work, creative writing)
- Build/test cycle takes >10 minutes
- No type system and dynamic language with no linting
- "You have to run it and look at it to know if it's right"

**Remediation:** Set up a test framework. Add a type checker or linter. Define acceptance criteria templates. Consider if the verification gap can be addressed by a QA machine.

---

## Gate 3: Sufficient Architecture

**Question:** Is there enough architectural clarity to write a "constitution" that prevents drift across hundreds of features?

**High confidence (75-100%) signals:**
- Clear data model exists or can be defined
- Technology choices are made and rationale is understood
- Module boundaries are defined with explicit interfaces
- Key patterns are established (state management, data flow, error handling)
- The user can explain the system's architecture in 10 minutes

**Medium confidence (50-74%) signals:**
- Data model exists but has known gaps
- Some technology choices are tentative
- Module boundaries are roughly known but interfaces aren't formalized
- Some patterns are established, others are ad hoc
- "We know roughly how it works but haven't written it down"

**Low confidence (0-49%) signals:**
- No data model -- "we'll figure it out as we go"
- Technology choices are still being evaluated
- No module boundaries -- "it's all one thing right now"
- No established patterns
- The user can't explain the architecture without hand-waving

**Remediation:** Run a focused architecture session. You don't need everything -- you need enough to write a 30-50 page constitution that covers data model, module boundaries, technology choices, and key interfaces. The architecture can be progressive (design the first 3 modules well enough to start, design more later).

**Important:** Architecture does NOT need to be exhaustive. The word4 project had a 947-line architecture spec, but it was written in 1 hour and evolved. "Sufficient" means: enough to prevent drift, not enough to anticipate everything.

---

## Gate 4: Functioning Toolchain

**Question:** Do the build and test commands work? Can a fresh session run them?

**High confidence (75-100%) signals:**
- `build_command` runs and succeeds from a clean state
- `test_command` runs and reports results
- Commands are fast (<2 minutes for build, <5 minutes for full test suite)
- No manual setup required beyond initial clone
- CI/CD is configured or trivially configurable

**Medium confidence (50-74%) signals:**
- Build command works but is slow (>5 minutes)
- Test command works but only for some modules
- Some manual setup required (environment variables, local services)
- "It works on my machine" but setup isn't documented

**Low confidence (0-49%) signals:**
- No build command exists yet
- No test command exists yet
- Setup requires multiple manual steps that aren't documented
- The project hasn't been bootstrapped (no package.json, Cargo.toml, etc.)
- "We haven't set up the project yet"

**Remediation:** Bootstrap the project scaffold. This CAN be the machine's first task -- but the toolchain must work before the machine can build features. Set up: package manager, build command, test runner, type checker. Verify they run cleanly.

---

## Gate 5: Spec Quality

**Question:** Can initial feature specs be written at sufficient quality for machine consumption?

**High confidence (75-100%) signals:**
- Existing specs (PRDs, user stories) contain concrete details
- Features can be specified with: interfaces, acceptance criteria, edge cases, files to modify
- The user has domain knowledge to review specs for accuracy
- Spec writing follows a repeatable template
- A sample spec can be written and reviewed in <15 minutes

**Medium confidence (50-74%) signals:**
- Specs exist but are high-level ("add user authentication")
- Features can be described but acceptance criteria are vague
- Domain knowledge exists but isn't documented
- "We know what we want but haven't written it down precisely"

**Low confidence (0-49%) signals:**
- No specs exist -- "we're making it up as we go"
- Features can't be described without extensive discussion
- No domain expert available to review specs
- Requirements change frequently and unpredictably
- "We'll know it when we see it"

**Remediation:** Write 3-5 sample specs using the feature spec template. Have a domain expert review them. If the specs are too vague, the problem may need more product definition before a machine can build it.

---

## Assessment Output Format

The admissions advisor produces a `.dev-machine-assessment.md` file:

```
# Dev Machine Assessment

**Project:** [name]
**Date:** [ISO date]
**Overall Verdict:** PROCEED / PROCEED WITH CAUTION / NOT READY

## Gate Scores

| Gate | Score | Verdict |
|------|-------|---------|
| 1. Decomposability | XX% | PASS/CAUTION/FAIL |
| 2. Verifiable Correctness | XX% | PASS/CAUTION/FAIL |
| 3. Sufficient Architecture | XX% | PASS/CAUTION/FAIL |
| 4. Functioning Toolchain | XX% | PASS/CAUTION/FAIL |
| 5. Spec Quality | XX% | PASS/CAUTION/FAIL |

## Per-Gate Analysis

### Gate 1: Decomposability (XX%)
[Evidence and reasoning]

### Gate 2: Verifiable Correctness (XX%)
[Evidence and reasoning]

...

## Remediation Plan (if any gates < 50%)
[Specific steps to address failing gates]

## Recommended Next Steps
[What to do next based on the assessment]
```