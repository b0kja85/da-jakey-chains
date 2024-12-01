import streamlit as st

# Set the title and layout of the page
st.set_page_config(page_title="VisWalis", page_icon="assets/viswalis-favicon.png")

with st.container():
    
    st.image("assets/viswalis-logo.png", width=1000, use_container_width=True) 
    st.subheader("🧹 Brushing Off the Mess, 🌟 Visualizing Sucess!", anchor=False)

    # Short Description
    st.write("VisWalis is an intuitive web app that streamlines data analysis. Simply upload your CSV, let it clean the data, and generate insightful visualizations and reports effortlessly!")
    st.divider()

    # Add a file uploader below the icon
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
