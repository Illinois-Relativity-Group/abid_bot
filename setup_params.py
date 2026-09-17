#!/usr/bin/env python3
"""Derive the case-specific params fields from the data in h5data/.

Scans every h5data/3d_data_*/ folder whose rho_b.file_0.h5 can be read by
h5dump, and from them derives it, dt, firstTime, offset, maxdensity and M,
then rewrites those fields in ./params.

dt is derived from the h5 file's own 'time' attribute (paired with the
iteration number baked into each dataset's name), not from bhns.xon row
spacing -- bhns.xon rows are not reliably it/3 apart across datasets, so a
fixed-offset formula against it silently gives the wrong dt. The old
bhns.xon-based value is still computed and printed alongside the derived
one purely so the discrepancy is visible rather than silent.

overlap.txt (and the frame numbering built from it) is ordered by
ITERATION, so frame 0 is the earliest iteration -- not the folder that
happens to sort first by name. Folder names are wall-clock timestamps and
their sort order need not match iteration order, and real datasets contain
corrupt/truncated snapshot folders. So every 3d_data_* folder with a
readable rho_b.file_0.h5 is scanned, "it" is taken from any one of them
(they all share the same iteration spacing), "first_iter" is the MINIMUM
first-iteration seen across all of them, and any folder h5dump cannot read
is skipped rather than treated as fatal -- the run only dies if none of
the folders are readable.

A field is only rewritten while it still holds the placeholder shipped with
the branch. If you have already set a value yourself it is kept, and a
warning is printed when the derived value disagrees by more than 1%.

Run from the abid_bot root, after h5data/ is populated:  python3 setup_params.py
"""

import os
import re
import subprocess
import sys

PLACEHOLDERS = {
    "it": {"512"},
    "dt": {"0.0"},
    "M": {"0.0"},
    "maxdensity": {"0.0"},
    "firstTime": {"00000.00000000000"},
    "offset": {"0"},
}
TOL = 0.01


def die(msg):
    print("setup_params: %s" % msg, file=sys.stderr)
    raise SystemExit(1)


def data_dirs(h5dir):
    """All 3d_data_* subfolders of h5dir that contain a rho_b.file_0.h5,
    in a fixed (sorted-by-name) but not necessarily iteration order."""
    names = sorted(n for n in os.listdir(h5dir)
                   if n.startswith("3d_data_") and os.path.isdir(os.path.join(h5dir, n)))
    return [n for n in names
            if os.path.exists(os.path.join(h5dir, n, "rho_b.file_0.h5"))]


def read_timesteps(h5file):
    """Sorted distinct 'timestep' attribute values in h5file, or None if
    h5dump cannot read the file (corrupt/truncated -- this happens in real
    datasets and is not fatal by itself)."""
    try:
        proc = subprocess.run(["h5dump", "-N", "timestep", h5file],
                               capture_output=True, text=True)
    except FileNotFoundError:
        die("h5dump not found on PATH")
    if proc.returncode != 0:
        return None
    vals = sorted({int(m) for m in re.findall(r"\(0\): (\d+)", proc.stdout)})
    return vals or None


def read_time_pairs(h5file):
    """{iteration: time} built from every dataset in h5file, by reading the
    'it=<n> tl=0 rl=0 c=0' tag baked into each dataset's name alongside its
    own 'time' attribute. None if h5dump cannot read the file.

    This is the authoritative source for dt: it is the actual coordinate
    time Cactus/Carpet stamped on that iteration, unlike bhns.xon row
    spacing (see dt_xon below), which silently assumes monitor rows are
    written every it/3 iterations -- true only by coincidence in some
    datasets."""
    try:
        proc = subprocess.run(["h5dump", "-A", h5file],
                               capture_output=True, text=True)
    except FileNotFoundError:
        die("h5dump not found on PATH")
    if proc.returncode != 0:
        return None
    pairs = {}
    for block in proc.stdout.split('DATASET "')[1:]:
        m_it = re.search(r'it=(\d+) tl=0 rl=0 c=0', block)
        m_time = re.search(r'ATTRIBUTE "time"[\s\S]*?\(0\): ([-\d.eE+]+)', block)
        if m_it and m_time:
            pairs.setdefault(int(m_it.group(1)), float(m_time.group(1)))
    return pairs or None


def data_rows(path, ncol):
    rows = []
    with open(path, errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line or line[0] in "#T":
                continue
            parts = line.split()
            if len(parts) > ncol:
                rows.append(parts)
    if not rows:
        die("no data rows in %s" % path)
    return rows


def current(params_text, name):
    m = re.search(r'^%s="?([^"#\n]*)"?' % re.escape(name), params_text, re.M)
    return m.group(1).strip() if m else None


def rewrite(params_text, name, value, quoted=True):
    repl = '%s=%s' % (name, '"%s"' % value if quoted else value)
    return re.sub(r'^%s=[^\n]*' % re.escape(name), repl, params_text, count=1, flags=re.M)


def main():
    root = os.getcwd()
    h5dir = os.path.join(root, "h5data")
    if not os.path.isdir(h5dir):
        die("no h5data/ here -- run this from the abid_bot root")

    dirs = data_dirs(h5dir)
    if not dirs:
        die("no 3d_data_* folder in %s contains rho_b.file_0.h5" % h5dir)

    it = None
    it_dir = None
    it_vals = None
    first_iter = None
    skipped = 0
    for n in dirs:
        vals = read_timesteps(os.path.join(h5dir, n, "rho_b.file_0.h5"))
        if vals is None:
            print("  skipping %s -- rho_b.file_0.h5 unreadable by h5dump" % n)
            skipped += 1
            continue
        folder_it = vals[1] - vals[0] if len(vals) > 1 else vals[0]
        if it is None:
            it = folder_it
            it_dir = n
            it_vals = vals
        if first_iter is None or vals[0] < first_iter:
            first_iter = vals[0]

    if it is None:
        die("none of the %d 3d_data_* folders in %s have a readable rho_b.file_0.h5"
            % (len(dirs), h5dir))

    print("scanned %d 3d_data_* folders, skipped %d unreadable, used %d"
          % (len(dirs), skipped, len(dirs) - skipped))
    print("it=%d  first_iter=%d (minimum across readable folders)" % (it, first_iter))

    # dt: derive it from the h5 file's own 'time' attribute, paired with the
    # iteration tag baked into each dataset name, for the same folder that
    # gave us `it` above. The old bhns.xon-row-spacing formula (kept below,
    # dt_xon) assumes monitor rows are written every it/3 iterations, which
    # does not hold in general (these runs write bhns.xon every 256
    # iterations, not it/3=170.67) and silently gives the wrong dt.
    if len(it_vals) < 2:
        die("%s has only one iteration in rho_b.file_0.h5 -- cannot derive dt "
            "from the h5 time attribute" % it_dir)
    time_pairs = read_time_pairs(os.path.join(h5dir, it_dir, "rho_b.file_0.h5"))
    if time_pairs is None:
        die("h5dump -A could not read time attributes from %s/rho_b.file_0.h5" % it_dir)
    try:
        t0 = time_pairs[it_vals[0]]
        t1 = time_pairs[it_vals[1]]
    except KeyError as exc:
        die("no 'time' attribute found for iteration %s in %s" % (exc, it_dir))
    dt_h5 = (t1 - t0) / (it_vals[1] - it_vals[0]) * it

    # bhns.xon is still read here -- dt_xon is kept only as a visible sanity
    # comparison (see the printout below), and firstTime is derived from
    # dt_h5, not from bhns.xon.
    xon = data_rows(os.path.join(h5dir, "bhns.xon"), 0)
    dt_xon = float(xon[3][0]) - float(xon[0][0])

    dt = dt_h5

    # offset is what makes t/M correct when the data does not start at
    # iteration 0. setmovie.py names each frame time_<(frame+offset)*dt/M>.txt
    # and runModule.py reads the label out of that filename.
    if first_iter % it:
        die("first iteration %d is not a multiple of it=%d" % (first_iter, it))
    offset = first_iter // it
    first_time = "%017.11f" % (offset * dt)

    mon = data_rows(os.path.join(h5dir, "bhns.mon"), 12)
    maxdensity = float(mon[0][8])
    M = float(mon[0][11]) + float(mon[0][12])

    derived = {
        "it": (str(it), False),
        "dt": (repr(dt), True),
        "offset": (str(offset), False),
        "firstTime": (first_time, True),
        "maxdensity": (repr(maxdensity), True),
        "M": (repr(M), True),
    }

    path = os.path.join(root, "params")
    text = open(path).read()

    print("  dt from h5 time attr : %.10f" % dt_h5)
    print("  dt from bhns.xon rows: %.10f   (upstream formula; assumes xon rows are it/3 apart)" % dt_xon)
    print("  dt currently in params: %s" % current(text, "dt"))

    for name, (value, quoted) in derived.items():
        cur = current(text, name)
        if cur is None:
            print("  %-11s not found in params, skipped" % name)
            continue
        if cur in PLACEHOLDERS[name]:
            text = rewrite(text, name, value, quoted)
            print("  %-11s = %s" % (name, value))
            continue
        try:
            differs = abs(float(cur) - float(value)) > TOL * max(abs(float(value)), 1e-30)
        except ValueError:
            differs = cur != value
        if differs:
            print("  %-11s KEPT %s (derived %s -- differs by more than %d%%)"
                  % (name, cur, value, TOL * 100))
        else:
            print("  %-11s = %s (already set)" % (name, cur))
    open(path, "w").write(text)
    print("params updated")


if __name__ == "__main__":
    main()
