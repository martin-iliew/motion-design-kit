# motion-design-kit

Claude Code plugin for modern web motion work. It ships canonical commands for building, upgrading, auditing, discovering, and refreshing website motion with a shared trend-aware runtime layer.

---

## Fast Start

Install at user scope:

```bash
claude plugin marketplace add --scope user martin-iliew/motion-design-kit
claude plugin install --scope user motion-design-kit@motion-design-kit
```

Then open Claude Code at the root of the app you want to edit:

```bash
cd your-project
claude
```

For the recommended project permissions profile, use the setup guide:

- [SETUP.md](/Users/Martin/Desktop/Weband/Repositories/claude-skills/SETUP.md)

---

## Canonical Commands

| Goal | Command | Input |
| --- | --- | --- |
| Add or translate motion | `/motion-build` | file path + request |
| Audit and auto-modernize | `/motion-upgrade` | one or more file paths |
| Review without editing | `/motion-audit` | one or more file paths |
| Discover new pattern ideas | `/motion-discover` | trend brief or no file |
| Rerank runtime trend data | `/motion-refresh` | no file required |

Public surface is canonical:

- `/motion-build`
- `/motion-upgrade`
- `/motion-audit`
- `/motion-discover`
- `/motion-refresh`

---

## Execution Modes

`/motion-build` and `/motion-upgrade` support an optional leading mode prefix:

```bash
/motion-build mode: fast src/index.html add scroll reveal to the pricing cards
/motion-upgrade mode: premium src/pages/home.html
```

If no mode is provided, the default is `balanced`.

| Mode | Use when | Behavior |
| --- | --- | --- |
| `fast` | you want the cheapest safe pass | compiled selector layer only, top-value buckets only |
| `balanced` | normal production work | compiled selector first, selective fallback, concise output |
| `premium` | showcase or premium-brand work | richer composition, limited escalation, slightly richer output |

---

## Example Requests

```bash
/motion-build src/index.html add a GSAP reveal for each feature card on scroll
```

```bash
/motion-build mode: fast src/components/Hero.tsx add an intro timeline for the heading and CTA
```

```bash
/motion-upgrade src/pages/home.html
```

```bash
/motion-upgrade mode: premium src/components/Hero.vue src/components/hero.css
```

```bash
/motion-audit src/components/Hero.tsx src/components/Hero.module.css
```

Plain-English prompts also work as long as you give Claude a real file path.

---

## What Ships

- 5 canonical commands
- 5 canonical skills
- trend-aware runtime selectors under `plugins/motion-design-kit/.claude/motion-library/`
- validation and refresh scripts under `plugins/motion-design-kit/.claude/scripts/`

Marketplace installs resolve from `plugins/motion-design-kit`, so repo-only development assets do not ship with the plugin payload.

---

## Maintainer Notes

Validate before publishing:

```bash
claude plugin validate plugins/motion-design-kit
claude plugin validate plugins/motion-design-kit/.claude-plugin/plugin.json
python plugins/motion-design-kit/.claude/scripts/validate_motion_surfaces.py
python plugins/motion-design-kit/.claude/scripts/validate_motion_library.py --expected-count 75
```

**Last updated:** March 2026
