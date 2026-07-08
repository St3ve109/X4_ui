# X4 UI Rework — Meridian Theme

A clean, modern recolour and readability overhaul for X4: Foundations' menus and HUD.

## What this is

X4's default interface leans heavily on a single low-contrast blue ("azure") for almost
every panel, button, border and HUD element. **Meridian** replaces it with a cohesive,
higher-contrast palette:

- **Graphite panels** — background chrome (windows, containers, dropdowns, tables) uses a
  neutral dark graphite instead of flat black/navy, so panels read as distinct layers
  instead of a blue-on-black smear.
- **Signal-cyan accent** — buttons, borders, sliders, the crosshair, shields and neutral
  contacts share one crisp, high-contrast cyan so interactive elements are easy to find at
  a glance.
- **Warm amber secondary** — hull bars, active orders, boost/heat indicators, loading
  screens and production flowcharts get a warm amber that's easy to tell apart from the
  cyan accent and from faction relation colours.
- **Preserved relation colours** — player/friendly stays green, hostile stays red, missions
  stay gold/amber, scan-mode stays magenta. Only the *shade and contrast* of these changed,
  not their meaning, so your existing muscle memory for "green = mine, red = danger" still
  works.

It touches **every major surface** the game exposes through its colour-mapping system:
menus and panels, buttons/dropdowns/editboxes/checkboxes/sliders/scrollbars, tables and
rows, tooltips, the flight HUD crosshair, the holomap (including order lines, orders,
radar, info boxes), the target monitor, the message ticker, mission markers, notoriety,
status bars, the production flowchart, the loading screen, and more — **314 individual UI
colour mappings** in total, all listed under [How it works](#how-it-works).

## How it works

X4 ships a game-native colour system: every themeable UI element references a named
*mapping* (e.g. `button_border_default`, `holomap_player`, `crosshair_shield`), and each
mapping points at a named *colour* (RGBA + optional glow). The game reads this from
`libraries/colors.xml`, and extensions can patch it using X4's standard XML diff/patch
system without touching any other file.

This mod is a single diff patch, [`libraries/colors.xml`](libraries/colors.xml), that:

1. Adds a new palette of colours under an `x4uir_` prefix (`<add sel="/colormap/colors">`).
2. Repoints the 314 real, game-defined UI mappings at those new colours
   (`<replace sel="/colormap/mappings/mapping[@id='...']">`).

It does **not** touch any `.lua` file, any menu layout, any macro/ware/job data, or any
Mission Director script. It is a pure colour patch — the least invasive way to reskin the
UI, and the reason it stays compatible with almost everything else (see below).

The palette and every mapping assignment are generated from [`tools/build_colors.py`](tools/build_colors.py)
so the whole theme can be re-tuned by editing one Python file and re-running it, rather than
hand-editing a thousand lines of XML. See [Customizing](#customizing-the-palette).

## Installation

1. Download this repository (Code → Download ZIP, or `git clone`).
2. Copy the contents into a new folder named `x4_ui_rework_meridian` inside your X4
   Foundations `extensions` folder, so you end up with:
   ```
   X4 Foundations/extensions/x4_ui_rework_meridian/content.xml
   X4 Foundations/extensions/x4_ui_rework_meridian/libraries/colors.xml
   ```
   (The `extensions` folder lives next to your X4 install, or under
   `Documents/Egosoft/X4/<id>/extensions/` if you use the Documents-folder install
   location.)
3. Launch the game, open **Extensions** from the main menu, and make sure
   "X4 UI Rework - Meridian Theme" is enabled.
4. If you use X4's in-game **colour intensity / glow sliders** (Options → HUD), they still
   work as normal — this mod only changes the base colours they scale.

No new save is required and none of your saves need this extension to stay enabled — it's
purely cosmetic (`save="false"`), so you can freely enable, disable or remove it at any
time.

## Compatibility with other mods

This mod is designed to sit alongside your existing mod list with minimal friction:

- **It only patches one file**, `libraries/colors.xml`, via the standard XML diff/patch
  system (`<add>` / `<replace>` on XPath selectors). It never replaces a whole file and
  never touches `.lua` UI logic, so it cannot break menu behaviour added by other
  extensions, and other extensions' logic mods can't break this one.
- **[kuertee's UI Extensions and HUD](https://www.nexusmods.com/x4foundations/mods/552)**
  is explicitly supported: it's declared as an *optional* dependency in `content.xml`, so
  if you have it installed, Meridian loads after it and its extra menus/HUD widgets (map
  tools, boarding menu tweaks, interact-menu additions, etc.) automatically pick up the
  Meridian colours too, since they draw from the same game colour-mapping system. You do
  **not** need kuertee's mod installed for Meridian to work — it's a nice-to-have for the
  extra functionality it brings, not a requirement.
- **Other colour/recolour mods** (e.g. "Warmer Palette", "UI Recolor", "RS Colors",
  "Color Factions") patch the same `libraries/colors.xml` mappings. That's not a conflict
  in the sense of breaking anything — X4 just applies whichever patch loads last for any
  mapping the two mods both touch — but running two full recolours together will produce a
  mixed, patchwork look. Disable other full-UI recolour mods if you want the clean Meridian
  look throughout; if a mod only tweaks a couple of specific colours (e.g. just faction
  colours), the two will layer fine.
- **Everything else** — ship mods, economy/balance overhauls, mission mods, VRO, DLCs,
  Mission Director content — is untouched by this mod and will work exactly as it does
  without it.

## What this mod deliberately does *not* change

To stay safe and broadly compatible without the ability to test against every game
version/DLC combination, this mod is scoped to the colour-mapping system only. It does not:

- Rearrange, resize or reposition any menu, panel or HUD element.
- Change fonts or text size (use Options → HUD/Accessibility for that — X4 has native
  scaling controls).
- Add new menus, tabs, or options screens (that's exactly what kuertee's UI Extensions and
  HUD is for, and why it's recommended alongside this mod).
- Modify any `.lua` file.

If you want deeper layout changes on top of this colour theme, kuertee's UI Extensions and
HUD (and other Lua-based UI mods) are the right complementary tools — this mod is designed
to not get in their way.

## Customizing the palette

The whole palette is defined declaratively in [`tools/build_colors.py`](tools/build_colors.py):

- `FAMILIES` — the base RGB for each colour family (`panel`, `chrome`, `accent`, `signal`,
  `player`, `hostile`, `mission`, `scan`, `text`, `textmute`).
- Each `m("some_mapping_id", "family", brightness=..., alpha=..., glow=...)` call assigns
  one of the game's 314 real UI mappings to a shade of one of those families.

To retune the theme (e.g. make the accent purple instead of cyan), edit the RGB tuple for
the relevant family in `FAMILIES` and regenerate:

```bash
python3 tools/build_colors.py
```

This rewrites `libraries/colors.xml` from scratch — don't hand-edit that file directly, or
your changes will be lost the next time the generator runs.

## Credits

- Built against X4: Foundations' documented XML diff/patch modding system
  ([Egosoft Modding Support wiki](https://wiki.egosoft.com/X4%20Foundations%20Wiki/Modding%20Support/)).
- The list of real, game-defined colour-mapping IDs was cross-checked against publicly
  available community recolour mods (notably
  [AutoGibbon's Warmer Palette](https://www.nexusmods.com/x4foundations/mods/1870) and
  [kuertee's UI Extensions and HUD](https://github.com/kuertee/x4-mod-ui-extensions)) to
  make sure every patch targets a real, working mapping id — the Meridian colour palette
  itself is original.
- kuertee's UI Extensions and HUD — recommended companion mod, see
  [Compatibility](#compatibility-with-other-mods).
