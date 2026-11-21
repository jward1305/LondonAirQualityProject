INSERT OR REPLACE INTO LocalAuthorityStaging
SELECT
    "@LocalAuthorityCode" AS LACode,
    "@LocalAuthorityName" AS LAName,
    "@LaCentreLatitude" AS LACentreLat,
    "@LaCentreLongitude" AS LACentreLong,
FROM DailyDataRaw;

INSERT OR REPLACE INTO SiteStaging
SELECT
    json_extract_string(Site, '$."@SiteCode"') AS SCode,
    "@LocalAuthorityCode" AS LACode,
    json_extract_string(Site, '$."@SiteName"') AS SName,
    json_extract_string(Site, '$."@SiteType"') AS SType,
    json_extract_string(Site, '$."@Latitude"') AS SLat,
    json_extract_string(Site, '$."@Longitude"') AS SLong,
FROM SiteRaw;

INSERT OR REPLACE INTO Species
SELECT DISTINCT
    json_extract_string(sp, '$."@SpeciesCode"') AS SpCode,
    json_extract_string(sp, '$."@SpeciesDescription"') AS SpDescription,
FROM ( SELECT unnest(from_json(
    CASE WHEN json_type(json_extract(site, '$.Species')) = 'OBJECT'
         THEN json_array(json_extract(site, '$.Species'))
         ELSE json_extract(site, '$.Species') END,
    '["JSON"]'
)) AS sp FROM SiteRaw);

--PLACEHOLDER
INSERT OR REPLACE INTO AirQualityBand (AQBand, AQLowerBound, AQUpperBound) VALUES
    ('Low',       1,  3),
    ('Moderate',  4,  6),
    ('High',      7,  9),
    ('Very High', 10, 10);

INSERT OR REPLACE INTO Reading
SELECT DISTINCT ON (SCode, RDate, SpCode)
    SCode,
    CAST(RDate AS DATE) AS RDate,
    json_extract_string(sp, '$."@SpeciesCode"') AS SpCode,
    json_extract_string(sp, '$."@AirQualityBand"') AS AQBand,
    CAST(json_extract_string(sp, '$."@AirQualityIndex"') AS INTEGER) AS AQIndex,
    json_extract_string(sp, '$."@IndexSource"') AS SpSource,
FROM ( SELECT 
    json_extract_string(site, '$."@BulletinDate"') AS RDate,
    json_extract_string(site, '$."@SiteCode"') AS SCode,
    unnest(from_json(
    CASE WHEN json_type(json_extract(site, '$.Species')) = 'OBJECT'
         THEN json_array(json_extract(site, '$.Species'))
         ELSE json_extract(site, '$.Species') END,
    '["JSON"]'
)) AS sp FROM SiteRaw);