# Motion Design Kit Setup

This file is for teammates who want to install the plugin fast, configure Claude once per project, and then point Claude at real frontend files.

---

## 1. Install The Plugin

Recommended: install at user scope so it is available in every project.

From a terminal:

```bash
claude plugin marketplace add --scope user martin-iliew/motion-design-kit
claude plugin install --scope user motion-design-kit@motion-design-kit
```

Inside Claude Code, the slash-command equivalent is:

```bash
/plugin marketplace add martin-iliew/motion-design-kit
/plugin install motion-design-kit@motion-design-kit
```

After that, the motion commands are available in Claude Code.

---

## 2. Configure Claude In The Project You Want To Edit

In the app repo you want Claude to work on, create `.claude/settings.json`:

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": [
      "Bash(rg:*)",
      "Bash(ls:*)",
      "Bash(dir:*)",
      "Bash(Get-ChildItem:*)",
      "Bash(cat:*)",
      "Bash(type:*)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git ls-files:*)",
      "Bash(git rev-parse:*)",
      "Bash(npm run build:*)",
      "Bash(npm run lint:*)",
      "Bash(npm run test:*)",
      "Bash(pnpm run build:*)",
      "Bash(pnpm run lint:*)",
      "Bash(pnpm run test:*)",
      "Bash(yarn build:*)",
      "Bash(yarn lint:*)",
      "Bash(yarn test:*)",
      "Bash(bun run build:*)",
      "Bash(bun run lint:*)",
      "Bash(bun run test:*)"
    ]
  }
}
```

This keeps Claude from stopping constantly for normal file edits and common project checks.

What still usually prompts:

- package installs
- unusual shell commands
- pushes and other sensitive git actions

---

## 3. Open Claude At The Project Root

```bash
cd your-project
claude
```

Then give Claude file paths relative to that project.

---

## 4. Fastest Commands To Use

### If you want Claude to just improve a file automatically

```bash
/motion-enhance src/pages/home.html
```

```bash
/motion-enhance src/components/Hero.tsx src/components/Hero.module.css
```

Use this when you want the AI to do most of the work.

### If you know the exact effect you want

```bash
/motion-dev src/index.html add a premium scroll reveal to the pricing cards
```

```bash
/motion-dev src/components/Hero.tsx add a strong intro animation for the heading, CTA, and hero image
```

```bash
/motion-dev src/components/Hero.vue add smoother enter motion and keep it mobile-safe
```

```bash
/motion-dev src/lib/Hero.svelte add subtle in-view card reveals
```

Use this when you want a specific outcome.

### If you want a report first

```bash
/motion-audit src/components/Hero.vue
```

```bash
/motion-audit src/components/Hero.tsx src/components/Hero.module.css
```

Use this when you want findings before edits.

---

## 5. The Easiest Prompt Pattern

For HTML, React, Vue, Svelte, and similar frontend files, the simplest prompt is:

```text
[file path] + [desired effect] + [optional hard constraint]
```

Examples:

- `src/index.html add a better scroll reveal and keep the layout`
- `src/components/Hero.tsx make this hero feel more premium`
- `src/components/Hero.vue add subtle motion and keep reduced-motion support`
- `src/lib/Hero.svelte modernize this section without changing the copy`

That is enough in most cases.

Claude will usually handle:

- reading the file
- detecting the framework and stack
- deciding whether GSAP, CSS, or the existing stack is the better fit
- updating imports, hooks, styles, and component code
- keeping the result performant and accessible

---

## 6. When To Include More Than One File

Give multiple files when the feature spans more than one place.

Examples:

```bash
/motion-enhance src/components/Hero.tsx src/components/Hero.module.css
```

```bash
/motion-enhance src/lib/FeatureGrid.svelte src/lib/feature-grid.css src/lib/animations.ts
```

Do this when:

- styles are in a separate CSS or module file
- animation helpers live in another file
- the component is split across markup and shared utilities

---

## 7. Which Command To Pick

| Situation | Command |
| --- | --- |
| I have a file and want Claude to improve it on its own | `/motion-enhance` |
| I know what animation I want | `/motion-dev` |
| I want a report before changing code | `/motion-audit` |
| I want new pattern ideas for the library itself | `/motion-discover` |
| I want to rerank the library data | `/motion-refresh` |

For most teammates, the default should be:

1. `/motion-enhance` first
2. `/motion-dev` if they want something more specific
3. `/motion-audit` if they want review-only output

---

## 8. Short Examples By Stack

### HTML

```bash
/motion-enhance landing-page.html
```

### React / Next / TSX

```bash
/motion-dev src/components/Hero.tsx add a launch-style intro timeline
```

### Vue

```bash
/motion-dev src/components/PricingSection.vue add scroll reveal and CTA hover motion
```

### Svelte

```bash
/motion-dev src/lib/sections/FeatureGrid.svelte add subtle enter motion for each card
```

---

## 9. What To Tell Teammates

The simple rule is:

- open Claude in the app repo
- reference the file they want changed
- say what motion outcome they want
- let Claude do the implementation work

They do not need to explain selectors, imports, hooks, or animation plumbing unless they want a very specific implementation.

---

## 10. Validation For Maintainers

If you are updating the plugin repo itself:

```bash
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
python .claude/scripts/validate_motion_library.py --expected-count 75
```

---

**Last updated:** March 2026
