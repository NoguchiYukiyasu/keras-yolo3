import xml.etree.ElementTree as ET
from os import getcwd
import os
import glob

classes = ["urchin", "urchin_hatena", "seaweed","urchin_hatena2"]
jpeg_xml_folder = "jpeg_xml_files"#"local_path"
output_annotation_name = "annotations.txt"
output_class_file_name = "class.txt"


wd = getcwd()
list_file = open(output_annotation_name, 'w', encoding="utf-8_sig")
buff_list = glob.glob("./"+jpeg_xml_folder+"/*")
image_list = []
no_xml_file_list = []
for file_name in buff_list:
    base, ext = os.path.splitext(file_name)
    print(base)
    if (ext == ".jpeg") or (ext == ".jpg") or (ext == ".JPEG") or (ext == ".JPG"):
        image_list.append(file_name)
for image_name in image_list:
    if os.path.exists(os.path.splitext(image_name)[0]+".xml"):
        in_file = open(os.path.splitext(image_name)[0]+".xml", encoding="utf-8_sig")
    else:
        no_xml_file_list.append(image_name)
        continue
    list_file.write(wd+"/"+image_name)
    tree = ET.parse(in_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
    list_file.write('\n')
print("No xml file:", no_xml_file_list)
list_file.close()

class_file = open(output_class_file_name, 'w', encoding="utf-8_sig")
for class_name in classes:
    class_file.write(class_name+'\n')
class_file.close()
