import streamlit as st
import pandas as pd

# Data Cleaning Imports
from utils.data_cleaner import DataCleaner as dc

# Data Visualization
from dashboard import Dashboard

# Report Generation
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components
import io

# AI chatbot func import
from ai import chatbot

# Page Configuration
st.set_page_config(
    page_title="VisWalis",
    page_icon="app/static/viswalis-favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
        menu_items={
        'About': "# 🧹 VisWalis \nby Jakey Chains | PLM BSCS 4-3 (A.Y. 2024-2025 1st Sem)\n\nrepo: https://github.com/b0kja85/da-jakey-chains"
    }
)

# Initialize session state for DataFrame and uploaded file name
if 'df' not in st.session_state:
    st.session_state.df = None
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = None

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Data Cleaning", "Dashboard", "Report", "Ask AI"])

# Sidebar
st.sidebar.image("app/static/viswalis-logo.png")
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
    # Data Cleaning
    with tab1:
        st.header("🧹 Data Cleaning", anchor=False)
        st.write("Prepare and clean your dataset for analysis.")

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
                st.subheader("Standardize Column Names", anchor=False)
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
                st.subheader("Drop Columns", anchor=False)
                column_to_drop = st.selectbox("Select column to drop:", st.session_state.df.columns)
                if st.button("Drop Column"):
                    st.session_state.df = st.session_state.df.drop(columns=[column_to_drop])
                    alert = f"Column '{column_to_drop}' dropped!"

            # Handle Missing Values Section
            with st.expander("Handle Missing Values"):
                st.subheader("Handle Missing Data", anchor=False)
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
                st.subheader("Remove Outliers", anchor=False)
                column_for_outliers = st.selectbox("Select column to check for outliers:", st.session_state.df.select_dtypes(include=[float, int]).columns)
                if st.button("Remove Outliers"):
                    st.session_state.df = cleaner.remove_outliers(columns=[column_for_outliers]).get_cleaned_data()
                    alert = f"Outliers removed from column '{column_for_outliers}'!"

            # Advanced Data Cleaning Section
            with st.expander("Advanced Data Cleaning"):
                st.subheader("Advanced Cleaning Tools", anchor=False)

                # Standardize Dates
                st.subheader("Standardize Dates", anchor=False)
                date_column = st.selectbox("Select column with dates:", st.session_state.df.columns)
                desired_date_format = st.text_input("Enter desired date format (e.g., %Y-%m-%d):", "%Y-%m-%d")
                if st.button("Standardize Dates"):
                    try:
                        st.session_state.df = (
                            cleaner.standardize_dates(column=date_column, date_format=desired_date_format)
                            .get_cleaned_data()
                        )
                        alert = f"Dates in column '{date_column}' standardized to format '{desired_date_format}'!"
                    except Exception as e:
                        alert = f"Error: {str(e)}"
           
                # Clean Symbols
                st.subheader("Clean Symbols", anchor=False)
                symbol_column = st.selectbox("Select column to clean symbols:", st.session_state.df.columns, key="symbol_column")
                unwanted_symbols = st.text_input("Enter symbols to remove (e.g., $,%,&):")
                if st.button("Remove Symbols"):
                    if unwanted_symbols:
                        st.session_state.df = (
                            cleaner.clean_symbols(column=symbol_column, symbols=unwanted_symbols)
                            .get_cleaned_data()
                        )
                        alert = f"Unwanted symbols removed from column '{symbol_column}'!"
                    else:
                        alert = "Please specify symbols to remove."
                    
                # Replace Values
                st.subheader("Replace Values", anchor=False)
                replace_column = st.selectbox("Select column to replace values:", st.session_state.df.columns, key="replace_column")
                value_to_replace = st.text_input("Value to replace:", key="value_to_replace")
                replacement_value = st.text_input("Replace with:", key="replacement_value")
                if st.button("Replace Values"):
                    if value_to_replace:
                        st.session_state.df = (
                            cleaner.replace_values(column=replace_column, to_replace=value_to_replace, replacement=replacement_value)
                            .get_cleaned_data()
                        )
                        alert = f"Replaced '{value_to_replace}' with '{replacement_value}' in column '{replace_column}'!"
                    else:
                        alert = "Please specify a value to replace."

                # Convert to Numeric
                st.subheader("Convert to Numeric", anchor=False)
                numeric_column = st.selectbox("Select column to convert to numeric:", st.session_state.df.columns, key="numeric_column")
                if st.button("Convert to Numeric"):
                    try:
                        st.session_state.df = (
                            cleaner.convert_to_numeric(column=numeric_column)
                            .get_cleaned_data()
                        )
                        alert = f"Column '{numeric_column}' converted to numeric type!"
                    except Exception as e:
                        alert = f"Error: {str(e)}"

        # Success Alert
        try:
            st.success(alert)
        except NameError:
            pass

    # Dashboard
    with tab2:
        st.header("📊 Dashboard", anchor=False)
        st.write("Explore your data through interactive visualizations.")

        df = st.session_state.get('df')  # Set df based on the Session State

        if df is not None:
            # Instantiate the Dashboard class
            dashboard = Dashboard(df)
            
            # Render the dashboard
            dashboard.render()
        else:
            st.warning("Please upload a CSV file to view the dashboard.", icon="⚠️")

    # Report Generation
    with tab3:
        st.header("📋 Report Generation", anchor=False)
        st.write("Generate detailed profiling reports for your dataset.")

        df = st.session_state.get("df")  # Retrieve the DataFrame from Session State

        if df is not None:
            report_title = st.text_input("Enter Title of the Report: ")
            st.markdown("---")
            
            if report_title:    
                profile = ProfileReport(df, title=report_title, explorative=True)
                profile.config.html.navbar_show = False

                try:
                    # Generate the HTML file
                    with st.spinner("Please wait... Generating your Report"):
                        profile_html = profile.to_html()

                    st.subheader(f"{report_title}", anchor=False)
                    # Display the profiling report as HTML
                    components.html(profile_html, height=800, scrolling=True)

                    # Create a downloadable version of the HTML report
                    report_buffer = io.BytesIO(profile_html.encode())  
                    st.download_button(
                        label="Download Report",
                        data=report_buffer,
                        file_name = f"{report_title.lower().strip().replace(' ', '_')}_data_profile_report.html",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"Error generating widgets: {str(e)}")
                    st.warning("Falling back to HTML generation.")
                    st.markdown(profile.to_html(), unsafe_allow_html=True)

        else:
            st.warning("Please upload a CSV file to generate a report.", icon="⚠️")
    
    #AI chatbot
    with tab4:
        chatbot()