# Live Sources — motion-dev

This file lists the official and high-signal live sources to fetch when local references are not enough.

Fetch live docs when:
- the user asks for a specific GSAP plugin or API detail
- browser support or standards behavior needs current confirmation
- a new plugin family is involved and the local pattern snippet is too narrow
- you need exact method signatures, parameters, or cleanup behavior

## Primary GSAP Sources

### GSAP LLM Docs

- URL: `https://gsap.com/llms.txt`
- Use first for any GSAP question, plugin lookup, or syntax check
- Best prompt: `Extract the API details and examples for [plugin_or_method]. Include parameters, cleanup notes, and caveats.`

### Plugin-Specific Official Docs

- ScrollTrigger: `https://gsap.com/docs/v3/Plugins/ScrollTrigger/`
- SplitText: `https://gsap.com/docs/v3/Plugins/SplitText/`
- Flip: `https://gsap.com/docs/v3/Plugins/Flip/`
- Draggable: `https://gsap.com/docs/v3/Plugins/Draggable/`
- Observer: `https://gsap.com/docs/v3/Plugins/Observer/`
- MotionPathPlugin: `https://gsap.com/docs/v3/Plugins/MotionPathPlugin/`
- MorphSVGPlugin: `https://gsap.com/docs/v3/Plugins/MorphSVGPlugin/`
- DrawSVGPlugin: `https://gsap.com/docs/v3/Plugins/DrawSVGPlugin/`
- ScrambleTextPlugin: `https://gsap.com/docs/v3/Plugins/ScrambleTextPlugin/`
- ScrollSmoother: `https://gsap.com/docs/v3/Plugins/ScrollSmoother/`

Use these when the user needs exact plugin behavior or when a pattern folder calls for a plugin-specific build that the local snippet does not fully answer.

## Browser and Platform Sources

- MDN CSS Animations: `https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations`
- MDN Web Animations API: `https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API`
- MDN View Transitions API: `https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API`
- Tailwind animation docs: `https://tailwindcss.com/docs/animation`

Use these only when the question depends on browser support, standards behavior, or CSS/Tailwind implementation details.

## Community Validation Sources

- Codrops: `https://tympanus.net/codrops/`

Use community sources second, after official docs, to validate whether a pattern still feels current in real-world premium builds.

## Suggested Fetch Order

1. Local pattern folder `spec.yaml` + snippet
2. Local fallback docs in `references/gsap-patterns.md`
3. `https://gsap.com/llms.txt`
4. Plugin-specific GSAP docs
5. MDN / Tailwind / platform docs
6. Codrops or comparable community validation

## Common Scenarios

| Scenario | Source to fetch | Prompt |
|---|---|---|
| Need exact `ScrollTrigger` start/end or pin behavior | GSAP LLM Docs, then ScrollTrigger docs | `Explain ScrollTrigger pin, scrub, start, and end options with examples.` |
| Need `SplitText` or `ScrambleTextPlugin` syntax | GSAP LLM Docs, then plugin docs | `Show the current API and cleanup pattern for [plugin].` |
| Need drag, inertia, or reorder behavior | GSAP LLM Docs, then Draggable docs | `Explain Draggable with inertia and how to clean it up safely.` |
| Need orbit/path animation details | GSAP LLM Docs, then MotionPath docs | `Show MotionPathPlugin setup, align, and autoRotate usage.` |
| Need SVG drawing or morphing details | GSAP LLM Docs, then DrawSVG/MorphSVG docs | `Show the current DrawSVG/MorphSVG API with examples.` |
| Need full-page smooth-scroll shell behavior | GSAP LLM Docs, then ScrollSmoother docs | `Explain ScrollSmoother setup, wrapper/content requirements, and cleanup.` |
| Need browser support or standards confirmation | MDN | `Summarize current support and caveats for [feature].` |

## Rules

- Official GSAP sources come first for GSAP questions.
- Do not fetch every live source up front; fetch only what the active task requires.
- Cache `https://gsap.com/llms.txt` once per session and reuse it.
- If a live source fails, say so briefly and continue with the best local fallback.
