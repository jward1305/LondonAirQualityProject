import requests
import json
import duckdb as db
from config import JSON_DIR, LAP_API_URL, DUCKDB_DIR, YEARS


#Information/MonitoringSites/GroupName=London/Json
def main():
    con = db.connect(str(DUCKDB_DIR))
    for year in YEARS:
        year_json = {"Year": year, "Sites": []}
        sites = con.execute(f"SELECT SCode FROM SiteStructured WHERE YearClosed IS NULL OR YearClosed >= ?", [year]).fetchall()
        for site in sites:
            site_code = site[0]
            response = requests.get(f"{LAP_API_URL}Annual/MonitoringReport/SiteCode={site_code}/Year={year}/Json")
            response.raise_for_status()
            results = response.json()
            if results.get("SiteReport"):
                year_json["Sites"].append({"Site Code": site_code, **results})
                print(f"Appended {site_code}")
        with open(f"{JSON_DIR}/{year}_Site_Data.json", "w") as f:
                json.dump(year_json, f, indent=4)
        print(f"Dumped {year} data in {year}_Site_Data.json")
    con.close()

if __name__ == "__main__":
    main()