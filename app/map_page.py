import json
from pathlib import Path

import duckdb
import pydeck as pdk
import streamlit as st

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import DUCKDB_DIR
from data import api_name

BOUNDARY_FILE = Path(__file__).resolve().parent / "london_boroughs.geojson"
BAND_COLORS = {
    "Low": [46, 158, 79, 150],
    "Moderate": [242, 169, 0, 150],
    "High": [215, 48, 31, 150],
    "Very High": [106, 61, 154, 150],
}
NO_DATA_COLOR = [128, 128, 128, 150]

#st.set_page_config(page_title="London air quality", layout="wide")
st.title("London air quality monitoring sites")


@st.cache_data
def load_sites():
    con = duckdb.connect(str(DUCKDB_DIR), read_only=True)
    try:
        return con.sql("""
            SELECT DISTINCT s.SCode, s.SName, s.SType, s.SLat AS latitude, s.SLong AS longitude
            FROM SiteStructured AS s
            INNER JOIN Reading AS r USING (SCode)
            WHERE s.SLat IS NOT NULL AND s.SLong IS NOT NULL
        """).df()
    finally:
        con.close()


@st.cache_data
def load_boundaries():
    return json.loads(BOUNDARY_FILE.read_text())


@st.cache_data(ttl=600)
def load_borough_maxima():
    con = duckdb.connect(str(DUCKDB_DIR), read_only=True)
    try:
        return con.sql("""
            SELECT LAName, RDate, MaxAQIndex, AQBand
            FROM BoroughAirQualitySummary
            WHERE TargetPopulation = 'General population'
        """).df()
    finally:
        con.close()


sites = load_sites()
boundary_data = load_boundaries()
maxima = {
    row.LAName: row
    for row in load_borough_maxima().itertuples(index=False)
}
features = []
for feature in boundary_data["features"]:
    properties = dict(feature["properties"])
    maximum = maxima.get(api_name(properties["name"]))
    properties["max_aqi"] = (
        f"{maximum.MaxAQIndex} ({maximum.RDate:%d %b %Y})"
        if maximum is not None
        else "No data"
    )
    properties["fill_color"] = (
        BAND_COLORS.get(maximum.AQBand, NO_DATA_COLOR)
        if maximum is not None
        else NO_DATA_COLOR
    )
    features.append({**feature, "properties": properties})

boundaries = {
    **boundary_data,
    "features": features,
}

layers = [
    pdk.Layer(
        "GeoJsonLayer", boundaries, id="boroughs",
        stroked=True, filled=True, pickable=True,
        get_fill_color="properties.fill_color",
        get_line_color=[20, 80, 160, 255],       # darker outline
        line_width_min_pixels=1,
    ),
    pdk.Layer(
        "ScatterplotLayer", sites,
        get_position="[longitude, latitude]",
        get_fill_color=[220, 60, 40, 220],
        get_radius=200, radius_min_pixels=4,
    ),
]

event = st.pydeck_chart(
    pdk.Deck(
        layers=layers,
        initial_view_state=pdk.ViewState(latitude=51.5, longitude=-0.12, zoom=9.2),
        tooltip={"text": "{name}\nMaximum AQI: {max_aqi}"},
    ),
    on_select="rerun", selection_mode="single-object", key="map",
)

# Clicking a borough opens the borough page, passing its name in the URL
picked = event.selection.get("indices", {}).get("boroughs", [])
if picked:
    name = boundaries["features"][picked[0]]["properties"]["name"]
    st.switch_page("borough_page.py", query_params={"borough": name})
st.caption(f"{len(boundaries['features'])} boroughs, {len(sites)} active monitoring sites")
st.caption(
    "Source: Office for National Statistics licensed under the Open Government "
    "Licence v.3.0. Contains OS data © Crown copyright and database right 2025."
)