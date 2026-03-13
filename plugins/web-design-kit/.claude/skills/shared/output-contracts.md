# Output Contracts

Use these response shapes.

## web-build

- `Summary:` one paragraph on what changed and why
- `Patterns used:` flat list of selected library patterns
- `Files changed:` flat list
- `Notes:` only if there is a meaningful caveat

## web-upgrade

- `Summary:` one paragraph on the upgrade
- `Audit fixes:` flat list of key problems fixed
- `Enhancements:` flat list of patterns or sections added
- `Files changed:` flat list
- `Residual risks:` only if something could not be completed

## web-audit

- `Summary:` include CRITICAL / WARNING / INFO counts
- `Findings:` ordered by severity
- `Proposed fixes:` concrete patch-ready guidance
- `Next command:` only if redirecting to `/web-build` or `/web-upgrade`

## web-discover

- `Patterns added:` table with pattern, category, folder, snippet
- `Catalog size:` final count
- `Runtime refresh:` yes or no

## web-refresh

- `Catalog size:`
- `Patterns rescored:`
- `Runtime outputs regenerated:`
- `Notable movers:`
- `Discovery gaps:`
