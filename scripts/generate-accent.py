#!/usr/bin/env python3
"""Build the optional Pixora Accent theme without changing the original artwork.

KDE recolors the marked SVG paths at render time. This script adapts folders
and their aliases, preserving fixed-color exceptions; it is only a build tool.
"""

import argparse
import copy
import os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "pixora" / "scalable"
DESTINATION = ROOT / "pixora-accent"
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)

# These folders keep their original artwork in the Accent theme too.
FIXED_COLOR_FOLDERS = {"folder-nixos"}

DIRECTORY_CONTEXTS = {
    "apps": "Applications",
    "places": "Places",
    "categories": "Categories",
    "devices": "Devices",
    "mimetypes": "MimeTypes",
    "status": "Status",
    "actions": "Actions",
}
BODY_TRANSFORMS = {
    "translate(32,160)",
    "translate(160,128)",
    "translate(128,64)",
}
SHADOW_TRANSFORM = "translate(32,448)"
SHADOW_PATH = "m0 0h448v32h-448z"
# Black overlays derive glyph tones from Accent while retaining the original
# ordering of light/dark details. Borders and lines between subfolders stay fixed.
GLYPH_SHADES = {
    "#ab947a": "0.40",
    "#a68c77": "0.45",
    "#a88f78": "0.45",
    "#a48675": "0.45",
    "#a48875": "0.45",
    "#9e7c71": "0.50",
    "#966c6c": "0.55",
    "#625565": "0.65",
}
# Linux combines its glyph and bottom band in one path. Recolor the glyph,
# then give the existing bottom band the same shade as the other folders.
LINUX_SHARED_SHADOW = (
    "m0 0h32v32h32v64h32v-32h32v-32h32v-32h32v64h-32v64"
    "h160v32h-448v-32h160v-64h-32z"
)


def folder_names():
    return sorted(
        path.stem for path in (SOURCE / "places").glob("folder*.svg")
        if path.is_file() and not path.is_symlink()
    )


def accent_path(path, role):
    result = copy.deepcopy(path)
    result.attrib.pop("fill", None)
    result.set("class", "ColorScheme-Accent")
    result.set("style", "fill:currentColor")
    result.set("data-pixora-role", role)
    return result


def overlay(path, color, opacity, role):
    result = copy.deepcopy(path)
    result.attrib.pop("id", None)
    result.set("fill", color)
    result.set("fill-opacity", opacity)
    result.set("data-pixora-role", role)
    return result


def append_shaded(result, path, opacity, role):
    result.append(accent_path(path, role))
    result.append(overlay(path, "#000000", opacity, role + "-shade"))


def render_folder(source):
    original = ET.parse(source).getroot()
    paths = list(original)
    body = [
        p for p in paths
        if p.tag == f"{{{SVG}}}path"
        and p.get("fill", "").lower() == "#e3c896"
        and p.get("transform") in BODY_TRANSFORMS
    ]
    shadow_color = "#a48875" if source.stem == "folder-wine" else "#ab947a"
    shadow = [
        p for p in paths
        if p.tag == f"{{{SVG}}}path"
        and p.get("fill", "").lower() == shadow_color
        and p.get("transform") == SHADOW_TRANSFORM
        and p.get("d") == SHADOW_PATH
    ]
    shared_shadow = []
    if source.stem == "folder-linux":
        shared_shadow = [
            p for p in paths
            if p.get("fill", "").lower() == "#ab947a"
            and p.get("transform") == "translate(160,320)"
            and p.get("d") == LINUX_SHARED_SHADOW
        ]
    if source.stem == "folder-desktop":
        # Desktop uses a screen illustration instead of the usual folder shape.
        # Adapt its beige area, preserving the rest of the screen and controls.
        body = [
            p for p in paths
            if p.get("fill", "").lower() == "#e3c896"
            and p.get("transform") == "translate(288,224)"
            and p.get("d") == "m0 0h192v128h-160v-96h-32z"
        ]
        expected = (1, 0, 0)
    elif source.stem == "folder-linux":
        expected = (3, 0, 1)
    else:
        expected = (3, 1, 0)
    if (len(body), len(shadow), len(shared_shadow)) != expected:
        raise ValueError(f"Folder needs an explicit artwork review: {source.name}")
    if source.stem != "folder-desktop":
        supported = {"#e3c896", "#3e3546", "#fff", "#ffffff"} | GLYPH_SHADES.keys()
        if any(p.get("fill", "").lower() not in supported for p in paths):
            raise ValueError(f"Folder palette needs an explicit review: {source.name}")

    result = ET.Element(original.tag, original.attrib)
    definitions = ET.SubElement(result, f"{{{SVG}}}defs")
    style = ET.SubElement(
        definitions, f"{{{SVG}}}style",
        {"id": "current-color-scheme", "type": "text/css"},
    )
    style.text = ".ColorScheme-Accent { color:#e3c896; }"

    for path in paths:
        fill = path.get("fill", "").lower()
        if fill == "#e3c896":
            # Some glyph cutouts and body fragments use separate beige paths.
            # Recolor them too, so no fixed-color pixels remain in the folder.
            result.append(accent_path(path, "body"))
            # Lighten the existing one-pixel top band, without new geometry.
            if path.get("transform") == "translate(128,64)":
                result.append(overlay(path, "#ffffff", "0.18", "highlight"))
        elif path in shadow:
            # The opaque accent underneath prevents background-dependent shades.
            result.append(accent_path(path, "shadow-base"))
            result.append(overlay(path, "#000000", "0.25", "shadow"))
        elif path in shared_shadow:
            append_shaded(result, path, GLYPH_SHADES[fill], "glyph")
            band = ET.Element(f"{{{SVG}}}path", {
                "transform": SHADOW_TRANSFORM, "d": SHADOW_PATH,
            })
            result.append(accent_path(band, "shadow-base"))
            result.append(overlay(band, "#000000", "0.25", "shadow"))
        elif source.stem != "folder-desktop" and fill in GLYPH_SHADES:
            append_shaded(result, path, GLYPH_SHADES[fill], "glyph")
        else:
            # Preserve borders, white paper and lines between the subfolders.
            # Desktop's multicolored screen is separate from folder glyphs.
            result.append(copy.deepcopy(path))

    ET.indent(result, space="  ")
    provenance = f"<!-- Generated from pixora/scalable/places/{source.name}. -->\n"
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n' + provenance
        + ET.tostring(result, encoding="unicode") + "\n"
    ).encode()


def index_contents(directories):
    ordered = [name for name in DIRECTORY_CONTEXTS if name in directories]
    contents = (
        "[Icon Theme]\n"
        "Name=Pixora Accent\n"
        "Comment=Pixora folders that follow the KDE accent color\n"
        "Inherits=pixora,breeze,hicolor\n"
        "FollowsColorScheme=true\n"
        "Directories=" + ",".join(f"scalable/{name}" for name in ordered) + "\n"
    )
    for name in ordered:
        contents += (
            f"\n[scalable/{name}]\n"
            f"Size=16\nContext={DIRECTORY_CONTEXTS[name]}\n"
            "Type=Scalable\nMinSize=8\nMaxSize=512\n"
        )
    return contents.encode()


def build_manifest(names):
    files = {}
    links = {}
    converted = {}
    for name in names:
        source = SOURCE / "places" / f"{name}.svg"
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"Expected original folder artwork: {name}")
        destination = Path("scalable/places") / source.name
        if name in FIXED_COLOR_FOLDERS:
            # An exact alias prevents KDE from choosing the generic Accent
            # folder through its name fallback before checking the base theme.
            links[destination] = os.path.relpath(
                source, DESTINATION / destination.parent,
            )
        else:
            files[destination] = render_folder(source)
        converted[source.resolve()] = destination

    # Override aliases in every context, so inherited symlinks cannot select
    # the original, fixed-color folder instead of this theme's adapted SVG.
    for source in sorted(SOURCE.rglob("*.svg")):
        if not source.is_symlink():
            continue
        destination = converted.get(source.resolve())
        if destination is None:
            continue
        alias = Path("scalable") / source.relative_to(SOURCE)
        links[alias] = os.path.relpath(destination, alias.parent)

    directories = {p.parts[1] for p in files.keys() | links.keys()}
    if "apps" in directories:
        links[Path("scalable/categories")] = "apps"
        directories.add("categories")
    files[Path("index.theme")] = index_contents(directories)
    return files, links


def write_manifest(files, links, check):
    differences = []
    for relative, content in files.items():
        path = DESTINATION / relative
        if path.is_symlink():
            raise ValueError(f"Refusing to replace a symlink: {path}")
        if not path.is_file() or path.read_bytes() != content:
            differences.append(str(relative))
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
    for relative, target in links.items():
        path = DESTINATION / relative
        if os.path.lexists(path):
            if not path.is_symlink() or os.readlink(path) != target:
                raise ValueError(f"Refusing to replace an existing alias: {path}")
        else:
            differences.append(str(relative))
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.symlink_to(target)
    return differences


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="check that generated files match their sources without writing",
    )
    parser.add_argument(
        "--icons", nargs="+", default=folder_names(),
        help="original folder names to adapt (default: all original folders)",
    )
    args = parser.parse_args()
    if any(Path(name).name != name or not name.startswith("folder") for name in args.icons):
        parser.error("icon names must be folder basenames, without paths")
    files, links = build_manifest(args.icons)
    differences = write_manifest(files, links, args.check)
    if args.check and differences:
        print("Generated files differ: " + ", ".join(differences), file=sys.stderr)
        return 1
    print(f"Pixora Accent: {len(args.icons)} folders, {len(links)} aliases, check={args.check}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, ET.ParseError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
