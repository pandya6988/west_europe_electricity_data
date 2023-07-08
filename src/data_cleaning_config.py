from dataclasses import dataclass

@dataclass
class config:
    required_columns  = ["date"          ,"demand", "supply", "price", "country"]
    columns_dtype     = ["datetime64[ns]", float  , float   , float  ,  object  ]
    nan_value_handler = { "demand": "mean",
                          "supply": "mean",
                          "price" : "drop",
                          "country" : "drop",
                          "date" : "drop"
                          }
    outliers_zscore_threshold = { "price":4 }