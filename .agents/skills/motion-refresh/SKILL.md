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

**Research animation trends and rerank the motion library by relevance and popularity.**

Scores the 25 existing patterns in `.Codex/motion-library/` against current web animation trends via web research. Assigns `trend_score` (1–10), `status` (trending/evergreen/declining/emerging), and sources to each pattern. Detects trend gaps and suggests new patterns for `/motion-discover`.

## When to use

- Run periodically (monthly/quarterly) to keep pattern relevance current
- Before major skill updates to ensure they reference hot patterns
- When you suspect a pattern has become dated
- To audit which patterns are evergreen vs. declining

## Workflow

### Pre-flight — Start timer

Run via Bash and save the output as `TASK_START`:
```
TASK_START=$(python .Codex/scripts/query_cost.py --stamp)
```

### Phase 1: Web Research

Search for current animation trends across multiple sources:
- **GSAP/CSS release notes** — new capabilities, performance improvements
- **Design community surveys** — CSS-Tricks, State of CSS, Awwwards
- **GitHub trending** — popular animation libraries and repos
- **Design blogs** — Codrops, Smashing Magazine, design agency trend reports
- **Browser specs** — View Transitions, CSS Scroll-driven Animations, new APIs

Produce a ranked list of "what's hot in March 2026" with citations.

### Phase 2: Rerank Existing Patterns

For each pattern in `.Codex/motion-library/catalog.yaml`:

1. **IMPORTANT: Load only catalog.yaml + trends-overview.md during Phase 2. Do NOT open any pattern folders** (no index.md, spec.yaml, or snippet reads)
   - The catalog `name` + `triggers` + `components` fields contain structural metadata
   - The trends-overview.md provides narrative context per pattern ("what it is", "best for", "when NOT to use")
   - Folder opens are unnecessary and token-expensive
2. Compare each pattern's context (from trends-overview.md) + triggers (from catalog.yaml) against Phase 1 research findings
3. Assign:
   - `trend_score` (1–10 scale)
   - `status`: `trending` | `evergreen` | `declining` | `emerging`
   - `popularity_signal`: `high` | `medium` | `low`
   - `sources`: list of source labels/URLs used
   - `last_reviewed`: current month (YYYY-MM)

4. Skip any pattern with `manual_override: true` in `catalog.yaml`
5. Write updated trend fields (`trend_score`, `status`, `popularity_signal`, `last_reviewed`) back into each matching pattern entry in `.Codex/motion-library/catalog.yaml`. Match by `id`. Respect `manual_override: true` — skip those entries.

6. **Update `trends-overview.md`** — for each pattern whose score or status changed:
   - Update the header bracket: `[category | framework | status score/10]`
   - Update the summary table row at the bottom (Status column)
   - If research reveals the pattern's "When NOT to use" guidance should change, update that line too
   - Update the `Last updated:` date at the top of the file

**Token optimization:** This approach uses catalog.yaml (structural metadata) + trends-overview.md (narrative context) instead of 25 folder reads during Phase 2 reranking.

**Scoring rubric:**

| Score | Meaning | Status |
|-------|---------|--------|
| 9–10 | Industry standard, actively trending, high adoption | trending |
| 7–8 | Stable, widely used, good modern support | evergreen or trending |
| 5–6 | Niche or declining adoption, still viable | evergreen or declining |
| 1–4 | Outdated, low adoption, rarely used | declining |
| ? | Brand new, under 1 month old | emerging |

### Phase 3: Regenerate scores.yaml Inverted Index

After updating trend scores in catalog.yaml, regenerate the RAG inverted index:

1. Read the updated `catalog.yaml`
2. For each pattern, for each entry in its `components` list, add the pattern `id` to the matching element bucket in the index
3. Within each element bucket, sort patterns by `trend_score` descending; exclude any pattern with `status: declining`
4. Apply site-context specificity:
   - Patterns with `components` containing `hero` or `heading` → distribute across `hero.saas`, `hero.portfolio`, `hero.marketing` buckets using the pattern's "Best for" line in `trends-overview.md`:
     - `saas` bucket: "Best for" mentions SaaS, B2B, dashboard, enterprise, product contexts
     - `portfolio` bucket: "Best for" mentions portfolio, agency, creative, showcase, luxury contexts
     - `marketing` bucket: "Best for" mentions marketing, campaign, landing, brand contexts
     - Add to all three if the pattern is general-purpose (e.g., "any repeating content", "any interactive surface")
   - Patterns with `components` containing `card` → distribute across `card.saas`, `card.portfolio` buckets
   - All patterns go into their element's `any` bucket as fallback
5. Preserve the `site_contexts` personality block — only update it if a pattern's status changed to/from `declining`
6. Update the `# Last updated: YYYY-MM-DD` header comment with today's date
7. Write the result to `.Codex/motion-library/scores.yaml`

### Phase 4: Gap Detection

If Phase 1 research surfaced 2+ animation trends with **no matching pattern** in `catalog.yaml`:

1. List them as gap candidates
2. Report to user: "These 3 trends have no pattern yet. Consider `/motion-discover` to generate them."
3. Do NOT auto-generate — user decides

If a `declining` pattern (score 4–5) has a clear modern replacement in research, flag it for potential deprecation.

### Phase 5: Metrics

Run via Bash:
```
python .Codex/scripts/query_cost.py --since "$TASK_START"
```
Output the result line directly. If unavailable: _Metrics unavailable — run `python .Codex/scripts/query_cost.py --since <start-timestamp>` manually._

---

## Integration with other skills

**motion-dev** — reads `scores.yaml` as a pre-computed inverted index at invocation time. Direct element-type lookup, no scoring algorithm. Never reads `catalog.yaml` at invocation time.

**motion-discover** — checks `catalog.yaml` for duplicates before generating new patterns. Appends new pattern entries with placeholder trend fields, then relies on `/motion-refresh` to regenerate `scores.yaml`.

**motion-enhance** — uses the pre-sorted `scores.yaml` index for prioritization order and reads `catalog.yaml` only when it needs extra metadata for shortlisted patterns.

---

## Manual override

To prevent a pattern's scores from being updated on the next refresh:

```yaml
# In .Codex/motion-library/catalog.yaml
  - id: my-pattern
    ...
    manual_override: true
    notes: "Custom tuning for our brand"
```

The skill will skip this entry when reranking.

---

## Output

- Updated `.Codex/motion-library/catalog.yaml` with fresh trend fields for all 25 patterns
- Updated `.Codex/motion-library/trends-overview.md` with revised scores, statuses, and narrative context
- Regenerated `.Codex/motion-library/scores.yaml` inverted index from updated catalog
- Conversation output: list of patterns whose scores changed significantly
- Gap report: any trends found with no matching pattern (if applicable)
- Suggestions: patterns flagged for deprecation (if any)

---

## Example: Running the refresh

```
User: /motion-refresh

Codex (motion-refresh):
[Phase 1] Researching animation trends in CSS, GSAP, View Transitions, design surveys...
[Phase 2] Reranking 25 patterns against findings...
[Phase 3] Regenerating scores.yaml inverted index...
[Phase 4] Checking for gaps...

✅ Updated 25 patterns in catalog.yaml
✅ Regenerated scores.yaml inverted index

Notable changes:
• scroll-trigger-reveal: 9/trending (stable leader)
• view-transitions-api: 8/emerging (new W3C spec, rising fast)
• card-flip-3d: 6/declining (outdated 3D effect)

Gap detected:
• "GPU texture morphing" — no pattern yet. Consider generating?

All ranking changes written to .Codex/motion-library/catalog.yaml and `.Codex/motion-library/scores.yaml` regenerated
```

---

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
