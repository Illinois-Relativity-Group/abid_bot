import numpy as np 
import os
import xml.etree.ElementTree as ET
import argparse

parser = argparse.ArgumentParser(description = "goes through the xml directory, changes the view setting so that resulting movie would have a progressive zoom out")
parser.add_argument("xml_directory", type=str, help="input path to xml directory")
parser.add_argument("xmlfile", type=str, help="the xml file we want to modify")
parser.add_argument("zoomin", type=float, help="imageZoom number for Zoom In")
parser.add_argument("zoomout", type=float, help="imageZoom number foor Zoom Out")
args = parser.parse_args()


def xml_editor(xml_directory, xmlfile, zoomin, zoomout):
    xml_paths = []
    for paths, directories, files in os.walk(xml_directory):
        if len(directories) == 0:
            xml_paths.append(os.path.join(paths, xmlfile))
    xml_paths.sort()
    view_range = np.linspace(zoomin, zoomout, len(xml_paths), endpoint = True)
    for i in range(len(xml_paths)):
        if (os.path.exists(xml_paths[i])):
            xml_tree = ET.parse(xml_paths[i])
            root = xml_tree.getroot()
            for child in root.iter("Field"):
                if child.get("name") == "imageZoom":
                    child.text = str(view_range[i])
            xml_tree.write(xml_paths[i], encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    xml_editor(args.xml_directory, args.xmlfile, args.zoomin, args.zoomout)
