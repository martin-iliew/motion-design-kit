# Motion Library Pattern Catalog — Dynamic Reference

This file is intentionally minimal. Pattern baselines are derived dynamically at runtime.

---

## How Pattern Selection Works

**Do NOT use a hardcoded pattern list.** Instead, derive the baseline dynamically:

1. Load `.claude/motion-library/scores.yaml` — read `site_contexts` block for the detected site type's `prefer`/`avoid` lists
2. Load `.claude/motion-library/trends-overview.md` — read "When NOT to use" for each candidate
3. Collect all patterns from element-type buckets matching the detected site context
4. Rank by `trend_score` descending:
   - Score >= 8 → CRITICAL (must apply)
   - Score 7 → WARNING (apply if element exists)
   - Score <= 6 → SKIP (unless specifically requested)
5. Exclude any pattern with `status: declining`
6. Cross-check against trends-overview.md "When NOT to use" — downgrade if site context matches an avoid condition

This approach auto-updates when `/motion-refresh` changes pattern scores, instead of relying on stale hardcoded lists.

---

## Status Labels

- **APPLIED** = pattern was used
- **SKIPPED** = applicable but actively decided against (include reason)
- **N/A** = element/structure not present in file
- **ALREADY_ANIMATED** = element has existing GSAP (skipped to avoid conflicts)
