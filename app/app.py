import json
from pathlib import Path

import duckdb
import pydeck as pdk
import streamlit as st

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import DUCKDB_DIR

BOUNDARY_FILE = Path(__file__).resolve().parent / "london_boroughs.geojson"

st.set_page_config(page_title="London air quality", layout="wide")
st.title("London air quality monitoring sites")


@st.cache_data
def load_sites():
    con = duckdb.connect(str(DUCKDB_DIR), read_only=True)
    try:
        return con.sql("""
            SELECT SCode, SName, SType, SLat AS latitude, SLong AS longitude
            FROM SiteStaging
            WHERE SLat IS NOT NULL AND SLong IS NOT NULL
        """).df()
    finally:
        con.close()


@st.cache_data
def load_boundaries():
    return json.loads(BOUNDARY_FILE.read_text())


sites = load_sites()
boundaries = load_boundaries()

layers = [
    pdk.Layer(
        "GeoJsonLayer", boundaries,
        stroked=True, filled=True, pickable=True,
        get_fill_color=[30, 120, 200, 40],       # translucent blue fill
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

st.pydeck_chart(pdk.Deck(
    layers=layers,
    initial_view_state=pdk.ViewState(latitude=51.5, longitude=-0.12, zoom=9.2),
    tooltip={"text": "{name}"},       # borough name on hover
))
st.caption(f"{len(boundaries['features'])} boroughs, {len(sites)} monitoring sites")
st.caption(
    "Source: Office for National Statistics licensed under the Open Government "
    "Licence v.3.0. Contains OS data © Crown copyright and database right 2025."
)