#!/usr/bin/env python3
"""
Rewrite an SVG's viewBox to tightly fit its visible path content.
Handles relative path commands and translate() transforms.
Usage: python3 svgfit.py <input.svg> <output.svg>
"""

import sys
import re
from lxml import etree


def parse_transform_translate(transform):
    """Extract tx, ty from translate(tx) or translate(tx, ty)."""
    if not transform:
        return 0.0, 0.0
    m = re.search(r'translate\(\s*([-\d.]+)(?:[,\s]\s*([-\d.]+))?\s*\)', transform)
    if not m:
        return 0.0, 0.0
    tx = float(m.group(1))
    ty = float(m.group(2)) if m.group(2) else 0.0
    return tx, ty


def parse_path_bbox(d, tx=0.0, ty=0.0):
    """
    Compute bounding box of a path, accounting for a translate offset.
    Handles both absolute (M L H V C S Q T A Z) and
    relative (m l h v c s q t a z) commands.
    """
    tokens = re.findall(
        r'[MLHVCSQTAZmlhvcsqtaz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?',
        d
    )

    xs, ys = [], []
    i = 0
    cmd = None
    cx, cy = 0.0, 0.0   # current point
    sx, sy = 0.0, 0.0   # subpath start (for Z)

    def num(offset=0):
        return float(tokens[i + offset])

    while i < len(tokens):
        t = tokens[i]
        if t.isalpha():
            cmd = t
            i += 1
            continue

        try:
            if cmd == 'M':
                cx, cy = num(0), num(1); sx, sy = cx, cy
                xs.append(cx + tx); ys.append(cy + ty); i += 2
            elif cmd == 'm':
                cx += num(0); cy += num(1); sx, sy = cx, cy
                xs.append(cx + tx); ys.append(cy + ty); i += 2

            elif cmd == 'L':
                cx, cy = num(0), num(1)
                xs.append(cx + tx); ys.append(cy + ty); i += 2
            elif cmd == 'l':
                cx += num(0); cy += num(1)
                xs.append(cx + tx); ys.append(cy + ty); i += 2

            elif cmd == 'H':
                cx = num(0); xs.append(cx + tx); i += 1
            elif cmd == 'h':
                cx += num(0); xs.append(cx + tx); i += 1

            elif cmd == 'V':
                cy = num(0); ys.append(cy + ty); i += 1
            elif cmd == 'v':
                cy += num(0); ys.append(cy + ty); i += 1

            elif cmd == 'C':
                xs += [num(0)+tx, num(2)+tx, num(4)+tx]
                ys += [num(1)+ty, num(3)+ty, num(5)+ty]
                cx, cy = num(4), num(5); i += 6
            elif cmd == 'c':
                xs += [cx+num(0)+tx, cx+num(2)+tx, cx+num(4)+tx]
                ys += [cy+num(1)+ty, cy+num(3)+ty, cy+num(5)+ty]
                cx += num(4); cy += num(5); i += 6

            elif cmd == 'S':
                xs += [num(0)+tx, num(2)+tx]; ys += [num(1)+ty, num(3)+ty]
                cx, cy = num(2), num(3); i += 4
            elif cmd == 's':
                xs += [cx+num(0)+tx, cx+num(2)+tx]
                ys += [cy+num(1)+ty, cy+num(3)+ty]
                cx += num(2); cy += num(3); i += 4

            elif cmd == 'Q':
                xs += [num(0)+tx, num(2)+tx]; ys += [num(1)+ty, num(3)+ty]
                cx, cy = num(2), num(3); i += 4
            elif cmd == 'q':
                xs += [cx+num(0)+tx, cx+num(2)+tx]
                ys += [cy+num(1)+ty, cy+num(3)+ty]
                cx += num(2); cy += num(3); i += 4

            elif cmd == 'T':
                cx, cy = num(0), num(1)
                xs.append(cx + tx); ys.append(cy + ty); i += 2
            elif cmd == 't':
                cx += num(0); cy += num(1)
                xs.append(cx + tx); ys.append(cy + ty); i += 2

            elif cmd == 'A':
                cx, cy = num(5), num(6)
                xs.append(cx + tx); ys.append(cy + ty); i += 7
            elif cmd == 'a':
                cx += num(5); cy += num(6)
                xs.append(cx + tx); ys.append(cy + ty); i += 7

            elif cmd in ('Z', 'z'):
                cx, cy = sx, sy
                i += 0
                break
            else:
                i += 1

        except (IndexError, ValueError):
            break

    if not xs or not ys:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def is_transparent(fill):
    fill = fill.strip().lower()
    if fill in ('none', 'transparent', ''):
        return True
    if fill.startswith('#') and len(fill) == 9:
        return int(fill[7:9], 16) == 0
    if fill.startswith('#') and len(fill) == 5:
        return int(fill[4], 16) == 0
    return False


def fit_viewbox(input_path, output_path):
    tree = etree.parse(input_path)
    root = tree.getroot()

    all_x1, all_y1, all_x2, all_y2 = [], [], [], []

    for path in root.iter('{http://www.w3.org/2000/svg}path'):
        d = path.get('d', '')
        if not d:
            continue

        fill = path.get('fill', '')
        if is_transparent(fill):
            continue

        tx, ty = parse_transform_translate(path.get('transform', ''))
        bbox = parse_path_bbox(d, tx, ty)
        if bbox is None:
            continue

        x1, y1, x2, y2 = bbox
        all_x1.append(x1); all_y1.append(y1)
        all_x2.append(x2); all_y2.append(y2)

    if not all_x1:
        with open(output_path, 'w') as f:
            f.write(etree.tostring(root, encoding='unicode'))
        return

    min_x = min(all_x1)
    min_y = min(all_y1)
    max_x = max(all_x2)
    max_y = max(all_y2)

    w = round(max_x - min_x, 4)
    h = round(max_y - min_y, 4)
    vb = f"{round(min_x, 4)} {round(min_y, 4)} {w} {h}"

    root.set('viewBox', vb)
    root.set('width', str(w))
    root.set('height', str(h))

    with open(output_path, 'w') as f:
        f.write(etree.tostring(root, encoding='unicode'))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.svg output.svg", file=sys.stderr)
        sys.exit(1)
    fit_viewbox(sys.argv[1], sys.argv[2])
