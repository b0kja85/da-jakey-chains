import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()
        self.logs = []

    def log_changes(self, action, details):
        self.logs.append({"action": action, "details": details})

    def standardize_columns(self):
        old_columns = self.df.columns.tolist()
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )
        self.log_changes("Standardized Columns", {
            "before": old_columns,
            "after": self.df.columns.tolist()
        })
        return self

    def handle_missing_values(self, strategy="drop", fill_value=None):
        if strategy == "drop":
            affected_rows = self.df[self.df.isnull().any(axis=1)]
            self.log_changes("Dropped Missing Values", affected_rows)
            self.df.dropna(axis=0, how='any', inplace=True)
        elif strategy == "mean":
            missing_cols = self.df.columns[self.df.isnull().any()]
            self.log_changes("Filled Missing Values with Mean", missing_cols.tolist())
            self.df[missing_cols] = self.df[missing_cols].fillna(self.df[missing_cols].mean())
        elif strategy == "median":
            missing_cols = self.df.columns[self.df.isnull().any()]
            self.log_changes("Filled Missing Values with Median", missing_cols.tolist())
            self.df[missing_cols] = self.df[missing_cols].fillna(self.df[missing_cols].median())
        elif strategy == "mode":
            missing_cols = self.df.columns[self.df.isnull().any()]
            self.log_changes("Filled Missing Values with Mode", missing_cols.tolist())
            self.df[missing_cols] = self.df[missing_cols].fillna(self.df[missing_cols].mode().iloc[0])
        elif strategy == "fill":
            if fill_value is not None:
                missing_cols = self.df.columns[self.df.isnull().any()]
                self.log_changes("Filled Missing Values with Custom Value", {
                    "columns": missing_cols.tolist(),
                    "value": fill_value
                })
                self.df[missing_cols] = self.df[missing_cols].fillna(fill_value)
            else:
                raise ValueError("fill_value must be provided when strategy is 'fill'")
        else:
            raise ValueError("Invalid strategy for handling missing values.")
        return self
        
    def drop_column(self, column_name):
        if column_name in self.df.columns:
            self.df.drop(columns=[column_name], inplace=True)
            self.log_changes("Dropped Column", {"column": column_name})
        else:
            raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
        return self
    def drop_duplicates(self):
        duplicates = self.df[self.df.duplicated(keep=False)]
        self.log_changes("Dropped Duplicates", duplicates)
        self.df.drop_duplicates(inplace=True)
        return self

    def remove_outliers(self, columns=None):
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns
        outlier_details = {}
        for col in columns:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.df[
                (self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))
            ]
            outlier_details[col] = outliers
            self.df = self.df.drop(outliers.index)
        self.log_changes("Removed Outliers", outlier_details)
        return self

    def get_logs(self):
        return self.logs

    def get_cleaned_data(self):
        return self.df

    def get_cleaned_data(self):
        """
        Return the cleaned DataFrame.

        Returns:
        pd.DataFrame: The cleaned DataFrame.
        """
        return self.df
