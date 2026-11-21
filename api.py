import requests
import json
from config import JSON_DIR, LAP_API_URL, TEST_DATES

def dated_data_dump(date):
    datedURL = f"{LAP_API_URL}Daily/MonitoringIndex/GroupName=London/Date={date}/Json"
    response = requests.get(datedURL)
    response.raise_for_status()
    results = response.json()
    with open(f"{JSON_DIR}/{date}_Data.json", "w") as f:
        json.dump(results, f, indent=4)
    print(f"Dumped data from {date} to json_dump/{date}_Data.json")
    
def latest_data_dump():
    latestDataURL = f"{LAP_API_URL}Daily/MonitoringIndex/Latest/GroupName=London/Json"
    response = requests.get(latestDataURL)
    response.raise_for_status()
    results = response.json()
    date = results["DailyAirQualityIndex"]["@MonitoringIndexDate"].split()[0]
    with open(f"{JSON_DIR}/DailyGroup.json", "w") as f:
        json.dump(results, f, indent=4)
    print(f"Dumped latest daily data to json_dump/DailyGroup.json")
    dated_data_dump(date)
    
def main():
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    for date in TEST_DATES:
        dated_data_dump(date)
    latest_data_dump()
    print("Data dump complete.")
    
if __name__ == "__main__":
    main()

'''import requests
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
XML_DIR = ROOT_DIR / "xml_dump"
LAP_API_URL = "http://api.erg.ic.ac.uk/AirQuality/"

XML_DIR.mkdir(parents=True, exist_ok=True)
healthAdviceURL = f"{LAP_API_URL}Information/IndexHealthAdvice"
speciesURL = f"{LAP_API_URL}Information/Species"

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