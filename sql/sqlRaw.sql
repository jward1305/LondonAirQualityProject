--Creates table with the data from the latest daily data on file. One local authority to a row. Site field is still a JSON.
CREATE OR REPLACE TABLE DailyDataRaw AS
SELECT
unnest(LocalAuthority, max_depth := 2)
FROM  (SELECT unnest(DailyAirQualityIndex, max_depth := 2) FROM read_json('JSON_FILE'));

--Since Site is a JSON value, we can't just use unnest straight away. We convert any single objects into arrays, then convert the single JSON value into a list of JSON values with from_json. We can then use unnext on this list to get one row per site. The values haven't been extracted into their own fields yet.


-- and use json_extract_string to get the values from the JSONs.

CREATE OR REPLACE TABLE SiteRaw AS
SELECT 
    "@LocalAuthorityCode", 
    unnest(from_json(
        CASE WHEN json_type(Site) = 'OBJECT' THEN json_array(Site) ELSE Site END,
        '["JSON"]'
    )) AS site
    FROM DailyDataRaw
    WHERE Site IS NOT NULL;

