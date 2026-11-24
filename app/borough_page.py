import altair as alt
import streamlit as st
from data import api_name, load_data

st.page_link("map_page.py", label="← Back to map")

borough = st.query_params.get("borough")
if not borough:
    st.warning("No borough selected. Click a borough on the map.")
    st.stop()
st.title(borough)

#sites, readings, species = load_data()
b_name = api_name(borough)
sites, readings, health = load_data(b_name)
#sites_b = sites[sites["LAName"] == api_name(borough)]
if sites.empty:
    st.info("This borough has no monitoring sites.")
    st.stop()
readings_b = readings[readings["SCode"].isin(sites["SCode"])]

# ---- summary ----
c1, c2, c3 = st.columns(3)
c1.metric("Monitoring sites", len(sites))
if readings_b.empty:
    st.info("No readings stored for this borough yet.")
    st.stop()
c2.metric("Latest reading", f"{readings_b['RDate'].max():%d %b %Y}")
c3.metric("Days of data", readings_b["RDate"].nunique())

st.subheader("Borough air quality")
if health.empty:
    st.info("No AQI values are available to calculate a borough maximum.")
else:
    summary = health.iloc[0]
    st.metric("Maximum AQI", f"{summary['MaxAQIndex']}")
    st.caption(f"{summary['AQBand']} band on {summary['RDate']:%d %b %Y}")
    for advice in health.itertuples(index=False):
        st.markdown(f"**{advice.TargetPopulation}:** {advice.Advice}")

# ---- one row per site: latest reading for each pollutant ----
latest_date = readings_b.groupby("SCode")["RDate"].transform("max")
latest = readings_b[readings_b["RDate"] == latest_date].copy()
latest["cell"] = latest["AQIndex"].astype(str) + " (" + latest["AQBand"] + ")"
table = (
    sites.set_index("SCode")[["SName", "SType"]]
    .join(
        latest.groupby("SCode")["RDate"].max()
        .dt.strftime("%Y-%m-%d")
        .rename("Latest"),
        how="inner",
    )
    .join(latest.pivot(index="SCode", columns="SpCode", values="cell"))
    .rename(columns={"SName": "Site", "SType": "Type"})
    .reset_index(drop=True)
    .fillna("-")                       # sites that don't measure a pollutant
)

# ---- trend per site ----
st.subheader("Trend")
pollutants = sorted(readings_b["SpCode"].unique())
pollutant = st.selectbox("Pollutant", pollutants)
one = readings_b[readings_b["SpCode"] == pollutant].merge(sites[["SCode", "SName"]], on="SCode")
st.altair_chart(
    alt.Chart(one).mark_line(point=True).encode(
        x=alt.X("yearmonthdate(RDate):T", title="Date"),
        y=alt.Y("AQIndex:Q", title="Index (1-10)", scale=alt.Scale(zero=False), axis=alt.Axis(tickMinStep=1)),
        color=alt.Color("SName:N", title="Site"),
        tooltip=["SName:N", alt.Tooltip("RDate:T", title="Date"), "AQIndex:Q", "AQBand:N"],
    ).properties(height=320),
)

st.subheader("Sites")
st.dataframe(table, hide_index=True)

#st.map(sites, latitude="latitude", longitude="longitude")