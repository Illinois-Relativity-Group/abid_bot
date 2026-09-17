#!/bin/bash
#
# link_h5data.sh -- build $root/h5data from the raw simulation output on riemann.
#
# On riemann the ~3.5 TB of sol_32 output lives outside the abid_bot tree, in
# $h5src (see params). This script:
#   1. renames every raw date folder  YY_MM_DD_HHMMSS  ->  3d_data_YY_MM_DD_HHMMSS
#      in place in $h5src, and
#   2. symlinks each of those, plus the diagnostics files and horizon/ from
#      $h5src/data, into $root/h5data/.
#
# Symlinks, not copies: the data is far too big to duplicate, and this is the
# same layout the other abid_bot installs on riemann use.
#
# Safe to re-run: existing links are refreshed, already-renamed folders skipped.
#
# Usage:  . params ; . bin/link_h5data.sh

if [ -z "$root" ] || [ -z "$h5src" ]; then
	echo "link_h5data.sh: \$root and \$h5src must be set -- source params first"
	return 1 2>/dev/null || exit 1
fi

h5data=$root/h5data
mkdir -p $h5data

echo "raw data source : $h5src"
echo "target          : $h5data"

########## 1. pull the May folders up into the main tree ##########
# sol32_may_hdf5/ holds the 26_05_05..26_05_25 folders that are missing from
# the top level -- move them up so every date sits in one folder.
if [ -d "$h5src/sol32_may_hdf5" ]; then
	echo "merging sol32_may_hdf5/ into $h5src"
	for d in $h5src/sol32_may_hdf5/*/; do
		[ -d "$d" ] || continue
		b=$(basename -- "$d")
		if [ -e "$h5src/$b" ] || [ -e "$h5src/3d_data_$b" ]; then
			# 6 of the May dates (26_05_01..26_05_05) exist at the top
			# level with the full 128 rho_b files, while the copy in
			# sol32_may_hdf5 is an empty stub. Keep the full one.
			if [ -z "$(ls -A "$d" 2>/dev/null)" ]; then
				rmdir "$d" && echo "	dropped empty duplicate: $b"
			else
				echo "	already present, skipping: $b"
			fi
		else
			mv -- "$d" "$h5src/$b"
		fi
	done
	rmdir $h5src/sol32_may_hdf5 2>/dev/null && echo "	sol32_may_hdf5/ now empty, removed"
fi

########## 2. prefix the raw date folders with 3d_data_ ##########
renamed=0
for d in $h5src/*/; do
	b=$(basename -- "$d")
	# only YY_MM_DD_HHMMSS folders -- leaves data/, 3d_data_*, etc. alone
	if [[ "$b" =~ ^[0-9]{2}_[0-9]{2}_[0-9]{2}_[0-9]{6}$ ]]; then
		if [ -e "$h5src/3d_data_$b" ]; then
			# A previous pass may have left an EMPTY 3d_data_<date> here
			# (folder had no output at the time). If the incoming folder
			# actually has data, it wins.
			if [ -z "$(ls -A "$h5src/3d_data_$b" 2>/dev/null)" ] && [ -n "$(ls -A "$h5src/$b" 2>/dev/null)" ]; then
				rmdir "$h5src/3d_data_$b"
				mv -- "$h5src/$b" "$h5src/3d_data_$b"
				echo "	filled previously-empty 3d_data_$b"
				renamed=$((renamed+1))
			else
				# Both have data: fold in only files the target lacks
				# (these tars re-ship folders we already hold, plus extra
				# variables). Existing files are never overwritten.
				added=0
				for nf in "$h5src/$b"/*; do
					[ -e "$nf" ] || continue
					nb=$(basename -- "$nf")
					if [ ! -e "$h5src/3d_data_$b/$nb" ]; then
						mv -- "$nf" "$h5src/3d_data_$b/$nb"
						added=$((added+1))
					fi
				done
				left=$(ls -A "$h5src/$b" 2>/dev/null | wc -l)
				if [ "$left" -eq 0 ]; then
					rmdir "$h5src/$b"
					echo "	3d_data_$b: merged $added new file(s), duplicate dir removed"
				else
					echo "	3d_data_$b: merged $added new file(s), $left already-present file(s) left in $b"
				fi
			fi
		else
			mv -- "$h5src/$b" "$h5src/3d_data_$b"
			renamed=$((renamed+1))
		fi
	fi
done
echo "renamed $renamed folders to 3d_data_*"

########## 2b. un-quarantine folders that now have data ##########
# clean_h5folders.sh moves empty 3d_data_* into h5data/bad_data/ and never
# moves them back. If the data has since arrived, drop the stale entry so the
# folder gets linked normally again.
if [ -d "$h5data/bad_data" ]; then
	for l in "$h5data"/bad_data/3d_data_*; do
		[ -e "$l" ] || [ -L "$l" ] || continue
		b=$(basename -- "$l")
		# require actual .h5 data, not just "some file" -- restart folders
		# can hold only CCTK_Proc1.out and would otherwise be released,
		# occupy a folder index and render nothing.
		if ls "$h5src/$b"/*.h5 >/dev/null 2>&1; then
			rm -rf -- "$l"
			echo "	$b has data again, released from bad_data"
		fi
	done
fi

########## 3. link the data folders into h5data ##########
# drop stale links first so removed/renamed data doesn't linger
find $h5data -maxdepth 1 -name '3d_data_*' -type l -delete
n=0
for d in $h5src/3d_data_*/; do
	[ -d "$d" ] || continue
	b=$(basename -- "$d")
	ln -sfn -- "${d%/}" "$h5data/$b"
	n=$((n+1))
done
echo "linked $n 3d_data_* folders"

########## 4. link the diagnostics and horizon data ##########
# $h5src/data holds bhns.xon, bhns.mon, bhns_BHspin.mon, horizon/, ... --
# everything setup.sh expects to find alongside the 3d_data_* folders.
if [ -d "$h5src/data" ]; then
	# BH_diagnostics.ah1.gp exists in two places and the code reads BOTH:
	# setup_spinvtk_dimensionless.py reads horizon/all_horizon/, while other
	# steps read the top-level copy. Keep one source of truth so refreshing
	# the data can't leave them disagreeing.
	diag_h=$h5src/data/horizon/all_horizon/BH_diagnostics.ah1.gp
	diag_t=$h5src/data/BH_diagnostics.ah1.gp
	if [ -f "$diag_h" ] && [ -f "$diag_t" ] && ! cmp -s "$diag_h" "$diag_t"; then
		echo "WARNING: the two BH_diagnostics.ah1.gp copies differ:"
		echo "	$diag_t    (ends t=$(tail -1 $diag_t | awk '{print $2}'))"
		echo "	$diag_h    (ends t=$(tail -1 $diag_h | awk '{print $2}'))"
		echo "	using the horizon/all_horizon copy for both."
	fi

	for f in $h5src/data/*; do
		b=$(basename -- "$f")
		# always take BH_diagnostics from horizon/all_horizon
		if [ "$b" = "BH_diagnostics.ah1.gp" ] && [ -f "$diag_h" ]; then
			ln -sfn -- "$diag_h" "$h5data/$b"
			continue
		fi
		# don't clobber the box/line geometry that ships with the repo
		case "$b" in
			box.3d|cube_edges.3d|cube_edges_old.3d|line.3d|makebox.py|make_line.py)
				[ -e "$h5data/$b" ] && continue ;;
		esac
		ln -sfn -- "$f" "$h5data/$b"
	done
	echo "linked diagnostics + horizon/ from $h5src/data"
else
	echo "WARNING: $h5src/data not found -- no horizon/ or .mon files linked"
fi

echo "h5data ready: $(ls -d $h5data/3d_data_* 2>/dev/null | wc -l) data folders"
