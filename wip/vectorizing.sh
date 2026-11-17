#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/16x16"
OUT_DIR="$SCRIPT_DIR/svg"

for tool in bash parallel magick vtracer python3 scour; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "Missing dependency: $tool" >&2
        exit 1
    fi
done

PYTHON="$(command -v python3)"
if ! "$PYTHON" -c 'from lxml import etree'; then
    echo 'Python needs lxml. Use python3.withPackages (ps: [ ps.lxml ]) in Nix.' >&2
    exit 1
fi

[[ -d "$SRC_DIR" ]] || {
    echo "Missing source directory: $SRC_DIR" >&2
    exit 1
}

[[ -f "$SCRIPT_DIR/svgfit.py" ]] || {
    echo 'Missing svgfit.py beside this script.' >&2
    exit 1
}

TMP_DIR="$(mktemp -d "$SCRIPT_DIR/tmp-512.XXXXXX")"

cleanup() {
    local status=$?
    if (( status == 0 )); then
        rm -rf -- "$TMP_DIR"
    else
        echo "Failed. Intermediate files preserved in: $TMP_DIR" >&2
    fi
}
trap cleanup EXIT

find "$SRC_DIR" -type f -name '*.png' -print0 > "$TMP_DIR/inputs"

if [[ ! -s "$TMP_DIR/inputs" ]]; then
    echo "No PNG files found in: $SRC_DIR" >&2
    exit 1
fi

mkdir -p -- "$OUT_DIR"

process_image() {
    # Parallel runs each job in a separate shell.
    set -euo pipefail

    local img="$1" rel base output
    rel="${img#"$SRC_DIR"/}"
    base="$TMP_DIR/${rel%.png}"
    output="$OUT_DIR/${rel%.png}.svg"

    mkdir -p -- "$(dirname -- "$base")" "$(dirname -- "$output")"

    # Upscale using nearest-neighbor interpolation.
    magick "$img" -filter point -resize 512x512 "$base-512.png"

    # Trace the upscaled image.
    vtracer \
        --input "$base-512.png" \
        --output "$base-traced.svg" \
        --colormode color \
        --hierarchical cutout \
        --mode pixel

    sed -i 's/<svg /<svg shape-rendering="crispEdges" /' \
        "$base-traced.svg"

    # Fit the SVG to its visible content.
    "$PYTHON" "$SCRIPT_DIR/svgfit.py" \
        "$base-traced.svg" "$base-fit.svg"

    # Optimize before publishing the finished file.
    scour \
        -i "$base-fit.svg" \
        -o "$base-clean.svg" \
        --enable-id-stripping \
        --enable-comment-stripping \
        --shorten-ids \
        --indent=none \
        >/dev/null

    mv -- "$base-clean.svg" "$output"
}

export SCRIPT_DIR SRC_DIR OUT_DIR TMP_DIR PYTHON
export PARALLEL_SHELL="$(command -v bash)"
export -f process_image

parallel --null --halt soon,fail=1 --eta --bar \
    process_image {} :::: "$TMP_DIR/inputs"

echo "Done. SVGs saved in $OUT_DIR"
