from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
JSON_DIR = ROOT_DIR / "json_dump"
LAP_API_URL = "http://api.erg.ic.ac.uk/AirQuality/"
DUCKDB_DIR = ROOT_DIR/"duckdb"/"LAQ.duckdb"
SQL_DIR = ROOT_DIR / "sql"
TEST_DATES = ["2026-11-19", "2026-11-18", "2026-11-17", "2026-11-16", "2026-11-15", "2026-11-14", "2026-11-13"]