import duckdb as db

from api import ROOT_DIR
DUCKDB_DIR = ROOT_DIR/"duckdb"/"LAQ.duckdb"
DUCKDB_DIR.parent.mkdir(parents=True, exist_ok=True)
con = db.connect(str(DUCKDB_DIR))

query = f"SELECT unnest(LocalAuthority, max_depth := 2) FROM (SELECT unnest(DailyAirQualityIndex, max_depth := 2) FROM read_json('{ROOT_DIR}/json_dump/DailyGroup.json'))"
con.sql(query).show()
con.close()