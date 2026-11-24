import duckdb
import pandas as pd
import streamlit as st
from config import DUCKDB_DIR

# Boundary-file (ONS) names that differ from the air quality API's names
ONS_TO_API = {"Kingston upon Thames": "Kingston", "Richmond upon Thames": "Richmond"}


def api_name(ons_name):
    return ONS_TO_API.get(ons_name, ons_name)


@st.cache_data(ttl=600)
def load_data(b_name):
    con = duckdb.connect(str(DUCKDB_DIR), read_only=True)   # read-only: never blocks the pipeline
    try:
        sites = con.sql("""
            SELECT s.SCode, s.SName, s.SType, la.LAName,
                   s.SLat AS latitude, s.SLong AS longitude
            FROM SiteStructured AS s
            LEFT JOIN LAStructured AS la USING (LACode)
            WHERE s.SLat IS NOT NULL AND s.SLong IS NOT NULL
            AND la.LAName = ?
        """, params=[b_name]).df()
        readings = con.sql("""
            SELECT SCode, RDate, SpCode, CAST(AQIndex AS INTEGER) AS AQIndex, AQBand
            FROM Reading
        """).df()
        health = con.sql("""
            SELECT
                RDate,
                MaxAQIndex,
                AQBand,
                TargetPopulation,
                Advice
            FROM BoroughAirQualitySummary
            WHERE LAName = ?
            ORDER BY CASE TargetPopulation
                WHEN 'General population' THEN 0
                WHEN 'At-risk individuals' THEN 1
                ELSE 2
            END
        """, params=[b_name]).df()
        #species = con.sql("SELECT SpCode, SpName FROM Species").df()
    finally:
        con.close()
    readings["RDate"] = pd.to_datetime(readings["RDate"])
    return sites, readings, health