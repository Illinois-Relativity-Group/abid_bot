#!/bin/bash
# Install the colour tables the atts/ files reference into ~/.visit, where VisIt looks for them.
#
# WHY THIS EXISTS: an att with opacityType=ColorTable takes its per-shell alphas ENTIRELY from the
# named table. If VisIt cannot resolve the name it falls back silently -- no error, no warning, just
# a plot with the wrong opacity. NSNS_pseudo_disk_diskGW.xml names "bhdisk_opaque", so without this
# step a fresh checkout renders the disk wrong and nothing says so.
#
# Non-destructive: an existing table of the same name is NEVER overwritten (you may have tuned it).
# It is reported instead, so you can diff and decide.
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
src="$here/bw_many_folder_scripts/atts"
dst="$HOME/.visit"
mkdir -p "$dst"
inst=0; kept=0; same=0
for f in "$src"/*.ct; do
        [ -e "$f" ] || continue
        b=$(basename "$f")
        if [ ! -e "$dst/$b" ]; then
                cp "$f" "$dst/$b"; inst=$((inst+1))
        elif ! cmp -s "$f" "$dst/$b"; then
                echo "  colortable: $b differs from ~/.visit/$b -- keeping yours"; kept=$((kept+1))
        else
                same=$((same+1))
        fi
done
echo "colortables: $inst installed into $dst, $same already current, $kept left alone (differ)"
