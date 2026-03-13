# Motion Library Pattern Catalog — Runtime Baseline Reference

This file is intentionally minimal. Runtime selection is derived from the compiled selector layer first.

---

## How Pattern Selection Works

**Do NOT use a hardcoded pattern list.** Instead, select patterns in stages:

1. Load `.claude/motion-library/site-baselines.yaml`
2. Load `.claude/motion-library/trend-watchlist.yaml`
3. Detect:
   - site type
   - element buckets present
   - active page signals
4. For each detected bucket, choose the first ranked candidate whose `when` conditions are satisfied
5. Reject that candidate if its `trend-watchlist.yaml` `avoid_when` conditions are active
6. Fall through to the next candidate
7. Read only the winning pattern folder's `spec.yaml` + snippet

Escalation rules:
- Use `.claude/motion-library/scores.yaml` only when the compiled baseline cannot make a safe page-specific choice
- Use `.claude/motion-library/trends-overview.md` only for ambiguity, premium/high-stakes pages, or watchlist clarification

---

## Status Labels

- **APPLIED** = pattern was used
- **SKIPPED** = applicable but actively decided against (include reason)
- **N/A** = element/structure not present in file
- **ALREADY_ANIMATED** = element has existing GSAP (skipped to avoid conflicts)
