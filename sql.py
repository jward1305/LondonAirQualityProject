import duckdb as db
from config import JSON_DIR, DUCKDB_DIR, SQL_DIR

con = db.connect(str(DUCKDB_DIR))
DUCKDB_DIR.parent.mkdir(parents=True, exist_ok=True)
speciesFile = str(JSON_DIR / "Species.json")
adviceFile = str(JSON_DIR / "IndexHealthAdvice.json")
siteFile = str(JSON_DIR / "Sites.json")
LAFile = str(JSON_DIR / "LocalAuthority.json")
dailyFile = str(JSON_DIR / "*_Data.json")

'''
fileRaw = SQL_DIR / "sqlRaw.sql"
sqlRaw = fileRaw.read_text()
sqlRaw = sqlRaw.replace("SPECIES_FILE", speciesFile)
sqlRaw = sqlRaw.replace("ADVICE_FILE", adviceFile)
sqlRaw = sqlRaw.replace("LOCAL_AUTHORITY_FILE", LAFile)
sqlRaw = sqlRaw.replace("SITE_FILE", siteFile)
sqlRaw = sqlRaw.replace("DAILY_DATA_FILE", dailyFile)

con.execute(sqlRaw)

fileStage = SQL_DIR / "sqlStaging.sql"
sqlStage = fileStage.read_text()
con.execute(sqlStage)

#con.sql("SELECT * FROM SiteRaw").show()
#con.sql("SELECT * FROM LocalAuthorityRaw").show()
#con.sql("SELECT * FROM AirQualityBandRaw").show()
#con.sql("SELECT * FROM AdviceRaw").show()
#con.sql("SELECT * FROM SpeciesRaw").show()
con.sql("SELECT * FROM Reading").show()
'''
annualFile = str(JSON_DIR / '*_Site_Data.json')
fileAnnual = SQL_DIR / "sqlAnnualRaw.sql"
sqlAnnual = fileAnnual.read_text()
sqlAnnual = sqlAnnual.replace('ANNUAL_FILE', annualFile)
con.execute(sqlAnnual)

fileTest = SQL_DIR / "sqlAnnualStaging.sql"
sqltest = fileTest.read_text()
con.execute(sqltest)
con.sql("SELECT * FROM AnnualDataStaged").show()
#con.sql("SELECT * FROM MonthlyDataStaged").show()
con.close()