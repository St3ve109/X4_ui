#!/usr/bin/env python3
"""Structural validation for the X4 UI Rework extension.

Since the game itself can't be launched in CI, this checks everything that
*can* be verified statically: XML well-formedness, that every colour
reference resolves, that there are no duplicate/malformed selectors, that
attribute values are in range, and that content.xml carries the attributes
X4 requires. Run before every commit; also wired into CI.
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []
warnings = []


def check_well_formed(path):
    try:
        return ET.parse(path)
    except ET.ParseError as e:
        errors.append(f"{path.relative_to(ROOT)}: not well-formed XML: {e}")
        return None


def check_no_double_hyphen_in_comments(path):
    text = path.read_text(encoding="utf-8")
    for m in re.finditer(r"<!--(.*?)-->", text, re.DOTALL):
        if "--" in m.group(1):
            errors.append(f"{path.relative_to(ROOT)}: comment contains '--', which is invalid XML")


def validate_content_xml():
    path = ROOT / "content.xml"
    tree = check_well_formed(path)
    check_no_double_hyphen_in_comments(path)
    if tree is None:
        return
    root = tree.getroot()
    if root.tag != "content":
        errors.append("content.xml: root element must be <content>")
        return
    required = ["id", "name", "version", "save"]
    for attr in required:
        if attr not in root.attrib:
            errors.append(f"content.xml: missing required attribute '{attr}' on <content>")
    if not re.fullmatch(r"[A-Za-z0-9_]+", root.attrib.get("id", "")):
        errors.append("content.xml: id must be alphanumeric/underscore only")
    texts = root.findall("text")
    if not texts:
        errors.append("content.xml: must have at least one <text> element")
    for t in texts:
        if "description" not in t.attrib:
            errors.append("content.xml: <text> element missing 'description'")
    for dep in root.findall("dependency"):
        if "id" not in dep.attrib:
            errors.append("content.xml: <dependency> missing 'id'")


def validate_colors_xml():
    path = ROOT / "libraries" / "colors.xml"
    tree = check_well_formed(path)
    check_no_double_hyphen_in_comments(path)
    if tree is None:
        return
    root = tree.getroot()
    if root.tag != "diff":
        errors.append("libraries/colors.xml: root element must be <diff>")
        return

    defined_colors = {}
    mapping_selectors = []
    replace_ids = set()

    for replace in root.findall("replace"):
        sel = replace.get("sel", "")
        m = re.fullmatch(r"/colormap/mappings/mapping\[@id='([^']+)'\]", sel)
        if not m:
            errors.append(f"libraries/colors.xml: malformed sel attribute: {sel!r}")
            continue
        sel_id = m.group(1)
        mapping_selectors.append(sel_id)
        mapping_el = replace.find("mapping")
        if mapping_el is None:
            errors.append(f"libraries/colors.xml: <replace sel=\"{sel}\"> has no <mapping> child")
            continue
        if mapping_el.get("id") != sel_id:
            errors.append(
                f"libraries/colors.xml: sel targets id='{sel_id}' but child <mapping id='{mapping_el.get('id')}'>"
            )
        ref = mapping_el.get("ref")
        if not ref:
            errors.append(f"libraries/colors.xml: mapping '{sel_id}' has no ref attribute")
        else:
            replace_ids.add(ref)

    dupes = {x for x in mapping_selectors if mapping_selectors.count(x) > 1}
    if dupes:
        errors.append(f"libraries/colors.xml: duplicate mapping selectors: {sorted(dupes)}")

    for add in root.findall("add"):
        if add.get("sel") != "/colormap/colors":
            errors.append(f"libraries/colors.xml: unexpected <add sel=\"{add.get('sel')}\">")
            continue
        for color in add.findall("color"):
            cid = color.get("id")
            if not cid:
                errors.append("libraries/colors.xml: <color> missing id")
                continue
            if cid in defined_colors:
                errors.append(f"libraries/colors.xml: duplicate <color id='{cid}'>")
            defined_colors[cid] = color.attrib
            for ch in ("r", "g", "b", "a"):
                val = color.get(ch)
                if val is None:
                    errors.append(f"libraries/colors.xml: color '{cid}' missing '{ch}'")
                    continue
                try:
                    n = int(val)
                except ValueError:
                    errors.append(f"libraries/colors.xml: color '{cid}' has non-integer {ch}='{val}'")
                    continue
                if not (0 <= n <= 255):
                    errors.append(f"libraries/colors.xml: color '{cid}' has {ch}={n} out of range [0,255]")
            glow = color.get("glow")
            if glow is not None:
                try:
                    g = float(glow)
                    if not (0.0 <= g <= 1.0):
                        warnings.append(f"libraries/colors.xml: color '{cid}' glow={g} outside typical [0,1] range")
                except ValueError:
                    errors.append(f"libraries/colors.xml: color '{cid}' has non-numeric glow='{glow}'")

    missing_refs = replace_ids - set(defined_colors)
    if missing_refs:
        errors.append(f"libraries/colors.xml: mapping(s) reference undefined colour ids: {sorted(missing_refs)}")

    unused = set(defined_colors) - replace_ids
    if unused:
        warnings.append(f"libraries/colors.xml: {len(unused)} defined colour(s) not referenced by any mapping: {sorted(unused)}")

    if len(mapping_selectors) < 300:
        warnings.append(
            f"libraries/colors.xml: only {len(mapping_selectors)} mappings patched; expected a full-UI rework to cover 300+"
        )


def main():
    validate_content_xml()
    validate_colors_xml()

    for w in warnings:
        print(f"WARNING: {w}")
    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  ERROR: {e}")
        sys.exit(1)
    print(f"OK: content.xml and libraries/colors.xml passed all checks ({len(warnings)} warning(s)).")


if __name__ == "__main__":
    main()
