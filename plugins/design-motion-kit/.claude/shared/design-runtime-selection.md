# Design Runtime Selection

Use the compiled design runtime before opening individual pattern folders.

## 1. Load shared inputs

Start with:

- `brief/brief.json`
- `.claude/design-library/scores.yaml`
- `.claude/design-library/site-baselines.yaml`

If `brief/design-decision-pack.yaml` already exists, update it instead of rebuilding the whole plan from scratch.

## 2. Detect page context

Use `brief.json` first. If the bundle is vague, infer from the page or request:

- `saas`
- `ai`
- `enterprise`
- `developer-tools`
- `ecommerce`
- `any`

## 3. Choose required surfaces

Use the site baseline for the chosen context to derive the minimum section set.

Treat surfaces as weak when they exist but fail:

- clarity
- proof density
- scanability
- CTA continuity

## 4. Select patterns cheaply

1. Read `.claude/design-library/scores.yaml`.
2. Match each required or weak surface against the page context.
3. Keep the top-ranked non-conflicting pattern.
4. Open only `spec.yaml`, `index.md`, and `composition.yaml` in the winning folder.

## 5. Emit structure before code

Convert winners into `brief/design-decision-pack.yaml` with:

- selected patterns by surface
- section order
- component inventory
- implementation notes

Then emit `brief/motion-hints.yaml` from the winning compositions before any motion or coder work begins.
