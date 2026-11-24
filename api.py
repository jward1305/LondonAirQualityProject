import requests
import json
from config import JSON_DIR, LAP_API_URL, XML_DIR, TEST_DATES
import xmltodict

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
    with open(f"{JSON_DIR}/{date}_Data.json", "w") as f:
            json.dump(results, f, indent=4)
    print(f"Dumped latest daily data to json_dump/{date}_Data.json")

def xml_data_dump():
    healthAdviceURL = f"{LAP_API_URL}Information/IndexHealthAdvice"
    speciesURL = f"{LAP_API_URL}Information/Species"
    
    response = requests.get(healthAdviceURL)
    response.raise_for_status()
    with open(f"{XML_DIR}/IndexHealthAdvice.xml", "wb") as f:
        f.write(response.content)
    print(f"Dumped Index Health Advice data to xml_dump/IndexHealthAdvice.xml")
    conversiondata = xmltodict.parse(response.content, force_list={"AirQualityBanding", "HealthAdvice"})
    with open(f"{JSON_DIR}/IndexHealthAdvice.json", "w") as f:
            json.dump(conversiondata, f, indent=4)
    print(f"Converted Index Health Advice data to json_dump/IndexHealthAdvice.json")
    
    response = requests.get(speciesURL)
    response.raise_for_status()
    with open(f"{XML_DIR}/Species.xml", "wb") as f:
        f.write(response.content)
    print(f"Dumped Species data to xml_dump/Species.xml")
    conversiondata = xmltodict.parse(response.content, force_list={"Species"})
    with open(f"{JSON_DIR}/Species.json", "w") as f:
        json.dump(conversiondata, f, indent=4)
    print(f"Converted Species data to json_dump/Species.json")

def site_dump():
    sitesURL = "Information/MonitoringSites/GroupName=London/Json"
    response = requests.get(f"{LAP_API_URL}{sitesURL}")
    response.raise_for_status()
    results = response.json()
    with open(f"{JSON_DIR}/Sites.json", "w") as f:
            json.dump(results, f, indent=4)
    print(f"Dumped latest daily data to json_dump/Sites.json")

def local_authority_dump():
    localAuthorityURL = "Information/MonitoringLocalAuthority/GroupName=London/Json"
    response = requests.get(f"{LAP_API_URL}{localAuthorityURL}")
    response.raise_for_status()
    results = response.json()
    with open(f"{JSON_DIR}/LocalAuthority.json", "w") as f:
            json.dump(results, f, indent=4)
    print(f"Dumped latest daily data to json_dump/LocalAuthority.json")

def main():
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    XML_DIR.mkdir(parents=True, exist_ok=True)
    #monitoringSitesURL = f"{LAP_API_URL}Information/MonitoringSites/GroupName=London"
    for date in TEST_DATES:
        dated_data_dump(date)
    latest_data_dump()
    xml_data_dump()
    local_authority_dump()
    site_dump()
    print("Data dump complete.")
    
if __name__ == "__main__":
    main()