import streamlit as st
from src import data_cleaning_pipeline as dcp

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def convert_df(df):
    return df.to_csv().encode('utf-8')

file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if file:
    file_name = file.name

    df = dcp.load_file_and_checks_feature_name(file_name, file)
    st.dataframe(df)

    if st.button("preprocess the data"):
        df = dcp.check_column_dtypes(df)
        df = dcp.handling_duplicates_nan(df)
        df = dcp.replace_outliers(df)

        csv = convert_df(df)

        st.download_button(
            label="Download CSV file",
            data = csv,
            file_name="west_europe_electricity_data.csv",
            mime = "text/csv"
        )

