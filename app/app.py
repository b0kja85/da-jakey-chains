import streamlit as st

# Page Setup 
home = st.Page(
    page="home.py",
    default=True
)

# Page Navigation
pg = st.navigation(pages=[home])
pg.run()
