CREATE OR REPLACE TABLE SiteRaw AS
    SELECT 
        unnest(Site, max_depth := 2) 
    FROM (SELECT unnest(Sites, max_depth := 2) FROM read_json('SITE_FILE'));

CREATE OR REPLACE TABLE LocalAuthorityRaw AS
    SELECT 
        unnest(LocalAuthority, max_depth := 2) 
    FROM (SELECT unnest(LocalAuthorities, max_depth := 2) FROM read_json('LOCAL_AUTHORITY_FILE'));

CREATE OR REPLACE TABLE SpeciesRaw AS
SELECT
    unnest(AirQualitySpecies.Species, max_depth := 2),
FROM read_json('SPECIES_FILE');

CREATE OR REPLACE TABLE AdviceRaw AS
SELECT
    "@AirQualityBand",
    unnest(HealthAdvice, max_depth := 2),
FROM (SELECT unnest(AirQualityIndexHealthAdvice.AirQualityBanding, max_depth := 2) FROM read_json('ADVICE_FILE'));

CREATE OR REPLACE TABLE AirQualityBandRaw AS
SELECT
    unnest(AirQualityIndexHealthAdvice.AirQualityBanding, max_depth := 2),
FROM read_json('ADVICE_FILE');

CREATE OR REPLACE TABLE DailyDataRaw AS
SELECT
    unnest(LocalAuthority, max_depth := 2),
FROM  (SELECT unnest(DailyAirQualityIndex, max_depth := 2) FROM read_json('DAILY_DATA_FILE'));