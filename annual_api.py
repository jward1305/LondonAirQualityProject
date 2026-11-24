import requests
import json
import duckdb as db
from config import JSON_DIR, LAP_API_URL, DUCKDB_DIR, YEARS

#ANNUAL_API_URL = f"{LAP_API_URL}Annual/MonitoringReport/SiteCode={site_code}/Year={year}/Json"
#Information/MonitoringSites/GroupName=London/Json
def main():
    con = db.connect(str(DUCKDB_DIR))
    sites = con.execute("SELECT SCode FROM SiteStaging").fetchall()
    con.close()
    #for year in YEARS:
    response = requests.get(f"{LAP_API_URL}Information/MonitoringSites/GroupName=London/Json")
    response.raise_for_status()
    results = response.json()
    with open(f"{JSON_DIR}/sites.json", "w") as f:
            json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()