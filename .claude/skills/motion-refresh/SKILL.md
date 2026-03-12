---
name: motion-refresh
description: >
  Use this skill whenever the user wants to rerank, refresh, or rescore the
  motion library against current web animation trends. Trigger on:
  "/motion-refresh", "refresh the motion library scores", "rerank the
  animation patterns", or any request to rescore the existing motion library
  and regenerate the lookup index used by the other motion skills.
---

# motion-refresh

Research current animation trends, score the full catalog, and regenerate the lookup index consumed by the motion skills.

## When to use

- After `/motion-discover` adds new patterns and they must become usable immediately
- On a monthly or quarterly refresh of the motion library
- Before tuning `motion-dev` or `motion-enhance` behavior against current patterns
- When a pattern family feels stale or overused and you need a rerank

## Workflow

### Pre-flight — Start timer

Run via Bash and save the output as `TASK_START`:
```
TASK_START=$(python .claude/scripts/query_cost.py --stamp)
```

### Phase 1: Research the current baseline

Research what is current **today** before scoring.

Order of operations:
- Official GSAP references first: `https://gsap.com/llms.txt` plus plugin-specific docs
- Recent design-community validation second: Codrops, strong agency examples, recent pattern roundups
- Browser/platform sources when browser-native APIs are involved

Capture:
- What is actively rising
- What is now table stakes
- What is becoming noisy or dated
- Which plugin families are showing up in premium builds right now

### Phase 2: Score the full catalog

Read `.claude/motion-library/catalog.yaml` and `.claude/motion-library/trends-overview.md`.

Default rule:
- Use `catalog.yaml` for structural metadata
- Use `trends-overview.md` for narrative context
- Open individual pattern folders only when a new family or plugin-specific pattern needs clarification that the overview cannot provide

For every catalog entry:
1. Match the pattern against the current baseline
2. Update only the trend fields unless metadata is missing
3. Preserve `description`, `sources`, `manual_override`, and `notes` unless you are explicitly repairing missing values
4. Respect `manual_override: true` and skip scoring changes for those entries

Fields to refresh:
- `trend_score`
- `status`
- `popularity_signal`
- `last_reviewed`
- `sources` when the existing list is empty or clearly outdated

Status guidance:
- `trending`: actively visible in premium 2026 builds
- `evergreen`: stable, still modern, not necessarily rising
- `emerging`: promising or newly visible, but not yet table stakes
- `declining`: dated, overused, or clearly replaced by better patterns

### Phase 3: Regenerate `scores.yaml`

After scoring `catalog.yaml`, regenerate `.claude/motion-library/scores.yaml` from the full catalog.

Rules:
- Include every component bucket represented in `catalog.yaml`
- Exclude patterns with `status: declining` from ranked lists
- Sort ranked lists by `trend_score` descending
- Preserve the `site_contexts` personality block
- Ensure the expanded component families remain available: `menu`, `tabs`, `accordion`, `modal`, `drawer`, `toast`, `tooltip`, `form`, `input`, `gallery`, `carousel`, `media`, `image`, `video`, `svg`, `icon`, `loader`, `timeline`, `progress-bar`, and `hotspot`

### Phase 4: Repair missing metadata when needed

If the catalog contains older entries with missing `description` or `sources`, backfill them while refreshing.

Do not leave the catalog in a mixed schema state.

### Phase 5: Gap detection

If research surfaces patterns that are clearly current but still missing from `catalog.yaml`:
- Report them as gap candidates
- Suggest `/motion-discover` for generation
- Do not auto-generate here unless the user explicitly asked for both discovery and refresh in the same pass

### Phase 6: Output

Output:
- Current catalog size
- Number of patterns rescored
- Notable movers (up or down)
- Any declining patterns worth deprecating
- Any discovery gaps worth generating next

Before reporting success, validate the rebuilt corpus:
```
python .claude/scripts/validate_motion_library.py --expected-count <current-catalog-size>
```
If validation fails, fix the catalog, overview, or scores index before stopping.

Example:

```
Refreshed motion library.

Catalog size: 75
Patterns rescored: 75
Index regenerated: yes

Notable movers:
- shared-element-gallery-expand -> 9 / trending
- card-flip-3d -> 5 / declining
- scrollsmoother-data-effects -> 9 / trending
```

### Metrics

Run via Bash:
```
python .claude/scripts/query_cost.py --since "$TASK_START"
```
Output the result line directly. If unavailable: _Metrics unavailable — run `python .claude/scripts/query_cost.py --since <start-timestamp>` manually._

---

## Integration with other skills

- `motion-dev` reads `scores.yaml` for ranked lookup, then opens the selected pattern folder's `spec.yaml` and snippet as the primary implementation source.
- `motion-enhance` derives its enrichment baseline from `scores.yaml`, then reads the shortlisted pattern folders directly.
- `motion-discover` writes new folders and catalog entries; `motion-refresh` makes them immediately usable by rebuilding `scores.yaml`.

---

## Output guarantees

After a successful run:
- `catalog.yaml` reflects the current trend fields for the full catalog
- `scores.yaml` reflects the current ranked lookup surface
- `trends-overview.md` stays aligned with the full catalog size and status labels
- No fixed-size assumptions remain in the refresh instructions

---

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
