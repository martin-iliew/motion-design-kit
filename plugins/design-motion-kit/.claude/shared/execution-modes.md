# Execution Modes

These mode rules apply to:

- `design-build`
- `design-upgrade`
- `motion-build`
- `motion-upgrade`

Default mode is `balanced`.

## `fast`

- use only compiled runtime outputs
- do not open overview or trend prose unless the request explicitly requires it
- prefer the smallest safe design or motion move set
- do not introduce premium-only embellishments

## `balanced`

- use compiled runtime outputs first
- allow one selective fallback read when the compiled layer is insufficient
- preserve clear hierarchy and implementation simplicity
- this is the default production mode

## `premium`

- allow richer composition after the compiled layer has been checked
- one extra reference read is allowed when it materially improves the result
- design still owns structure; motion still owns behavior
- never use live trend research during build or upgrade

## Cross-Family Rules

- `design-*` must emit `design-decision-pack.yaml` and `motion-hints.yaml` before implementation work starts
- `motion-*` must consume `design-decision-pack.yaml` and `motion-hints.yaml` when those files exist
- greenfield work may invoke the internal `vite-react-bootstrap` skill before design-system processing
- all generated code must use the derived design-system tokens instead of raw values
