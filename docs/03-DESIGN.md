# 03-DESIGN — Therapeutic-AI (Global2Design Compliance)

## Overview
The clinician-facing SaMD app and the internal research platform both follow the global **Global2Design** standard: dual theme, animated backgrounds, award-level modern UI.

## Theme system (mandatory — dual theme)
- **Dark (default):** near-black canvas (`#0A0A0B` range), luxury feel, **gold accent** (`#C9A227`), muted body text (`#9CA3AF` tier).
- **Light:** soft off-white canvas (`#F7F6F3` range), same accent system, **identical layout** — only palette swaps.
- Visible theme toggle on every page; persisted in local storage.

## Typography & spacing
- System font stack (Inter / IBM Plex Sans) with clear type scale.
- Generous spacing rhythm; scroll-reveal animations; hover micro-interactions (lift, glow).

## Brand
- **Working name:** Therapeutic AI.
- **Accent:** Gold (`#C9A227`) — therapeutic + premium.
- Refined logo treatment; minimal top nav with accent CTA button; glassmorphism dropdown menus.

## Animated backgrounds (no static backgrounds anywhere)
- **Hero / auth / sign-in pages:** full-bleed animated background — slow flowing silk / particle motion, themed to molecular biology (atoms, protein folds, helix glyphs). GPU-friendly, custom easing, respects `prefers-reduced-motion`.
- **App pages:** subtle animated gradient motion / particles / flowing lines behind content.
- All visual assets are **AI-generated only** (no stock photos) — per global AI-Generated Visuals policy. Assets local in `/public/assets/generated`.

## Clinical product design principles (SaMD-specific)
- **Calm over flash:** motion must not distract during clinical use; animations subtle, short (<400ms), reduced on focus.
- **High readability & accessibility:** WCAG 2.1 AA contrast in both themes; focus states clear.
- **Error states:** explicit, non-technical, actionable (per Global2Design §3 + FDA usability expectations).
- **Data transparency:** show model version + validation status in UI (supports PCCP transparency).

## Component approach
- shadcn/ui component library (global design stack default).
- Framer Motion for transitions matching documented timing/easing.
- Micro-interaction specs from `microinteractions` skill; Framer Motion patterns from `framer-motion-animator`.

## Compliance notes
- Theme toggle must work on every route (Global2Design §4).
- Post-implementation interaction verification: full clickability audit per Global2Design §4 before shipping any UI.

_This is v1 design direction; refined when product build starts._