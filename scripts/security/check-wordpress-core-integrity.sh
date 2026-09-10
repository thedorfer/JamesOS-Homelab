#!/usr/bin/env bash
set -euo pipefail

CONTAINER="${1:-wordpress-wordpress-1}"

docker exec "$CONTAINER" sh -lc '
set -eu

SRC=/usr/src/wordpress
WEB=/var/www/html

missing=/tmp/wp-core-missing.txt
mismatch=/tmp/wp-core-mismatch.txt
extra=/tmp/wp-core-extra.txt

: > "$missing"
: > "$mismatch"
: > "$extra"

echo "Comparing WordPress core against the copy shipped in this Docker image..."
echo "Source: $SRC"
echo "Web:    $WEB"
echo

cd "$SRC"

find . -type f \
    ! -path "./wp-content/*" \
    ! -name "wp-config-sample.php" \
    -print |
while IFS= read -r rel; do
    target="$WEB/${rel#./}"

    if [ ! -f "$target" ]; then
        echo "${rel#./}" >> "$missing"
        continue
    fi

    src_hash=$(sha256sum "$rel" | awk "{print \$1}")
    web_hash=$(sha256sum "$target" | awk "{print \$1}")

    if [ "$src_hash" != "$web_hash" ]; then
        echo "${rel#./}" >> "$mismatch"
    fi
done

# Unexpected files inside core-owned directories.
for dir in wp-admin wp-includes; do
    if [ -d "$WEB/$dir" ]; then
        find "$WEB/$dir" -type f -print |
        while IFS= read -r target; do
            rel="${target#"$WEB/"}"
            if [ ! -f "$SRC/$rel" ]; then
                echo "$rel" >> "$extra"
            fi
        done
    fi
done

missing_count=$(wc -l < "$missing")
mismatch_count=$(wc -l < "$mismatch")
extra_count=$(wc -l < "$extra")

echo "=== SUMMARY ==="
echo "Missing core files:    $missing_count"
echo "Modified core files:   $mismatch_count"
echo "Unexpected core files: $extra_count"
echo

echo "=== MISSING ==="
if [ "$missing_count" -eq 0 ]; then
    echo "None"
else
    cat "$missing"
fi

echo
echo "=== MODIFIED / HASH MISMATCH ==="
if [ "$mismatch_count" -eq 0 ]; then
    echo "None"
else
    cat "$mismatch"
fi

echo
echo "=== UNEXPECTED FILES IN wp-admin / wp-includes ==="
if [ "$extra_count" -eq 0 ]; then
    echo "None"
else
    cat "$extra"
fi

echo
echo "This check does NOT modify the site."
echo "wp-content and site-specific wp-config.php/.htaccess are intentionally excluded."
'
