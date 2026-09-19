#!/bin/bash
# Resume an interrupted runMulti campaign: render only the frames whose PNG is missing.
#
#   ./renderMissing.sh [setN] [NPAR]
#
# WHY: runMulti.sh creates a fresh timestamped movies/ and log/ directory on every launch and has no
# skip logic, so a campaign that dies partway cannot be continued -- relaunching re-renders every
# frame into a new directory. This reads the job scripts runMulti.sh already wrote, drops every frame
# whose PNG exists, and runs the remainder into the SAME movies/ directory.
#
# It reuses the newest log/<DATE>_<jobName>/ for the jobName in params$setN, so run it after the
# runMulti campaign you want to finish. Nothing is re-rendered and nothing is overwritten.
#
# NPAR defaults to maxParallel from params. Note that more is not always faster: each frame is a
# fresh `visit -cli` (serial engine, ~1 core) that random-reads a large HDF5 file, so the ceiling is
# the storage, not the cores. A 40-way run here thrashed the array -- queue depth 42, zero frames in
# 12 minutes -- once the page cache was evicted by other writes. 24-30 has been the sweet spot.
set -u
cd "$(dirname "$0")"
# NOTE: params defines its own $root (the shipped template is /CHANGE/ME/abid_bot), so use the
# script's own location instead -- renderMissing.sh always sits at the tree root.
here=$(pwd)

setN="${1:-}"
if [[ -f "params$setN" ]]; then . "params$setN"; else echo "params$setN not found; using params"; . params; fi
NPAR="${2:-${maxParallel:-16}}"

# The job template carries the PATH to VisIt; source it so a resumed run has the same environment
# as the original campaign.
[ -f "$here/bin/scheduler/multirun_template_riemann" ] && . "$here/bin/scheduler/multirun_template_riemann"

# Which campaign to resume. jobName lives in runMulti<setN>.sh, not in params, so read it from
# there when that script exists; otherwise fall back to the most recent log/ directory. JOBNAME=...
# overrides both when several campaigns are interleaved.
jobName="${JOBNAME:-}"
if [ -z "$jobName" ] && [ -f "$here/runMulti$setN.sh" ]; then
        jobName=$(sed -n 's/^[[:space:]]*jobName=\([^#[:space:]]*\).*/\1/p' "$here/runMulti$setN.sh" | tail -1)
fi
if [ -n "$jobName" ]; then
        LOGDIR=$(ls -dt "$here"/log/*_"$jobName" 2>/dev/null | head -1)
else
        LOGDIR=$(ls -dt "$here"/log/*/ 2>/dev/null | head -1)
fi
[ -n "${LOGDIR:-}" ] || { echo "no campaign found under $root/log -- run runMulti.sh first"; exit 1; }
LOGDIR=${LOGDIR%/}
echo "resuming: $LOGDIR${jobName:+  (jobName=$jobName)}"

# Track this run by pid file. Do NOT manage it with `pkill -f <pattern>`: the pattern matches the
# managing shell's own command line and kills it.
echo $$ > "$here/.renderMissing${setN}.pid"

WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
cat "$LOGDIR"/job/job*.sh > "$WORK/all.txt" 2>/dev/null
: > "$WORK/todo.txt"
while IFS= read -r line; do
        [ -z "$line" ] && continue
        # the output prefix is the token containing /movies/; VisIt appends <frame>.png
        pre=$(printf '%s\n' "$line" | tr ' ' '\n' | grep '/movies/' | head -1)
        [ -z "$pre" ] && continue
        compgen -G "${pre}*.png" > /dev/null && continue        # already rendered -> skip
        printf '%s\n' "$line" >> "$WORK/todo.txt"
done < "$WORK/all.txt"

TOT=$(wc -l < "$WORK/all.txt"); TODO=$(wc -l < "$WORK/todo.txt")
echo "$(date '+%H:%M:%S') frames total=$TOT already=$((TOT-TODO)) todo=$TODO  NPAR=$NPAR"
[ "$TODO" -eq 0 ] && { echo "nothing to do"; exit 0; }

# </dev/null: visit -cli reads stdin and will swallow the job list otherwise.
xargs -a "$WORK/todo.txt" -d '\n' -P "$NPAR" -I{} bash -c '{} < /dev/null > /dev/null 2>&1'

PICS=$(ls -dt "$here"/movies/"$(basename "$LOGDIR")" 2>/dev/null | head -1)
echo "$(date '+%H:%M:%S') done; frames now = $(find "$PICS" -name '*.png' 2>/dev/null | wc -l) / $TOT"
