# Number Counter with Easing Animation

**Framework:** GSAP / JavaScript
**Category:** Typography
**Type:** Tween
**2026 Relevance:** Data visualization and real-time metrics are increasingly important in dashboards and analytics pages. Animated counters draw attention to KPIs and make data feel more dynamic. Perfect for pricing pages, statistics sections, and live metrics dashboards.

## Overview

Number Counter with Easing animates numeric values from a starting point to an ending point, displaying intermediate values in real-time as they increment or decrement. The animation respects easing functions to feel natural and weighted, rather than linear. This pattern handles formatting of numbers with commas, decimals, currency symbols, and percentage signs, making it suitable for displaying diverse metric types.

The counter works by tweening a numeric property from start to finish, then using a callback function to update the DOM text with formatted values. You can apply this to statistics sections, pricing displays, achievement badges, and KPI cards. The easing makes the animation feel intentional rather than mechanical, with common choices being ease-out (fast start, slow finish) or ease-in-out for balance.

## Use Cases

Ideal for hero statistics ("500K+ customers"), pricing page metrics ("30% savings"), achievement displays, and dashboard KPIs. Use on page load or when the section scrolls into view to draw attention. Numbers feel more impactful when animated rather than static, especially in marketing contexts. Works particularly well in combination with section headings and supporting descriptive text.

## Do's

- Format numbers with appropriate locale and currency considerations
- Use ease-out easing for most counters (feels snappy and natural)
- Trigger counters on scroll entry for performance
- Pair with icon or visual element for context
- Round intermediate values for smooth integer display
- Test different easing curves to match your motion brand
- Use in statistics, metrics, and KPI sections

## Don'ts

- Don't animate very large numbers (999,999+) too quickly or the updates blur together
- Don't use linear easing on number counters; ease-out or ease-in-out feel better
- Don't display decimals for whole-number metrics (inconsistent appearance)
- Don't trigger counters on every page visit if users return frequently
- Don't forget locale-specific number formatting for international audiences
- Don't animate counters for non-numeric content
- Don't make the animation duration too short (less than 1 second is too fast)

## Best Practices

**Accessibility & Performance:** Use GSAP for smooth, GPU-optimized tweening. Ensure the final numeric value is present in the DOM (not just animated) so screen readers and data scrapers capture the correct value. For users with prefers-reduced-motion, skip the animation and display the final value immediately. Test that rapidly updated counters don't cause performance issues on lower-end devices.

**When to Use:** Use number counters on hero sections to emphasize key statistics, on pricing pages to highlight cost savings, and on metrics dashboards to draw attention to important KPIs. Limit to 3–5 counters per page to avoid overwhelming the user. Trigger on scroll entry rather than page load to keep the animation impactful when users encounter the section.

**Formatting & Localization:** Support multiple number formats including thousands separators, decimal places, currency symbols, and percentage signs. Use Intl.NumberFormat for proper locale support. Test with various number ranges (1, 100, 1,000, 1,000,000) to ensure formatting looks correct at all scales. Consider suffix/prefix text ("+", "$", "%") to clarify the metric.
