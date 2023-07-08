import streamlit as st
from src import data_cleaning_pipeline as dcp
from src.data_cleaning_config import config

custom_config = config()

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

    with st.sidebar:
        required_columns = st.text_input("required columns (as a list)", str(config.required_columns))
        config.required_columns = eval(required_columns)
        columns_dtype = st.text_input("column dtype (as a list)", "['datetime64[ns]', float, float, float, object]")
        config.columns_dtype = eval(columns_dtype)
        nan_value_handler = st.text_input("How to handle nan values (as a dict)",
                                          '{ "demand": "mean","supply": "mean","price" : "drop", "country" : "drop","date" : "drop"}')
        config.nan_value_handler = eval(nan_value_handler)
        outliers_zscore_threshold = st.text_input("outliers_zscore_threshold (as a dict)", '{ "price":4 }')
        config.outliers_zscore_threshold = eval(outliers_zscore_threshold)

    if st.button("preprocess the data"):
        df = dcp.check_column_dtypes(df, config)
        df = dcp.handling_duplicates_nan(df, config)
        df = dcp.replace_outliers(df, config)
        csv = convert_df(df)

        st.download_button(
            label="Download CSV file",
            data = csv,
            file_name="west_europe_electricity_data.csv",
            mime = "text/csv"
        )

