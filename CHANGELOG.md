# Changelog

## 1.0.0 — 2026-07-08

- Initial release of the Meridian theme, styled after EVE Online's tactical-HUD look:
  near-black neutral panels, a teal-cyan interactive accent, and gold/amber highlights.
- Full colour-mapping patch (`libraries/colors.xml`) covering 314 real X4 UI mappings:
  menus/panels, buttons/dropdowns/editboxes/checkboxes/sliders/scrollbars, tables/rows,
  tooltips, flight HUD crosshair, holomap, target monitor, message ticker, missions,
  notoriety, status bars, production flowchart, loading screen, and faction/relation
  colours.
- Optional soft dependency on kuertee's UI Extensions and HUD for shared theming.
- Palette generator script (`tools/build_colors.py`) for maintainable re-theming.
- Automated structural validation (`tools/validate.py`) plus CI workflow to catch
  malformed XML, dangling colour references, and duplicate selectors on every push.
