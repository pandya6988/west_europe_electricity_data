# west_europe_electricity_data

This is the streamlit app. 

It performs following preprocessing tasks. 

1. Checks the required features in the file. (Only takes csv or excel file as an input)
2. Remove duplicate rows.
3. Handle `NaN`values in the column. (according config file)
4. Handle outliers. We are not removing the outliers but replacing the value 
with previous non-outlier values.

[click here](https://westeuropeelectricitydata-ufrq45d1ase.streamlit.app/) for streamlit app.