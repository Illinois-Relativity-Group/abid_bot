import os
import sys
import shutil
from glob import glob

# Usage:  python3 change_view.py [view_xml] [xml_dir]
#   view_xml : attribute file to stamp into every frame   (default below)
#   xml_dir  : which xml tree to write into -- "xml", "xml2", ...
#
# The xml_dir argument matters: renders read view_*.xml at RENDER time, so
# pointing this at the tree a running campaign is using will change its framing
# part-way through. Give a parallel run its own tree (xml2) and target that.

#XML file
default_view = "bin/bw_many_folder_scripts/atts/bhdisk_view_30deg_zoomin.xml" # bhdisk_view_30deg.xml bhdisk_view_meshmatch.xml bhdisk_view_30deg_superzoomin.xml

source_file = sys.argv[1] if len(sys.argv) > 1 else default_view
xml_dir     = sys.argv[2] if len(sys.argv) > 2 else "xml"

target_pattern = os.path.join(xml_dir, "3d_data_*", "view_*.xml")

# Verify source file exists
if not os.path.isfile(source_file):
    raise FileNotFoundError(f"Source file not found: {source_file}")

target_files = glob(target_pattern)

if not target_files:
    print(f"No target files found under {xml_dir}/.")
else:
    for target in target_files:
        shutil.copy2(source_file, target)

    print(f"Done! {len(target_files)} files updated in {xml_dir}/ from {os.path.basename(source_file)}")
