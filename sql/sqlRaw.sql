--Creates table with the data from the latest daily data on file. One local authority to a row. Site field is still a structure.
CREATE OR REPLACE TABLE DailyDataRaw AS
SELECT
unnest(LocalAuthority, max_depth := 2)
FROM  (SELECT unnest(DailyAirQualityIndex, max_depth := 2) FROM read_json('{ROOT_DIR}/json_dump/DailyGroup.json'));