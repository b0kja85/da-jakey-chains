import streamlit as st
import pandas as pd

#Page Configuration
st.set_page_config(
    page_title="VisWalis",
    page_icon="assets/viswalis-favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.image("assets/viswalis-logo.png")
st.sidebar.subheader("🧹 Brushing Off the Mess, 🌟 Visualizing Success!", anchor=False)
st.sidebar.write("VisWalis simplifies data analysis. Upload a CSV, let us clean it, and explore interactive visualizations.")
st.sidebar.divider()

# File uploader
csv_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# Function to clean data (basic example)
def clean_data(df):
    # Example cleaning steps: drop missing values, remove duplicates
    df_cleaned = df.dropna()  # Drop rows with missing values
    df_cleaned = df_cleaned.drop_duplicates()  # Drop duplicate rows
    # You can add more cleaning logic here (e.g., type conversion, outlier removal, etc.)
    return df_cleaned

# Main content
if csv_file:
    # Read CSV file into DataFrame
    df = pd.read_csv(csv_file)
    
    # Clean the data
    cleaned_df = clean_data(df)
    
    # Display the cleaned data on the main page
    st.write("### Cleaned Data:")
    st.dataframe(cleaned_df)  # Display the cleaned DataFrame as an interactive table
    
    # Allow user to download the cleaned CSV file
    cleaned_csv = cleaned_df.to_csv(index=False)  # Convert cleaned DataFrame to CSV (without index)
    st.download_button(
        label="Download Cleaned CSV",
        data=cleaned_csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )
