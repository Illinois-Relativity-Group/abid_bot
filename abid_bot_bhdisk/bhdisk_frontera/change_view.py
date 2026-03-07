import os
import shutil
from glob import glob

#XML file
source_file = "bin/bw_many_folder_scripts/atts/bhdisk_view_30deg_superzoomin_equatorial.xml" # bhdisk_view_30deg_zoomin.xml bhdisk_view_30deg.xml bhdisk_view_30deg_superzoomin_equatorial.xml bhdisk_view_30deg_superzoomin.xml


target_pattern = os.path.join("xml", "3d_data_*", "view_*.xml")

# Verify source file exists
if not os.path.isfile(source_file):
    raise FileNotFoundError(f"Source file not found: {source_file}")

target_files = glob(target_pattern)

if not target_files:
    print("No target files found.")
else:
    for target in target_files:
        shutil.copy2(source_file, target)
        print(f"Replaced: {target}")

    print(f"\nDone! {len(target_files)} files updated.")