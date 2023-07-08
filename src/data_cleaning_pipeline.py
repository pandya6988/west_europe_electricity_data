import numpy as np
import pandas as pd
import os
from dataclasses import dataclass
from ensure import ensure_annotations
from .logger import logger
from scipy.stats import zscore
from .data_cleaning_config import config

@ensure_annotations
def load_file_and_checks_feature_name(file_name:str, file, config=config):
    """
    Loads a .csv or .xls file, performs validity checks, and returns dataframe with required columns.

    Parameters:
    ----------
    file_name (str): Name of the file.
    file (csv/excel): File

    Returns:
    ----------
    DataFrame: Pandas DataFrame containing required columns as specified in config.
    """
    # assert file_name.endswith(".csv") or file_name.endswith(".xls"), logger.error("Wrong file extention.")

    # assert os.path.exists(file_name), logger.error("File does not exists.")

    # assert os.path.getsize("file_name") > 0, logger.error("Empty file detected.")

    if file_name.endswith(".csv"): df = pd.read_csv(file)
    if file_name.endswith(".xls"): df = pd.read_excel(file)
    logger.info("File loaded.")

    df = df.rename(columns=str.lower) # converting all column names to lower case.
    assert df.columns.all() in config.required_columns, logger.info("All required columns does not exist in the file.")
    logger.info("All required columns exists in the file.")

    return df[config.required_columns]

@ensure_annotations
def check_column_dtypes(df:pd.DataFrame, config=config):
    """
    Checks and converts the datatypes of DataFrame columns to specified types.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame whose columns' data types are to be checked and possibly converted.

    Returns
    -------
    pd.DataFrame
        The DataFrame with columns possibly converted to the specified data types.
    """

    for col, dtype in zip( config.required_columns, config.columns_dtype):
        if df[col].dtype != dtype:
            try:
                df[col] = df[col].astype(dtype)
            except:
                logger.error(f"Could not convert column {col} to {dtype}")

        logger.info("Features are converted to correct format.")
        return df

@ensure_annotations
def handle_nan(df:pd.DataFrame, col:str, method:str):
    if method == "drop":
        df.dropna(subset=[col], inplace=True)
        df.reset_index(drop=True, inplace=True)
    elif method == "mean":
        df[col].fillna( df[col].mean(), inplace=True )
    elif method == "zero":
        df[col].fillna( 0, inplace=True )
    elif method == "median":
        df[col].fillna( df[col].median(), inplace=True )

    return df

@ensure_annotations
def handling_duplicates_nan(df:pd.DataFrame, config=config):
    """
    Removes duplicates and handles missing values in a DataFrame based on the specified configuration.

    Parameters
    ----------
        df (pd.DataFrame): The input DataFrame.

    Returns
    -------
        pd.DataFrame: The processed DataFrame with duplicates and NaNs handled.
    """

    df_len = len(df)
    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Handling missing value
    for col, nan_handler in config.nan_value_handler.items():
        df = handle_nan(df, col, nan_handler)

    df_new_len = len(df)
    logger.info(f"{100-round((df_new_len/df_len), 4)*100}% of the data removed.")

    return df

@ensure_annotations
def replace_outliers(df:pd.DataFrame, config=config):
    """
    Replaces outliers in a DataFrame with the last valid (non-outlier) value.

    The function uses a z-score method, treating values above a threshold as outliers.
    This threshold is specified for each column in the `config.outliers_zscore_threshold` dictionary.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame on which outlier replacement is performed.

    Returns
    -------
    df : pd.DataFrame
        DataFrame after outlier replacement.
    """

    for col, threshold in config.outliers_zscore_threshold.items():
        count = 0
        z_scores = zscore(df[col].to_numpy())
        last_valid = None
        for idx, value in enumerate(df[col]):
            if np.abs(z_scores[idx]) > threshold:
                if last_valid is not None:
                    df.loc[idx, col] = last_valid
                    count += 1
            else:
                last_valid = value
        logger.info(f"{count} values are modified.")

    return df