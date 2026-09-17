"""Quarantine duplicated time ranges listed in duplicate.txt.

Each line of duplicate.txt is a path to a folder under h5data/. The folder is
moved to h5data/bad_data/ and its matching xml/ folder is removed.

h5data/3d_data_* is very often a SYMLINK into a data tree that lives outside
the checkout. os.rename moves the link itself; shutil.move would resolve it and
relocate the real files out of the user's data tree.
"""

import os
import shutil
import sys

root = sys.argv[1]
root = root if root.endswith('/') else root + '/'
duplicate_txt = os.path.join(root, 'bin/bw_many_folder_scripts/duplicate.txt')

with open(duplicate_txt) as f:
    f.readline()
    f.readline()
    for line in f:
        target = line.rstrip('\n').rstrip('/')
        if not target:
            continue
        print("rmdupes: ", target)

        h5data = os.path.dirname(target)
        name = os.path.basename(target)
        bad_data = os.path.join(h5data, 'bad_data')
        os.makedirs(bad_data, exist_ok=True)
        dest = os.path.join(bad_data, name)

        if not os.path.lexists(target):
            print("folder not found, please check h5folder: %s" % target)
        else:
            # clear any stale entry without following it
            if os.path.islink(dest):
                os.unlink(dest)
            elif os.path.isdir(dest):
                shutil.rmtree(dest)
            elif os.path.lexists(dest):
                os.unlink(dest)
            os.rename(target, dest)   # moves the link, never its target

        xml_dir = os.path.join(os.path.dirname(h5data), 'xml', name)
        if os.path.islink(xml_dir):
            os.unlink(xml_dir)
        elif os.path.isdir(xml_dir):
            shutil.rmtree(xml_dir)
        else:
            print("folder not found, skipped: %s" % xml_dir)
