CREATE OR REPLACE TABLE AnnualDataRaw AS
SELECT 
    Year,
    unnest(Sites, max_depth := 2),
FROM read_json('ANNUAL_FILE');