---
trigger: always_on
---

# Textual CSS Variables – Windsurf Project Reference

## 1. Purpose
- Complete list of all Textual CSS variables
- Single source of truth for Windsurf UI
- **Rule**: No hard-coded colors — use only these variables

## 2. Core Theme Variables (Must Define in @theme)
- `$primary` – Required – Main brand color – Buttons, focus
- `$secondary` – Optional – Secondary UI
- `$accent` – Optional – Highlights – Speed gauge
- `$warning` – Optional – Caution – Battery low
- `$error` – Optional – Critical – GPS lost
- `$success` – Optional – Success – GPS lock
- `$panel` – Optional – Background – Screen, cards
- `$surface` – Optional – Elevated – Cards, modals
- `$text` – Optional – Primary text – Labels, values
- `$muted` – Optional – Secondary text – Units, timestamps
- `$dim` – Optional – Disabled / dim – Inactive states

## 3. Auto-Generated Variants (Do Not Define)
### 3.1 Light/Dark
- `$primary-light`, `$primary-dark`
- `$accent-light`, `$accent-dark`
- `$warning-light`, `$warning-dark`
- `$error-light`, `$error-dark`
- `$success-light`, `$success-dark`

### 3.2 Opacity Steps (10% to 90%)
- `$primary-10`, `$primary-20`, ..., `$primary-90`
- Same for: `accent`, `warning`, `error`, `success`, `panel`, `surface`, `text`, `muted`, `dim`

### 3.3 Semantic Variants
- `$error-muted`, `$error-on-panel`, `$error-on-surface`
- `$warning-muted`, `$warning-on-panel`, `$warning-on-surface`
- `$success-muted`, `$success-on-panel`, `$success-on-surface`

### 3.4 Total Auto-Generated
- 14 variants per base color
- 11 base colors × 14 = **154 auto-generated**

## 4. Built-in System Variables (Always Available)
- `$background` – Current widget background
- `$foreground` – Current text color
- `$scrollbar` – Scrollbar thumb
- `$scrollbar-background` – Scrollbar track
- `$focus` – Focus ring color
- `$selection` – Text selection color

## 5. Custom CSS Variables (Windsurf-Defined)
- `--width` – Dynamic width
- `--height` – Dynamic height
- `--speed-pct` – Gauge fill percentage
- `--battery-level` – Battery state

## 6. Windsurf Variable Map
- Header background → `$panel`
- Card background → `$surface`
- Primary button → `$primary`
- Button hover → `$primary-70`
- Speed value → `$accent`
- GPS locked → `$success`
- GPS lost → `$error`
- Battery low → `$warning`
- Disabled button → `$dim`
- Focus ring → `$focus`
- Scrollbar → `$accent-30`

## 7. Validation Rules
- No `#hex`, `rgb()`, `hsl()` in code
- No `!important` unless inline override
- No undefined variables
- No web-only CSS (e.g. `position: absolute`)

## 8. Quick Reference
- **Bases (11)**: primary, accent, warning, error, success, panel, surface, text, muted, dim
- **Variants per base**: light, dark, -10 to -90, muted, on-panel, on-surface
- **Total available**: 11 + 154 = **165 variables**

## 9. Do NOT Use
- Hard-coded colors
- `!important`
- Undefined variables
- Web-only properties

---
**For Windsurf Project Only**  
*Last Updated: Nov 14, 2025*  
*Textual v0.85+*