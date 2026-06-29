---
name: ui-ux-pro-max
description: Pro-level UI/UX guidelines for creating premium, high-fidelity web dashboards with modern layouts, glassmorphism, rich typography, and sleek animations.
---

# UI/UX Pro Max Guidelines

When this skill is active, apply the following design guidelines to all frontend interfaces:
1. **Aesthetics & Theme**:
   - Dark theme by default with deep navy/slate backgrounds (e.g. background `#0b0f19`, cards `#151c2c` with subtle borders).
   - Use glassmorphism: `backdrop-filter: blur(12px) saturate(180%); background-color: rgba(21, 28, 44, 0.75); border: 1px solid rgba(255, 255, 255, 0.08);`.
   - Typography: Use Google Fonts like `Inter` or `Outfit` for a modern look.
2. **Visual Hierarchy & Spacing**:
   - Establish clear headings (large, bold, high contrast) and smaller muted labels.
   - Use dynamic visual cues: subtle glowing borders for active items, gradients for primary metrics.
   - Spacing: Ensure generous padding (at least 20px in cards, 24px-32px margins) to let content breathe.
3. **Charts & Data Presentation**:
   - Customize charts to align with the theme. Use glowing trace lines, smooth curve interpolations, and transparent chart backgrounds.
   - Highlight important details in tooltips with clean HTML/CSS formatting.
4. **Interactive Elements**:
   - Add micro-animations: slight hover lifts (`transform: translateY(-2px)`), scaling, and transitions for transitions (`transition: all 0.3s ease`).
