import duckdb as db

from config import DUCKDB_DIR, JSON_DIR, SQL_DIR, TEST_DATES

def test_data(sqlRaw, sqlTables, sqlStaging):
    latestFile = str(JSON_DIR / "*_Data.json")
    con = db.connect(str(DUCKDB_DIR))
    sqlRaw = sqlRaw.replace("JSON_FILE", latestFile)
    con.execute(sqlRaw)
    
    #con.sql("SELECT * FROM DailyDataRaw").show()
    
    con.execute(sqlTables)
    
    con.execute(sqlStaging)
    
    #con.sql("SELECT * FROM LocalAuthorityStaging").show()
    #con.sql("SELECT * FROM SiteStaging").show()
    #con.sql("SELECT * FROM Species").show()
    #con.sql("SELECT * FROM Reading").show()
    
    con.close()
    print("Test data stored successfully.")
    
def latest_data(sqlRaw, sqlTables, sqlStaging):
    latestFile = str(JSON_DIR / "DailyGroup.json")
    con = db.connect(str(DUCKDB_DIR))
    sqlRaw = sqlRaw.replace("JSON_FILE", latestFile)
    con.execute(sqlRaw)
    
    #con.sql("SELECT * FROM DailyDataRaw").show()
    #con.sql("SELECT * FROM SiteRaw").show()
    #con.sql("SELECT * FROM SpeciesRaw").show()
    
    con.execute(sqlTables)
    
    con.execute(sqlStaging)
    
    #con.sql("SELECT * FROM LocalAuthorityStaging").show()
    #con.sql("SELECT * FROM SiteStaging").show()
    #con.sql("SELECT * FROM Species").show()
    #con.sql("SELECT * FROM Reading").show()
    
    con.close()
    print("Latest data stored successfully.")
    

def main():
    DUCKDB_DIR.parent.mkdir(parents=True, exist_ok=True)
    

    fileRaw = SQL_DIR / "sqlRaw.sql"
    sqlRaw = fileRaw.read_text()

    fileTables = SQL_DIR / "sqlTables.sql"
    sqlTables = fileTables.read_text()    
    
    fileStaging = SQL_DIR / "sqlStaging.sql"
    sqlStaging = fileStaging.read_text()
    
    test_data(sqlRaw, sqlTables, sqlStaging)
    latest_data(sqlRaw, sqlTables, sqlStaging)
    

    
    
if __name__ == "__main__":
    main()
