CREATE TABLE IF NOT EXISTS LocalAuthorityStaging (
    LACode INTEGER PRIMARY KEY,
    LAName VARCHAR,
    LACentreLat FLOAT,
    LACentreLong FLOAT,
);

CREATE TABLE IF NOT EXISTS SiteStaging (
    SCode VARCHAR PRIMARY KEY,
    LACode INTEGER,-- REFERENCES LocalAuthorityStaging(LACode),
    SName VARCHAR,
    SType VARCHAR,
    SLat FLOAT,
    SLong FLOAT,
);

CREATE TABLE IF NOT EXISTS Species (
    SpCode VARCHAR PRIMARY KEY,
    SpDescription VARCHAR,
);

CREATE TABLE IF NOT EXISTS AirQualityBand (
    AQBand VARCHAR PRIMARY KEY,
    AQLowerBound INTEGER,
    AQUpperBound INTEGER,
);

CREATE TABLE IF NOT EXISTS Advice (
    AQBand VARCHAR,-- REFERENCES AirQualityBand(AQBand),
    TargetPopulation VARCHAR,
    Advice VARCHAR,
    PRIMARY KEY (AQBand, TargetPopulation),
);

CREATE TABLE IF NOT EXISTS Reading (
    SCode VARCHAR,-- REFERENCES SiteStaging(SCode),
    RDate DATE,
    SpCode VARCHAR,-- REFERENCES Species(SpCode),
    AQBand VARCHAR,-- REFERENCES AirQualityBand(AQBand),
    AQIndex INTEGER,
    SpSource VARCHAR,
    PRIMARY KEY (SCode, RDate, SpCode),
);