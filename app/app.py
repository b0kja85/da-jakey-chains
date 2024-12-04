import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

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
    if st.session_state.uploaded_file_name != csv_file.name:
        st.session_state.df = pd.read_csv(csv_file)
        st.session_state.uploaded_file_name = csv_file.name
        alert = f"Loaded new CSV: {csv_file.name}"
else:
    st.warning('Please load a CSV File!', icon="⚠️")

# Main Content
if st.session_state.df is not None:
    with tab1:
        st.header("Data Cleaning", anchor=False)

        # Cleaner instance
        cleaner = dc(st.session_state.df)

        # Display the CSV title
        st.subheader(f"Loaded CSV: {st.session_state.uploaded_file_name}", anchor=False)

        # Layout: Two columns (left for DataFrame, right for tools)
        col1, col2 = st.columns([3, 1])

        with col1:
            # Display the current DataFrame
            st.subheader("Current Data", anchor=False)
            st.dataframe(st.session_state.df)

        with col2:
            # Tools Section
            st.subheader("Tools", anchor=False)
            
            btn1, btn2 = st.columns([0.5,0.5])
            with btn1:
                if st.button("Refresh Table"):
                    st.session_state.df = st.session_state.df # Refresh the CSV
                    alert = "Table is Refreshed!"
            with btn2: 

                @st.cache_data
                def convert_df(df):
                    # IMPORTANT: Cache the conversion to prevent computation on every rerun
                    return df.to_csv().encode("utf-8")

                csv = convert_df(st.session_state.df)

                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name= f"{st.session_state.uploaded_file_name}[cleaned_data].csv",
                    mime="text/csv",
                )

            # Edit Columns Section
            with st.expander("Edit Columns"):
                st.subheader("Standardize Column Names")
                # Options for standardizing column names
                standardize_case = st.radio("Select case for column names:", ["lowercase", "uppercase", "sentence case"])
                replace_text = st.text_input("Text to replace in column names:")
                replacement_text = st.text_input("Replace with:")
                if st.button("Apply Standardization"):
                    if standardize_case == "lowercase":
                        st.session_state.df.columns = (
                            st.session_state.df.columns
                            .str.strip()
                            .str.lower()
                            .str.replace(replace_text, replacement_text)
                        )
                    elif standardize_case == "uppercase":
                        st.session_state.df.columns = (
                            st.session_state.df.columns
                            .str.strip()
                            .str.upper()
                            .str.replace(replace_text, replacement_text)
                        )
                    elif standardize_case == "sentence case":
                        st.session_state.df.columns = (
                            st.session_state.df.columns
                            .str.strip()
                            .str.title()
                            .str.replace(replace_text, replacement_text)
                        )
                    alert = "Column names standardized!"

                # Drop Column
                st.subheader("Drop Columns")
                column_to_drop = st.selectbox("Select column to drop:", st.session_state.df.columns)
                if st.button("Drop Column"):
                    st.session_state.df = st.session_state.df.drop(columns=[column_to_drop])
                    alert = f"Column '{column_to_drop}' dropped!"

            # Handle Missing Values Section
            with st.expander("Handle Missing Values"):
                st.subheader("Handle Missing Data")
                strategy = st.radio("Select strategy to handle missing values:", ["drop", "mean", "median", "mode", "fill"])
                if strategy == "fill":
                    fill_value = st.text_input("Value to fill missing data with:")
                    column_to_handle = st.selectbox("Select column to handle:", st.session_state.df.columns)

                if st.button("Apply Missing Value Handling"):
                    if strategy == "drop":
                        st.session_state.df = cleaner.handle_missing_values(strategy="drop").get_cleaned_data()
                    elif strategy == "mean":
                        st.session_state.df = cleaner.handle_missing_values(strategy="mean").get_cleaned_data()
                    elif strategy == "median":
                        st.session_state.df = cleaner.handle_missing_values(strategy="median").get_cleaned_data()
                    elif strategy == "mode":
                        st.session_state.df = cleaner.handle_missing_values(strategy="mode").get_cleaned_data()
                    elif strategy == "fill" and fill_value:
                        st.session_state.df[column_to_handle] = st.session_state.df[column_to_handle].fillna(fill_value)
                    alert = f"Missing values handled using strategy '{strategy}'!"

            # Drop Duplicates Section
            with st.expander("Drop Duplicates"):
                if st.button("Drop Duplicate Rows"):
                    st.session_state.df = cleaner.drop_duplicates().get_cleaned_data()
                    alert = "Duplicate rows removed!"

            # Remove Outliers Section
            with st.expander("Remove Outliers"):
                st.subheader("Remove Outliers")
                column_for_outliers = st.selectbox("Select column to check for outliers:", st.session_state.df.select_dtypes(include=[float, int]).columns)
                if st.button("Remove Outliers"):
                    st.session_state.df = cleaner.remove_outliers(columns=[column_for_outliers]).get_cleaned_data()
                    alert = f"Outliers removed from column '{column_for_outliers}'!"


        # Success Alert
        try:
            st.success(alert)
        except NameError:
            pass

# Dashboard - Visualization
with tab2:
    st.header("Dashboard")
    
    if csv_file:
        # Example Pie Chart
        st.subheader("Pie Chart")
        column_for_pie = st.selectbox("Select a column for the Pie Chart:", st.session_state.df.columns)
        pie_chart = px.pie(st.session_state.df, names=column_for_pie)
        st.plotly_chart(pie_chart)

        # Example Area Plot
        st.subheader("Area Plot")
        numeric_cols = st.session_state.df.select_dtypes(include=['float64', 'int64']).columns
        area_x = st.selectbox("Select X-axis for Area Plot:", numeric_cols)
        area_y = st.multiselect("Select Y-axis for Area Plot:", numeric_cols)
        if area_x and area_y:
            area_plot = px.area(st.session_state.df, x=area_x, y=area_y)
            st.plotly_chart(area_plot)

        # Example Donut Chart
        st.subheader("Donut Chart")
        column_for_donut = st.selectbox("Select a column for the Donut Chart:", st.session_state.df.columns, key="donut")
        donut_chart = px.pie(st.session_state.df, names=column_for_donut, hole=0.4)
        st.plotly_chart(donut_chart)

        # Example Radar Chart
        st.subheader("Radar Chart")
        radar_cols = st.multiselect("Select columns for Radar Chart (numeric only):", numeric_cols)
        if len(radar_cols) > 0:
            radar_data = st.session_state.df[radar_cols].mean().reset_index()
            radar_data.columns = ['Metric', 'Value']
            radar_chart = px.line_polar(radar_data, r='Value', theta='Metric', line_close=True)
            st.plotly_chart(radar_chart)

        # Example Gauge Chart
        st.subheader("Gauge Chart")
        gauge_col = st.selectbox("Select a column for Gauge Chart (numeric only):", numeric_cols, key="gauge")
        if gauge_col:
            gauge_value = st.session_state.df[gauge_col].mean()
            fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=gauge_value,
            title={'text': f"Mean of {gauge_col}"},
            gauge={
            'axis': {'range': [0, st.session_state.df[gauge_col].max()]},
            'bar': {'color': "blue"},
            'steps': [
                {'range': [0, st.session_state.df[gauge_col].max() / 2], 'color': "lightgray"},
                {'range': [st.session_state.df[gauge_col].max() / 2, st.session_state.df[gauge_col].max()], 'color': "gray"}
            ],
        }
    ))
        st.plotly_chart(fig)
    else:
        st.warning('Please upload a CSV File to see visualizations!', icon="⚠️")