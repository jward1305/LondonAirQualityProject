CREATE OR REPLACE TABLE LAStructured AS
SELECT
    CAST(la."@LocalAuthorityCode" AS INTEGER) AS LACode,
    la."@LocalAuthorityName" AS LAName,
    CAST(la."@LaCentreLatitude" AS DOUBLE) AS LACentreLat,
    CAST(la."@LaCentreLongitude" AS DOUBLE) AS LACentreLong,
    YEAR(TRY_STRPTIME(
        NULLIF(la."@DateContractClosed", ''),
        '%d/%m/%Y %H:%M:%S'
    )) AS YearClosed
FROM LocalAuthorityRaw as la;

CREATE OR REPLACE TABLE SiteStructured AS
SELECT
    s."@SiteCode" AS SCode,
    CAST(s."@LocalAuthorityCode" AS INTEGER) AS LACode,
    s."@SiteName" AS SName,
    s."@SiteType" AS SType,
    TRY_CAST(s."@Latitude" AS DOUBLE) AS SLat,
    TRY_CAST(s."@Longitude" AS DOUBLE) AS SLong,
    YEAR(TRY_CAST(NULLIF(s."@DateClosed", '') AS TIMESTAMP)) AS YearClosed
FROM SiteRaw AS s;

CREATE OR REPLACE TABLE Species AS
SELECT 
    sp."@SpeciesCode" AS SpCode, 
    sp."@SpeciesName" AS SpName,
    sp."@Description" AS SpDescription,
    sp."@HealthEffect" AS SpHealthEffect,
FROM SpeciesRaw AS sp;

CREATE OR REPLACE TABLE AirQualityBand AS
SELECT 
    aq."@AirQualityBand" AS AQBand,
    CAST(aq."@LowerAirQualityIndex" AS INTEGER) AS AQLowerBound,
    CAST(aq."@UpperAirQualityIndex" AS INTEGER) AS AQUpperBound
FROM AirQualityBandRaw AS aq;

CREATE OR REPLACE TABLE Advice AS
SELECT
    a."@AirQualityBand" AS AQBand,
    a."@Population" AS TargetPopulation,
    a."@Advice" AS Advice,
FROM AdviceRaw AS a;

-- Helper: normalise a JSON value that may be an object, an array, or missing into an array
CREATE OR REPLACE MACRO as_array(j) AS
    CASE json_type(j)
        WHEN 'ARRAY'  THEN j
        WHEN 'OBJECT' THEN json_array(j)
        ELSE '[]'::JSON
    END;

CREATE OR REPLACE TABLE Reading (
    SCode VARCHAR NOT NULL,
    RDate DATE NOT NULL,
    SpCode VARCHAR NOT NULL,
    AQBand VARCHAR,
    AQIndex INTEGER,
    SpSource VARCHAR,
    PRIMARY KEY (SCode, RDate, SpCode)
);

INSERT OR IGNORE INTO Reading
WITH sites AS (
    SELECT
        CAST(s.value ->> '$."@BulletinDate"' AS DATE) AS RDate,
        s.value ->> '$."@SiteCode"'                   AS SCode,
        s.value -> '$.Species'                        AS SpeciesJson
    FROM DailyDataRaw AS la,
         LATERAL json_each(as_array(la.Site)) AS s
)
SELECT
    sites.SCode,
    sites.RDate,
    sp.value ->> '$."@SpeciesCode"'                        AS SpCode,
    sp.value ->> '$."@AirQualityBand"'                     AS AQBand,
    TRY_CAST(sp.value ->> '$."@AirQualityIndex"' AS INTEGER) AS AQIndex,
    sp.value ->> '$."@IndexSource"'                        AS SpSource
FROM sites,
     LATERAL json_each(as_array(sites.SpeciesJson)) AS sp;


CREATE OR REPLACE TABLE BoroughAirQualitySummary AS
WITH borough_max AS (
    SELECT
        la.LACode,
        la.LAName,
        r.RDate,
        MAX(r.AQIndex) AS MaxAQIndex
    FROM Reading AS r
    JOIN SiteStructured AS s  USING (SCode)
    JOIN LAStructured   AS la USING (LACode)
    WHERE r.AQIndex IS NOT NULL
    GROUP BY la.LACode, la.LAName, r.RDate
    QUALIFY r.RDate = MAX(r.RDate) OVER (PARTITION BY la.LACode)
),
band_index AS (
    SELECT
        AQBand,
        UNNEST(generate_series(AQLowerBound, AQUpperBound)) AS AQIndex
    FROM AirQualityBand
)
SELECT
    m.LACode,
    m.LAName,
    m.RDate,
    m.MaxAQIndex,
    b.AQBand,
    advice.TargetPopulation,
    advice.Advice
FROM borough_max AS m
JOIN band_index AS b      ON m.MaxAQIndex = b.AQIndex
JOIN Advice     AS advice USING (AQBand)
ORDER BY m.LAName, CASE advice.TargetPopulation
    WHEN 'General population' THEN 0
    WHEN 'At-risk individuals' THEN 1
    ELSE 2
END;