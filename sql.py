import duckdb as db

from config import DUCKDB_DIR, JSON_DIR, SQL_DIR, TEST_DATES

def test_data(sqlRaw, sqlTables, sqlStaging):
    testFiles = str(JSON_DIR / "*_Data.json")
    speciesFile = str(JSON_DIR / "Species.json")
    adviceFile = str(JSON_DIR / "IndexHealthAdvice.json")
    con = db.connect(str(DUCKDB_DIR))
    sqlRaw = sqlRaw.replace("JSON_FILE", testFiles)
    sqlRaw = sqlRaw.replace("SPECIES_FILE", speciesFile)
    sqlRaw = sqlRaw.replace("ADVICE_FILE", adviceFile)
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
    speciesFile = str(JSON_DIR / "Species.json")
    adviceFile = str(JSON_DIR / "IndexHealthAdvice.json")
    con = db.connect(str(DUCKDB_DIR))
    sqlRaw = sqlRaw.replace("JSON_FILE", latestFile)
    sqlRaw = sqlRaw.replace("SPECIES_FILE", speciesFile)
    sqlRaw = sqlRaw.replace("ADVICE_FILE", adviceFile)
    con.execute(sqlRaw)
    
    #con.sql("SELECT * FROM DailyDataRaw").show()
    #con.sql("SELECT * FROM SiteRaw").show()
    #con.sql("SELECT * FROM AdviceRaw").show()
    
    con.execute(sqlTables)
    
    con.execute(sqlStaging)
    
    #con.sql("SELECT * FROM LocalAuthorityStaging").show()
    #con.sql("SELECT * FROM SiteStaging").show()
    #con.sql("SELECT * FROM Species").show()
    #con.sql("SELECT * FROM Reading").show()
    #con.sql("SELECT * FROM Species").show()
    #con.sql("SELECT * FROM Advice").show()
    #con.sql("SELECT * FROM AirQualityBand").show()
    
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
