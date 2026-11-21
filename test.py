
from api import JSON_DIR, ROOT_DIR
import json

with open(f"{JSON_DIR}/DailyGroup.json", "r") as f:
    data = json.load(f)
print(data['DailyAirQualityIndex']['LocalAuthority'][2])



'''
import xml.etree.ElementTree as ET
XML_DIR = ROOT_DIR / "xml_dump"
tree = ET.parse(f"{XML_DIR}/DailyGroup.xml")
root = tree.getroot()
print(root)
print(root[2].attrib)
'''
