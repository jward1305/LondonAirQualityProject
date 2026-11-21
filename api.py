import requests
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
JSON_DIR = ROOT_DIR / "json_dump"
LAP_API_URL = "http://api.erg.ic.ac.uk/AirQuality/"

JSON_DIR.mkdir(parents=True, exist_ok=True)
healthAdviceURL = f"{LAP_API_URL}Daily/MonitoringIndex/Latest/GroupName=London/Json"

response = requests.get(healthAdviceURL)
response.raise_for_status()
results = response.json()
date = results["DailyAirQualityIndex"][0]["@MonitoringIndexDate"]


with open(f"{JSON_DIR}/DailyGroup.json", "w") as f:
    json.dump(results, f, indent=4)
    
print(f"Dumped daily data to json_dump/DailyGroup.json")


with open(f"{JSON_DIR}/{date}.json", "w") as f:
    json.dump(results, f, indent=4)

print(f"Dumped data from {date} to json_dump/{date}.json")


'''import requests
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
XML_DIR = ROOT_DIR / "xml_dump"
LAP_API_URL = "http://api.erg.ic.ac.uk/AirQuality/"

XML_DIR.mkdir(parents=True, exist_ok=True)
healthAdviceURL = f"{LAP_API_URL}Information/IndexHealthAdvice"

response = requests.get(healthAdviceURL)
response.raise_for_status()
#tree = ET.fromstring(response.content)
f =  open(f"{XML_DIR}/IndexHealthAdvice.xml", "wb")
f.write(response.content)
f.close()

import requests
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
XML_DIR = ROOT_DIR / "xml_dump"
LAP_API_URL = "http://api.erg.ic.ac.uk/AirQuality/"

XML_DIR.mkdir(parents=True, exist_ok=True)
#healthAdviceURL = f"{LAP_API_URL}Information/IndexHealthAdvice"
dailyDataURL = f"{LAP_API_URL}Daily/MonitoringIndex/Latest/GroupName=London"

response = requests.get(dailyDataURL)
response.raise_for_status()
#tree = ET.fromstring(response.content)
#f =  open(f"{XML_DIR}/IndexHealthAdvice.xml", "wb")
f =  open(f"{XML_DIR}/DailyGroup.xml", "wb")
f.write(response.content)
f.close()'''