# Runtime Selection

Use the compiled runtime layer before opening individual pattern folders.

## 1. Detect page context

Infer the primary context from the request and existing page:

- `saas`: subscription software, demos, workflows, pricing
- `ai`: model, assistant, automation, inference, workspace, copilots
- `enterprise`: security, compliance, procurement, multi-team rollouts
- `developer-tools`: API, platform, infrastructure, docs-led acquisition
- `ecommerce`: catalog, product merchandising, checkout-oriented flows

If unclear, use `any`.

## 2. Detect missing or weak surfaces

Scan for the surfaces below:

- `hero`
- `proof`
- `metrics`
- `product`
- `features`
- `integrations`
- `pricing`
- `testimonial`
- `security`
- `faq`
- `cta`

Treat surfaces as weak when they exist but fail clarity, proof, or scannability.

## 3. Choose patterns cheaply

1. Read `.claude/design-library/scores.yaml`.
2. Match each missing or weak surface against the page context.
3. Keep the top-ranked pattern unless it clearly conflicts with the existing layout.
4. Open only the winning folder `spec.yaml` plus `snippet.html` and `index.md`.

## 4. Baseline checks

Read `.claude/design-library/site-baselines.yaml` only for page-level work or when choosing between two valid patterns.

Use it to answer:

- which sections are expected for this page type
- where proof should appear
- what style moves to avoid by default

## 5. Escalation rules

- `fast`: do not open `trends-overview.md`
- `balanced`: open `trends-overview.md` only if the compiled scores are tied or incomplete
- `premium`: open `trends-overview.md` when the page needs stronger composition choices or narrative sequencing
