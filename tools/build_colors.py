# Build script: generates libraries/colors.xml diff patch content.
# Not shipped in the mod -- dev tool only.

FAMILIES = {
    # name: base RGB
    "panel":    (16, 19, 23),
    "chrome":   (98, 112, 128),
    "accent":   (56, 189, 248),
    "signal":   (255, 158, 64),
    "player":   (86, 222, 138),
    "hostile":  (255, 82, 82),
    "mission":  (255, 205, 70),
    "scan":     (255, 72, 176),
    "text":     (238, 236, 228),
    "textmute": (150, 158, 168),
}

GLOW_LEVELS = {
    "weak_glow": 0.05,
    "moderate_glow": 0.2,
    "glow": 0.4,
    "strong_glow": 0.6,
}

def blend(c, target, factor):
    return tuple(round(c[i] + (target[i] - c[i]) * factor) for i in range(3))

def brightness_rgb(base, brightness):
    if brightness is None:
        return base
    if brightness == "dark":
        return blend(base, (0, 0, 0), 0.45)
    if brightness == "darker":
        return blend(base, (0, 0, 0), 0.70)
    if brightness == "bright":
        return blend(base, (255, 255, 255), 0.30)
    if brightness == "very_bright":
        return blend(base, (255, 255, 255), 0.55)
    if brightness == "extra_bright":
        return blend(base, (255, 255, 255), 0.75)
    raise ValueError(brightness)

COLOR_DEFS = {}  # id -> (r,g,b,a,glow_or_None)
COLOR_ORDER = []

def C(family, brightness=None, alpha=None, glow=None):
    base = FAMILIES[family]
    r, g, b = brightness_rgb(base, brightness)
    parts = ["x4uir", family]
    if brightness:
        parts.append(brightness)
    if alpha is not None:
        parts.append(f"alpha_{alpha}")
    if glow:
        parts.append(glow)
    cid = "_".join(parts)
    if cid not in COLOR_DEFS:
        a = alpha if alpha is not None else 255
        g_val = GLOW_LEVELS[glow] if glow else None
        COLOR_DEFS[cid] = (r, g, b, a, g_val)
        COLOR_ORDER.append(cid)
    return cid

# mapping_id -> color id (built via C(...))
MAP = {}

def m(mapping_id, family, brightness=None, alpha=None, glow=None):
    MAP[mapping_id] = C(family, brightness, alpha, glow)

# ---------------------------------------------------------------
# Player colours
m("faction_player", "player", glow="weak_glow")
m("targetmonitor_notoriety_player_1", "player", glow="glow")
m("holomap_player", "player", glow="glow")
m("holomap_playerlocation_playerowned", "player", "very_bright", glow="weak_glow")
m("holomap_multiverse_player", "player", glow="glow")
m("targetsystem_relation_player_text_obstructed", "player", "dark", glow="glow")
m("targetsystem_relation_player_text", "player", glow="glow")
m("targetsystem_relation_player_obstructed", "player", "dark", glow="glow")
m("targetsystem_relation_player", "player", glow="glow")
m("text_player", "player", glow="glow")
m("text_player_current", "player", "bright", glow="weak_glow")
m("text_player_lowlight", "player", "dark", glow="weak_glow")
m("text_player_inactive", "player", "dark", glow="weak_glow")
m("player_info_background", "panel", "dark", alpha=160, glow="weak_glow")

# Neutral relation colours (kept on accent hue, matches vanilla convention)
m("targetsystem_relation_neutral", "accent", "bright", glow="glow")
m("targetsystem_relation_neutral_obstructed", "accent", "dark", glow="weak_glow")
m("targetsystem_relation_neutral_text", "accent", "bright", glow="glow")
m("targetsystem_relation_neutral_text_obstructed", "accent", "bright", glow="weak_glow")
m("holomap_playerlocation_neutral", "accent", "bright", glow="glow")
m("holomap_neutral", "accent", "bright", glow="weak_glow")
m("text_relation_neutral", "accent", "bright", glow="weak_glow")
m("mapblip_neutral", "accent", glow=None)
m("mapblip_bad", "hostile", "bright")

# First person mode / dialog menu
m("dialogmenu_normal_text", "accent", "bright", glow="glow")
m("dialogmenu_normal_background", "panel", "darker", alpha=224)
m("dialogmenu_instant_text", "signal", "bright", glow="glow")
m("dialogmenu_instant_background", "panel", "darker", alpha=224)
m("dialogmenu_center_unselected", "chrome", "dark", glow="weak_glow")
m("firstperson_crosshair_text", "text", glow="moderate_glow")
m("firstperson_crosshair_crosshair", "accent", "bright", glow="glow")

# Cockpit HUD / notoriety
m("targetmonitor_notoriety_friendly_1", "player", "dark", glow="weak_glow")
m("targetmonitor_notoriety_friendly_2", "player", "dark", glow="glow")
m("targetmonitor_notoriety_friendly_3", "player", glow="glow")
m("targetmonitor_notoriety_friendly_4", "player", "bright", glow="glow")

# Target indicator / weapons
m("targetsystem_collectible", "accent", glow="weak_glow")
m("targetsystem_aimahead", "accent", glow="weak_glow")
m("targetsystem_shield", "accent", "bright")
m("targetsystem_shield_obstructed", "accent", "dark")
m("targetsystem_missile_hostile_locking", "hostile", glow="weak_glow")
m("targetsystem_velocity_indicator", "signal", "dark", glow="weak_glow")
m("targetsystem_velocity_indicator_offscreen", "signal", glow="glow")
m("external_view_target_arrow", "accent", glow="glow")
m("external_view_mission_arrow", "mission", "dark", glow="glow")

# HUD Gravidar / Holomap
m("gravidar_background", "panel", alpha=64)
m("holomap_equipment_slot", "signal", "bright")
m("holomap_yieldbar", "signal", glow="weak_glow")
m("holomap_yieldbar_empty", "chrome", "dark", alpha=160)
m("holomap_hullbar", "signal", alpha=96, glow="glow")
m("holomap_shieldbar", "accent", "bright")
m("holomap_oxygenbar", "accent", "very_bright", glow="weak_glow")
m("holomap_progressbar", "signal", "dark")
m("holomap_collectable", "accent", glow="weak_glow")
m("holomap_buyoffer", "mission", "very_bright", glow="weak_glow")
m("holomap_radar_background", "chrome", "darker")
m("holomap_radar_ecliptic", "chrome", "dark")
m("holomap_radar_axis_labels", "chrome")
m("holomap_ecliptic_line", "chrome", "dark")
m("holomap_ecliptic_sphere", "chrome", "dark")
m("holomap_order_inactive", "chrome", "dark", alpha=160)
m("holomap_order_active", "accent", "dark", alpha=160)
m("holomap_order_selected_inactive", "chrome", "dark", alpha=64)
m("holomap_order_selected_active", "accent", glow="glow")
m("holomap_orderline_inactive", "panel", alpha=32)
m("holomap_orderline_active", "accent", "dark", alpha=160)
m("holomap_orderline_selected_inactive", "chrome", "dark", alpha=160)
m("holomap_orderline_selected_active", "accent")
m("holomap_order_priority_active", "signal", "dark")
m("holomap_order_priority_inactive", "signal", "darker")
m("holomap_orderline_priority_active", "signal", "dark")
m("holomap_orderline_priority_inactive", "signal", "darker")
m("holomap_order_failed", "hostile", alpha=160, glow="glow")
m("holomap_intersector_defence_line", "panel", alpha=64, glow="weak_glow")
m("order_temp", "chrome", "dark")
m("holomap_attackmarker", "hostile", glow="weak_glow")
m("holomap_infobox_background", "panel", "darker", glow="weak_glow")
m("holomap_infobox_selected", "accent", "dark", glow="weak_glow")
m("holomap_infobox_picked", "accent", glow="weak_glow")
m("holomap_infobox_frame", "chrome", "dark", glow="weak_glow")
m("holomap_missiontarget", "mission", glow="glow")
m("holomap_inactivemissiontarget", "mission", "dark", glow="glow")

# Crosshair & weapon indicators
m("crosshair_crosshair", "accent", "bright", glow="glow")
m("crosshair_target_arrow", "text", glow="moderate_glow")
m("crosshair_hull_gradient", "chrome", "dark")
m("crosshair_hull_gradient_glow", "signal", "bright")
m("crosshair_hull", "text", glow="moderate_glow")
m("crosshair_shield", "accent", glow="glow")
m("crosshair_shield_damage_animation", "accent", "very_bright", glow="strong_glow")
m("crosshair_shield_boost", "accent", "dark", alpha=160, glow="glow")
m("crosshair_shield_gradient_glow", "accent", "bright")
m("crosshair_oxygen", "accent", "bright")
m("crosshair_boostbar", "signal", "bright", glow="glow")
m("crosshair_boostbar_full", "signal", "very_bright")
m("crosshair_boostbar_inactive", "chrome", "darker")
m("crosshair_boostbar_error", "hostile", "dark", glow="glow")
m("crosshair_weapon", "accent", glow="glow")
m("crosshair_weapon_highlight", "accent", "bright", glow="glow")
m("crosshair_weapon_deco", "accent", glow="glow")
m("crosshair_weapon_group_active", "accent", glow="glow")
m("crosshair_weapon_disabled", "chrome", "darker", alpha=244)
m("crosshair_weapon_error", "hostile", "dark", glow="glow")
m("crosshair_weapon_ammo", "text", glow="moderate_glow")
m("crosshair_reload_autoreloading", "signal", "dark")
m("crosshair_reload_autoreloading_inactive", "chrome", "dark")
m("crosshair_heat_normal", "signal", "extra_bright", glow="glow")
m("crosshair_heat_normal_inactive", "chrome")
m("crosshair_heat_next_shot_normal", "signal", "dark", alpha=160)
m("crosshair_heat_next_shot_normal_inactive", "chrome", "dark", alpha=160)
m("crosshair_turret_mode", "accent", glow="glow")
m("crosshair_turret_mode_highlight", "accent", "very_bright", glow="glow")
m("crosshair_drone_armed", "signal", glow="glow")
m("crosshair_drone_armed_highlight", "signal", "very_bright", glow="glow")
m("crosshair_drone_mode_active", "signal", glow="glow")
m("crosshair_drone_mode_active_highlight", "signal", "very_bright", glow="glow")
m("crosshair_drone_number", "text", glow="moderate_glow")
m("crosshair_indicator_active", "accent", glow="glow")
m("crosshair_indicator_activated", "chrome", "dark")
m("crosshair_countermeasures", "signal", glow="glow")
m("crosshair_progressbar_grid", "accent", "bright")
m("crosshair_progressbar_ring", "accent")
m("crosshair_progressbar_icon", "text", glow="moderate_glow")
m("crosshair_seta_ring", "chrome", "bright", glow="glow")
m("crosshair_seta_available", "chrome", "bright", glow="glow")
m("crosshair_seta_active", "chrome", "very_bright", glow="glow")
m("crosshair_speedbar", "text", glow="moderate_glow")
m("crosshair_speedbar_boost", "signal", glow="glow")
m("crosshair_speedbar_maxpoint", "signal", "bright")
m("crosshair_checkengine_normal", "text", glow="moderate_glow")
m("crosshair_mission_arrow", "mission", glow="glow")
m("crosshair_clipreload_autoreloadfailed", "hostile", "dark", glow="glow")
m("crosshair_clipreload_autoreloadfailed_inactive", "hostile", "dark", glow="glow")
m("crosshair_clipreload_autoreloadicon", "signal", glow="weak_glow")
m("crosshair_clipreload_autoreloading", "signal", glow="weak_glow")
m("crosshair_clipreload_autoreloading_inactive", "signal", "dark", glow="weak_glow")
m("crosshair_clipreload_background", "chrome", "darker")
m("crosshair_clipreload_highlight", "signal", glow="weak_glow")
m("crosshair_clipreload_highlight_inactive", "chrome", "darker")
m("crosshair_clipreload_icon", "accent", glow="glow")
m("crosshair_clipreload_ready", "accent", glow="glow")
m("crosshair_clipreload_ready_inactive", "chrome", "darker")
m("crosshair_clipreload_reloading", "hostile", "dark", glow="glow")
m("crosshair_clipreload_reloading_inactive", "hostile", "dark", glow="glow")
m("weaponpointer_inrange", "signal", glow="weak_glow")
m("weaponpointer_outofrange", "chrome", "dark", glow="weak_glow")
m("weapon_group_highlight", "accent", "dark", alpha=224)
m("interactmenu_queueorder", "accent", "very_bright", glow="glow")

# Messages / ticker / notifications
m("messageticker_mail_icon", "accent", glow="glow")
m("messageticker_text", "text", glow="weak_glow")
m("messageticker_text_background_default", "panel", alpha=0)
m("messageticker_deco", "accent", glow="glow")
m("messageticker_deco_background", "panel", "darker", alpha=160)
m("text_notification_header", "accent", "bright", glow="weak_glow")
m("text_notification_text", "text", glow="weak_glow")
m("text_notification_text_lowlight", "textmute", glow="weak_glow")

# Missions
m("targetsystem_mission", "mission")
m("targetsystem_mission_obstructed", "mission", "dark")
m("icon_mission", "mission", glow="glow")
m("text_mission", "mission", glow="glow")
m("text_mission_inactive", "mission", "dark")
m("messageticker_mission", "mission", glow="glow")
m("messageticker_mission_highlight", "mission", "dark")
m("messageticker_curmission_text", "mission", "bright")
m("messageticker_curmission_text_highlight", "mission", "extra_bright")
m("messageticker_bgmission_text", "mission", "very_bright")
m("messageticker_bgmission_text_highlight", "mission", "extra_bright")

# Selected target info screen
m("targetmonitor_text", "text", glow="weak_glow")
m("targetmonitor_text_background_default", "panel", alpha=0)
m("targetmonitor_text_background_overlay", "panel", "darker", alpha=64)
m("targetmonitor_deco", "accent", glow="weak_glow")
m("targetmonitor_deco_background", "panel", "darker", alpha=160)

# Shield / hull bars
m("shieldhullbar_shield", "accent", glow="glow")
m("shieldhullbar_hull", "signal", alpha=96, glow="glow")

# Statusbar
m("statusbar_value_default", "accent")
m("statusbar_value_white", "text", glow="weak_glow")
m("statusbar_diff_pos", "player", alpha=160)
m("statusbar_diff_neg", "hostile", alpha=160)
m("statusbar_marker_default", "accent", "very_bright")
m("statusbar_marker_hidden", "panel", alpha=64, glow="weak_glow")

# Activity modes
m("playeractivity_travel", "signal", glow="glow")
m("playeractivity_travel_background", "panel", alpha=64, glow="weak_glow")
m("playeractivity_scan", "scan", "bright", glow="glow")
m("playeractivity_scan_background", "panel", alpha=64, glow="weak_glow")
m("playeractivity_seta", "chrome", "dark", glow="glow")
m("playeractivity_seta_background", "panel", alpha=64, glow="weak_glow")
m("playeractivity_longrangescan", "accent", "very_bright", glow="strong_glow")
m("playeractivity_longrangescan_background", "panel", alpha=64, glow="weak_glow")
m("longrangescan_good", "accent", "bright", glow="glow")
m("longrangescan_bad", "hostile", glow="glow")

# Highlight / scan outline
m("highlight_target_outline", "hostile", glow="glow")
m("highlight_environmentobject_outline", "hostile", "very_bright", glow="glow")
m("highlight_scan_fill_0", "hostile", "dark", glow="glow")
m("highlight_scan_fill_1", "hostile", glow="glow")
m("highlight_scan_fill_4", "hostile", "bright", glow="glow")
m("signalleak_base", "signal", glow="glow")
m("signalleak_background", "signal", "darker")
m("signalleak_scanmode", "accent", glow="glow")

# Resource map
m("resource_map_ice", "accent", "dark")
m("resource_map_silicon", "signal", "dark")
m("resource_map_scrap", "chrome", "dark")
m("resource_map_khaakscrap", "chrome", "dark")

# Menu / loading screen
m("loadingscreen_text", "text", glow="weak_glow")
m("loadingscreen_background", "panel", "darker")
m("loadingscreen_circle", "accent")
m("loadingscreen_bar", "accent", glow="weak_glow")

# Production flowchart
m("flowchart_node_default", "accent", "bright")
m("flowchart_node_background", "panel", "dark")
m("flowchart_node_arrow", "text", glow="moderate_glow")
m("flowchart_value_default", "signal", "dark")
m("flowchart_slider_value1", "accent", "dark")
m("flowchart_slider_value2", "signal", glow="weak_glow")
m("flowchart_slider_diff1", "player", "darker")
m("flowchart_slider_diff2", "chrome", "darker")
m("flowchart_slider_mousedown", "text")
m("flowchart_border_default", "panel", alpha=64, glow="weak_glow")
m("flowchart_column_caption_default", "text", glow="moderate_glow")
m("flowchart_edge_default", "signal")
m("flowchart_junction_default", "text")
m("flowchart_slot_default", "text")

# UI components: text / icon
m("text_normal", "text", glow="weak_glow")
m("text_inactive", "textmute", "dark")
m("text_lowlight", "textmute")
m("text_input_device_keyboard", "signal", "bright")
m("icon_normal", "text", glow="weak_glow")
m("icon_inactive", "textmute", "dark")
m("icon_warning_inactive", "hostile", "bright", glow="glow")
m("text_ally", "player", "bright", glow="weak_glow")
m("text_friend", "player", "bright", glow="weak_glow")
m("text_member", "player", "bright", glow="weak_glow")

# Button
m("button_background_solid", "panel", "dark")
m("button_background_default", "chrome", "darker", alpha=224)
m("button_background_inactive", "panel", "dark")
m("button_border_default", "accent", "dark", glow="moderate_glow")
m("button_border_inactive", "chrome", "dark")
m("button_highlight_default", "accent", glow="weak_glow")
m("button_highlight_bigbutton", "accent", glow="weak_glow")
m("button_highlight_inactive", "chrome", "dark")
m("button_text_inactive", "textmute", "dark")

# Frame / tooltip
m("frame_background_semitransparent", "panel", alpha=224)
m("frame_background_notification", "panel", "dark")
m("frame_background2_notification", "textmute")
m("frameborder_pin", "accent", glow="moderate_glow")
m("frameborder_pin_inactive", "chrome", "dark")

# Container / panel chrome
m("container_panel_background", "panel", alpha=224)
m("container_panel_header", "panel", "darker")
m("container_section_background", "panel", "darker")
m("container_section_header", "panel", "dark")
m("container_subsection_header", "chrome", "darker", alpha=64)
m("container_subsection_header_inactive", "chrome", "darker", alpha=160)
m("inputbar_background", "panel", "darker")
m("inputbar_border", "chrome", "dark")
m("input_reference", "accent", "bright", glow="weak_glow")

# Table / row
m("table_row_multiselect", "chrome", "dark", alpha=244)
m("table_row_highlight", "textmute", glow="moderate_glow")
m("table_row_highlight_grey", "chrome", "dark", alpha=192)
m("row_background_blue", "chrome", "darker", alpha=224)
m("row_background_blue_opaque", "chrome", "dark")
m("row_background_selected", "textmute", alpha=160, glow="weak_glow")
m("row_separator", "chrome", "dark")
m("row_separator_encyclopedia", "chrome", "darker")
m("row_title", "chrome", "dark", alpha=160)
m("row_title_background", "chrome", "darker", alpha=224)
m("row_background_unselectable", "panel", "dark")

# Dropdown
m("dropdown_background_default", "chrome", "darker", alpha=224)
m("dropdown_background_inactive", "chrome", "darker")
m("dropdown_border_default", "accent", "dark", glow="moderate_glow")
m("dropdown_border_inactive", "chrome", "dark")
m("dropdown_highlight_default", "accent", glow="weak_glow")
m("dropdown_highlight_big", "accent", glow="weak_glow")
m("dropdown_highlight_inactive", "chrome", "dark")
m("dropdown_option_background_inactive", "panel", "dark")
m("dropdown_option_text_inactive", "textmute")
m("dropdown_text_inactive", "textmute", "dark")

# Editbox
m("editbox_background_default", "chrome", "darker", alpha=224)
m("editbox_background_black", "panel", "darker")
m("editbox_border", "accent", "dark", glow="moderate_glow")
m("editbox_inactive", "textmute", alpha=160)
m("editbox_text_default", "text")

# Slider
m("slider_value", "chrome", "dark")
m("slider_value_inactive", "chrome", "dark")
m("slider_value_inactive_dark", "chrome", "darker")
m("slider_background_default", "panel", "dark", alpha=160)
m("slider_background_inactive", "panel", "dark", alpha=160)
m("slider_border_default", "accent", "dark", glow="moderate_glow")
m("slider_arrow_click", "chrome", "darker")
m("slider_arrow_disabled", "chrome", "dark")

# Scrollbar
m("scrollbar_background", "panel", "dark")
m("scrollbar_slider_normal", "accent", glow="weak_glow")
m("scrollbar_slider_highlight", "accent", glow="glow")
m("scrollbar_slider_inactive", "chrome", "dark")
m("scrollbar_slider_click", "chrome", "darker")
m("hint_background_azure", "accent", glow="glow")

# Checkbox
m("checkbox_highlight", "accent", "bright", glow="weak_glow")
m("checkbox_background", "panel", "darker")
m("checkbox_background_default", "chrome", "darker", glow="glow")
m("checkbox_background_highlight", "chrome", "darker", alpha=160)
m("checkbox_background_inactive", "panel", "dark")
m("checkbox_symbol_active", "accent", glow="glow")
m("checkbox_symbol_inactive", "textmute", alpha=244)

# Tooltip / help overlay
m("helpoverlay_border", "signal", "dark")
m("helpoverlay_highlight", "signal", glow="moderate_glow")
m("helpoverlay_background", "panel", "darker", alpha=192)

# Misc
m("overlay_scenario_stat_text", "accent", "bright", glow="weak_glow")
m("dockui_shippos_current_bad", "hostile", "bright", glow="glow")
m("toplevel_arrow", "accent", glow="glow")
m("toplevel_arrow_inactive", "chrome", "dark", alpha=160)
m("si_prefix", "signal", "bright", glow="glow")

# Promo panels
m("promo_text_highlight", "accent", glow="weak_glow")
m("promo_text_background", "panel", "darker")
m("promo_white_line", "text", glow="weak_glow")
m("promo_background", "textmute", glow="moderate_glow")
m("promo_button_normal", "chrome", "darker", alpha=224)
m("promo_button_highlight", "accent", glow="moderate_glow")

# Faction colours (kept close to original semantics)
m("faction_loanshark", "scan", "bright", glow="weak_glow")
m("faction_teladi", "mission", "very_bright", glow="weak_glow")
m("faction_ministry", "player", "dark", glow="moderate_glow")

# ---------------------------------------------------------------
LANG_HEADER = """<?xml version="1.0" encoding="utf-8"?>
<diff>
\t<!--
\tX4 UI Rework: Meridian theme
\thttps://github.com/St3ve109/X4_ui

\tRecolours libraries/colors.xml via the game's native colour mapping
\tsystem. Only mapping references are changed; base game colour ids are
\tleft untouched so other extensions that add their own colours, or that
\tpatch different mapping ids, keep working normally alongside this mod.
\t-->

"""

def fmt_color_attr(v):
    r, g, b, a, glow = v
    s = f'r="{r}" g="{g}" b="{b}" a="{a}"'
    if glow is not None:
        s += f' glow="{glow}"'
    return s

def build():
    out = [LANG_HEADER]
    # group mapping replacements by section using a simple ordered dict of comments
    out.append("\t<!-- Colour mapping overrides -->\n\n")
    for mapping_id in sorted(MAP.keys()):
        color_id = MAP[mapping_id]
        out.append(f"\t<replace sel=\"/colormap/mappings/mapping[@id='{mapping_id}']\">\n")
        out.append(f"\t\t<mapping id=\"{mapping_id}\" ref=\"{color_id}\"/>\n")
        out.append("\t</replace>\n")
    out.append("\n\t<!-- Meridian theme colour palette -->\n\n")
    out.append('\t<add sel="/colormap/colors">\n')
    for cid in COLOR_ORDER:
        out.append(f'\t\t<color id="{cid}" {fmt_color_attr(COLOR_DEFS[cid])}/>\n')
    out.append('\t</add>\n')
    out.append("</diff>\n")
    return "".join(out)

if __name__ == "__main__":
    import os
    content = build()
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "libraries", "colors.xml")
    with open(out_path, "w") as f:
        f.write(content)
    print(f"mappings: {len(MAP)}  unique colors: {len(COLOR_ORDER)}")
