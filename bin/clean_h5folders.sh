echo "cleaning h5 and xml folders"
cur=$PWD

# This file is sourced (setup.sh does ". $bin/clean_h5folders.sh"), and setup.sh
# is itself sourced, so an "exit" here would close the user's shell. Every
# failure below returns instead.
if [ -z "$root" ]; then
	echo "clean_h5folders: \$root is not set -- source params first. Aborting." >&2
	return 1 2>/dev/null || exit 1
fi
if [ ! -d "$root/h5data" ]; then
	echo "clean_h5folders: no $root/h5data. Aborting." >&2
	return 1 2>/dev/null || exit 1
fi

# quoted, and only ever a directory we just confirmed lives under $root
if [ -d "$root/xml$1" ]; then
	rm -rf "$root/xml$1/"
fi

cd "$root/h5data/" || { echo "clean_h5folders: cannot cd to $root/h5data" >&2; return 1 2>/dev/null || exit 1; }
bad_data=$root/h5data/bad_data

if [ ! -d "$bad_data" ]; then
	mkdir "$bad_data"
	chmod 770 "$bad_data"
fi

for i in $(ls -d 3d_data* 2>/dev/null)
do
	# A folder is unusable if it has no *.h5, not merely if it is empty:
	# restart folders often contain only CCTK_Proc1.out, which slips past a
	# file-count test, renders no frames, and still consumes a folder index.
	if ! ls "$i"/*.h5 >/dev/null 2>&1
	then
		# A stale symlink here is just a pointer -- drop it. A stale
		# DIRECTORY is real quarantined data somebody may still want, so
		# move it aside rather than delete it.
		if [ -L "$bad_data/$i" ]; then
			rm -f "$bad_data/$i"
		elif [ -e "$bad_data/$i" ]; then
			n=1
			while [ -e "$bad_data/$i.prev$n" ]; do n=$((n+1)); done
			echo "clean_h5folders: keeping earlier $i as bad_data/$i.prev$n"
			mv -T "$bad_data/$i" "$bad_data/$i.prev$n"
		fi
		# -T so an existing bad_data/$i entry is replaced, not descended
		# into (that produced self-referential links inside the data dirs).
		mv -T "$i" "$bad_data/$i"
	fi
done
cd "$cur"
