# Live Sources — motion-dev

This file maintains WebFetch URLs for fetching up-to-date documentation and specifications. Use these conditionally when:

- A user asks about a specific GSAP API or plugin
- CSS animation specifications need verification
- Web Animations API support needs checking
- Animation trend research requires current standards

## GSAP Documentation

**GSAP Official LLM-Optimized Docs**

- URL: `https://gsap.com/llms.txt`
- Purpose: Comprehensive GSAP 3.12+ API reference, plugins, easing functions, ScrollTrigger patterns
- Extraction prompt: "Extract the API reference for [SPECIFIC_API]. Include type signatures, parameters, return values, and code examples."
- Cache strategy: Fetch once per session, reuse for multiple questions

**GSAP TypeScript Docs** (if user has TypeScript codebase)

- URL: `https://gsap.com/docs/v3/`
- Purpose: Official docs with TypeScript support
- Extraction prompt: "Find the TypeScript signatures and examples for [API]. Include `d.ts` file information if available."

## CSS Animation & Web Standards

**MDN Web Docs — CSS Animations**

- URL: `https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations`
- Purpose: CSS animation spec, browser support, performance notes
- Extraction prompt: "Summarize the current browser support for CSS animations, including prefers-reduced-motion, and any performance warnings."
- Use case: When user asks about pure CSS animations or browser compatibility

**MDN Web Docs — Web Animations API**

- URL: `https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API`
- Purpose: Web Animations API spec, timing functions, keyframe formats
- Extraction prompt: "What are the current browser support levels for Web Animations API? List all supported timing functions."
- Use case: When user asks about vanilla JavaScript animation APIs

**CSS Transitions Spec**

- URL: `https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_transitions`
- Purpose: Official CSS transition behavior, timing, edge cases
- Extraction prompt: "Summarize the spec for CSS transitions, including all valid timing functions and how prefers-reduced-motion affects transitions."

## React Animation Libraries

**GSAP useGSAP Hook** (Official React integration)

- URL: `https://gsap.com/react`
- Purpose: React-specific patterns, useGSAP hook API, cleanup strategies
- Extraction prompt: "Explain how the useGSAP hook works. What are the required imports and how should cleanup be handled?"
- Use case: When user needs React-specific GSAP implementation

**Framer Motion Docs** (Alternative to GSAP for React)

- URL: `https://www.framer.com/motion/introduction/`
- Purpose: Framer Motion API, gesture handling, layout animations
- Extraction prompt: "Compare Framer Motion's feature set to GSAP. What animations are possible with Framer Motion but not GSAP?"
- Use case: If user explicitly asks about Framer Motion or alternatives to GSAP

## Tailwind CSS Motion Utilities

**Tailwind CSS Animation Docs**

- URL: `https://tailwindcss.com/docs/animation`
- Purpose: Built-in Tailwind motion utilities, custom animation configuration
- Extraction prompt: "List all built-in Tailwind animation utilities and show how to extend them with custom animations in tailwind.config.js"
- Use case: When user uses Tailwind and needs CSS-only animation

## When to Use These Sources

| Scenario                                            | Source to Fetch         | Prompt                                                                                                      |
| --------------------------------------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------- |
| User asks "How do I use gsap.timeline()?"           | GSAP Official LLM Docs  | "Explain gsap.timeline(), including parameters, chainable methods, and a complete example."                 |
| User asks "What easing functions are available?"    | GSAP Official LLM Docs  | "List all built-in easing functions with examples. What's the difference between power easing and elastic?" |
| User asks "Does my browser support CSS animations?" | MDN CSS Animations      | "What are the current browser support levels for CSS animations in 2026?"                                   |
| User asks "How do I animate in React with GSAP?"    | GSAP useGSAP Hook docs  | "Show a complete example of using useGSAP in a React component."                                            |
| User uses Tailwind and asks about animation         | Tailwind Animation Docs | "How can I create custom animations in Tailwind CSS?"                                                       |
| User asks about Web Animations API                  | MDN Web Animations API  | "Explain how to use Web Animations API. What are its limitations compared to GSAP?"                         |

## Caching Strategy

- **GSAP LLM Docs** — fetch once per session and cache; reuse for all GSAP questions
- **Standards (MDN, Tailwind)** — fetch as needed; these change infrequently but may have browser support updates
- **Abort if 404** — If a URL returns 404, fall back to knowledge cutoff (February 2025) and note the failure

## Notes

- All URLs assume HTTPS; WebFetch will automatically upgrade HTTP to HTTPS
- Extraction prompts should be specific enough to yield actionable API information
- Don't fetch all live sources upfront; load conditionally based on user question
- If a user asks a question that _could_ benefit from a live source but your knowledge seems current, prefer local knowledge to save tokens
