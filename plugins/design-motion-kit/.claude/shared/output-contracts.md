# Output Contracts

Use these response shapes across the merged plugin.

## `design-build`

Report only:

- files changed or created
- mode used
- selected design patterns
- whether the brief bundle artifacts were generated
- one sentence on design-system enforcement

## `design-upgrade`

Report only:

- files changed
- mode used
- major audit issues fixed
- sections or patterns added
- whether the brief bundle artifacts were refreshed

## `design-audit`

Report only:

- severity counts
- ordered findings
- patch-ready fix guidance
- redirect to `/design-build` or `/design-upgrade` when appropriate

## `design-discover`

Report only:

- patterns added
- folder names
- catalog size
- whether runtime outputs were regenerated

## `design-refresh`

Report only:

- catalog size
- patterns rescored
- runtime outputs regenerated
- notable movers
- discovery gaps

## `motion-build`

Report only:

- target file
- mode used
- short Animation Plan
- whether design handoff files were consumed
- one sentence on major guardrails respected

## `motion-upgrade`

Report only:

- target file(s)
- mode used
- issue counts fixed
- motion added or skipped per major bucket
- whether design handoff files were consumed

## `motion-audit`

Report only:

- target file
- structured severity findings
- summary counts
- concrete fixes for every `CRITICAL` and `WARNING`
