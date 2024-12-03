import streamlit as st

# UI Imports
import utils.widgets_utils as widget

#Page Configuration
st.set_page_config(
    page_title="VisWalis",
    page_icon="assets/viswalis-favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Data Cleaning", "Dashboard", "Report", "Ask AI"])

# Sidebar
st.sidebar.image("assets/viswalis-logo.png")
st.sidebar.subheader("🧹 Brushing Off the Mess, 🌟 Visualizing Success!", anchor=False)
st.sidebar.write("VisWalis simplifies data analysis. Upload a CSV, let us clean it, and explore interactive visualizations.")
st.sidebar.divider()

# File uploader
csv_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# Main Content

with tab1:
    st.header("Data Cleaning")
    data_table, buttons = st.columns([4, 1])

    if csv_file:
        df = pd.read_csv(csv_file)
        widget.progress_bar("Processing Data...")
        
        with data_table:
            st.dataframe(df)  

        with buttons:

            st.button("Standardized Columns")
            st.button("Drop Empty Values")
            st.button("Drop Duplicates")
            st.button("Remove Outliers")
            st.button("Auto Clean")

    else:
        st.warning('Please upload a CSV File!', icon="⚠️")
        