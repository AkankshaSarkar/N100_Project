import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import streamlit as st
from utils.db import run_query
st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide"
)
from pathlib import Path

home = st.Page("pages/01_home.py", title="Home", icon="🏠")
profile = st.Page("pages/02_profile.py", title="Profile")
screener = st.Page("pages/03_screener.py", title="Screener")
peers = st.Page("pages/04_peers.py", title="Peers")
trends = st.Page("pages/05_trands.py", title="Trends")
sectors = st.Page("pages/06_sectors.py", title="Sectors")
capital = st.Page("pages/07_capital.py", title="Capital")
reports = st.Page("pages/08_reports.py", title="Reports")

pg = st.navigation(
    [home, profile, screener, peers, trends, sectors, capital, reports]
)

pg.run()