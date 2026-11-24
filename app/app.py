import streamlit as st

st.set_page_config(page_title="London air quality", layout="wide")

pages = [
    st.Page("map_page.py", title="Map", default=True),
    st.Page("borough_page.py", title="Borough", url_path="borough"),
]
st.navigation(pages, position="hidden").run()