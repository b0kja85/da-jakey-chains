import streamlit as st
import pandas as pd

# UI Imports
import utils.widgets_utils as widget

# Data Cleaning Imports
from utils.data_cleaner import DataCleaner as dc

# Page Configuration
st.set_page_config(
    page_title="VisWalis",
    page_icon="assets/viswalis-favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for DataFrame and uploaded file name
if 'df' not in st.session_state:
    st.session_state.df = None
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = None

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Data Cleaning", "Dashboard", "Report", "Ask AI"])

# Sidebar
st.sidebar.image("assets/viswalis-logo.png")
st.sidebar.subheader("🧹 Brushing Off the Mess, 🌟 Visualizing Success!", anchor=False)
st.sidebar.write("VisWalis simplifies data analysis. Upload a CSV, let us clean it, and explore interactive visualizations.")
st.sidebar.divider()

# File uploader
csv_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# Check if a new file is uploaded
if csv_file:
    # Check if the uploaded file is different from the one in session state
    if st.session_state.uploaded_file_name != csv_file.name:
        # Reset the session state
        st.session_state.df = pd.read_csv(csv_file)
        st.session_state.uploaded_file_name = csv_file.name  # Track the uploaded file name
        alert = f"Loaded new CSV: {csv_file.name}"
else:
    st.warning('Please load a CSV File!', icon="⚠️")

# Main Content
if st.session_state.df is not None:
    with tab1:

        try:
            st.header(f"Data Cleaning: {csv_file.name}")
        except AttributeError:
            st.header("Data Cleaning: No File Loaded!")

        data_table, buttons = st.columns([4, 1])

        # Create a cleaner instance
        cleaner = dc(st.session_state.df)

        with buttons:
            st.write("Data Cleaning Tools")
            # Buttons for cleaning actions
            if st.button("Standardized Columns"):
                placeholder = st.empty()
                st.session_state.df = cleaner.standardize_columns().get_cleaned_data()
                alert = "Standadized Columns!"
                
            if st.button("Drop Empty Values"):
                st.session_state.df = cleaner.handle_missing_values(strategy="drop").get_cleaned_data()
                alert = "Rows with missing values dropped!"

            # Dropdown for selecting columns to drop
            column_to_drop = st.selectbox(
                "Select a column to drop", 
                st.session_state.df.columns.tolist()
            )
            if st.button("Drop Column"):
                try:
                    st.session_state.df = cleaner.drop_column(column_to_drop).get_cleaned_data()
                    alert = f"Column '{column_to_drop}' dropped!"
                except ValueError as e:
                    st.error(str(e))

            

            if st.button("Drop Duplicates"):
                st.session_state.df = cleaner.drop_duplicates().get_cleaned_data()
                alert = "Duplicate rows removed!"

            if st.button("Remove Outliers"):
                st.session_state.df = cleaner.remove_outliers().get_cleaned_data()
                alert = "Outliers removed!"

            if st.button("Auto Clean"):
                st.session_state.df = (
                    cleaner
                    .standardize_columns()
                    .handle_missing_values(strategy="drop")
                    .drop_duplicates()
                    .remove_outliers()
                    .get_cleaned_data()
                )
                alert = "Auto Clean"
            
        with data_table:
            # Display the current state of the DataFrame
            st.dataframe(st.session_state.df)
        try:
            st.success(alert)
        except NameError:
            pass
