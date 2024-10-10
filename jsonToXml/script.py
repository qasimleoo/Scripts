import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

def dict_to_xml(tag, d):
    element = ET.Element(tag)
    for key, val in d.items():
        child = ET.SubElement(element, key)
        if isinstance(val, dict):
            child.extend(dict_to_xml(key, val))
        elif isinstance(val, list):
            for item in val:
                sub_child = ET.SubElement(child, 'item')
                if isinstance(item, dict):
                    sub_child.extend(dict_to_xml('item', item))
                else:
                    sub_child.text = str(item)
        else:
            child.text = str(val)
    return element

def json_to_xml(json_obj, root_tag):
    root = dict_to_xml(root_tag, json_obj)
    return ET.tostring(root, encoding='unicode', method='xml')

def pretty_xml_with_apostrophes_and_commas(xml_str):
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="    ")
    lines = pretty_xml.splitlines()
    return ',\n'.join([f"`{line}`" for line in lines if line.strip() and not line.strip().startswith('<?xml')]) + ','

def convert_json_to_xml_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    root_tag = 'root'
    if any(key.lower() == 'error' for key in json_data.keys()):
        root_tag = 'ApiExceptionResponse'

    xml_data = json_to_xml(json_data, root_tag)
    formatted_xml = pretty_xml_with_apostrophes_and_commas(xml_data)

    with open(file_path, 'w') as file:
        file.write(formatted_xml)

file_path = '/home/qasim/JFreaks/Scripts/jsonToXml/file.json'
convert_json_to_xml_file(file_path)
