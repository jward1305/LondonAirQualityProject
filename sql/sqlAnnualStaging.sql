
CREATE OR REPLACE TABLE AnnualDataStaged AS
PIVOT (
    SELECT Year, "Site Code",
           r."@SpeciesCode" AS SpCode,
           CAST(r."@Annual" AS INTEGER) AS Days,
           CASE r."@ReportItem" WHEN '3' THEN 'Low'
                                WHEN '4' THEN 'Moderate'
                                WHEN '5' THEN 'High'
                                WHEN '6' THEN 'Very High' END AS Band
    FROM (SELECT Year, "Site Code", unnest(SiteReport.ReportItem) AS r FROM AnnualDataRaw)
    WHERE r."@ReportItem" IN ('3', '4', '5', '6')
) ON Band IN ('Low', 'Moderate', 'High', 'Very High')
  USING first(Days)
GROUP BY Year, "Site Code", SpCode
ORDER BY "Site Code", SpCode;