import pandas as pd
import numpy as np

class DataCleaner:
    """
    A utility class for cleaning and preprocessing data in a Pandas DataFrame.
    """

    def __init__(self, df):
        """
        Initialize the DataCleaner with a Pandas DataFrame.

        Parameters:
        df (pd.DataFrame): The DataFrame to clean.
        """
        self.df = df.copy()  # Create a copy to avoid modifying the original DataFrame
        self.logs = []  # Initialize logs for tracking changes

    def log_changes(self, action, details):
        """
        Log changes made during data cleaning.

        Parameters:
        action (str): Description of the action performed.
        details (dict): Additional details about the change (e.g., affected rows or columns).
        """
        self.logs.append({"action": action, "details": details})

    def standardize_columns(self):
        """
        Standardize column names by stripping spaces, converting to lowercase, 
        and replacing spaces with underscores.

        Returns:
        self: The DataCleaner instance to enable method chaining.
        """
        old_columns = self.df.columns.tolist()
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
        )
        self.log_changes("Standardized Column Names", {
            "before": old_columns,
            "after": self.df.columns.tolist()
        })
        return self

    def handle_missing_values(self, strategy="drop", fill_value=None):
        """
        Handle missing values in the DataFrame.

        Parameters:
        strategy (str): Strategy for handling missing values.
        fill_value: Value to fill when strategy is 'fill'.

        Returns:
        self: The DataCleaner instance to enable method chaining.
        """
        if strategy == "drop":
            affected_rows = self.df[self.df.isnull().any(axis=1)]
            self.df.dropna(inplace=True)
            self.log_changes("Dropped Missing Values", {"affected_rows": len(affected_rows)})
        elif strategy in ["mean", "median", "mode"]:
            missing_cols = self.df.columns[self.df.isnull().any()]
            fill_func = {"mean": self.df.mean, "median": self.df.median, "mode": lambda: self.df.mode().iloc[0]}[strategy]
            self.df[missing_cols] = self.df[missing_cols].fillna(fill_func())
            self.log_changes(f"Filled Missing Values with {strategy.capitalize()}", {"columns": missing_cols.tolist()})
        elif strategy == "fill" and fill_value is not None:
            missing_cols = self.df.columns[self.df.isnull().any()]
            self.df[missing_cols] = self.df[missing_cols].fillna(fill_value)
            self.log_changes("Filled Missing Values with Custom Value", {"value": fill_value})
        else:
            raise ValueError("Invalid strategy for handling missing values.")
        return self

    def standardize_dates(self, column, date_format="%Y-%m-%d"):
        """
        Standardize dates in a specified column to a uniform format.

        Parameters:
        column (str): Column name containing dates.
        date_format (str): Desired date format (default: "%Y-%m-%d").

        Returns:
        self: The DataCleaner instance to enable method chaining.
        """
        if column in self.df.columns:
            original_values = self.df[column].dropna().tolist()
            self.df[column] = pd.to_datetime(self.df[column], errors="coerce").dt.strftime(date_format)
            self.log_changes("Standardized Dates", {"column": column, "original_values": original_values})
        else:
            raise ValueError(f"Column '{column}' does not exist.")
        return self

    def clean_symbols(self, column, symbols):
        """
        Remove unnecessary symbols from values in a specified column.

        Parameters:
        column (str): Column name to clean.
        symbols (str): String of symbols to remove.

        Returns:
        self: The DataCleaner instance to enable method chaining.
        """
        if column in self.df.columns:
            original_values = self.df[column].tolist()
            self.df[column] = self.df[column].replace(f"[{symbols}]", "", regex=True)
            self.log_changes("Cleaned Symbols", {"column": column, "symbols": symbols, "original_values": original_values})
        else:
            raise ValueError(f"Column '{column}' does not exist.")
        return self

    def convert_to_numeric(self, column):
        """
        Convert string representations of numbers to numeric values.

        Parameters:
        column (str): Column name to convert.

        Returns:
        self: The DataCleaner instance to enable method chaining.
        """
        if column in self.df.columns:
            original_values = self.df[column].tolist()
            self.df[column] = pd.to_numeric(self.df[column], errors="coerce")
            self.log_changes("Converted to Numeric", {"column": column, "original_values": original_values})
        else:
            raise ValueError(f"Column '{column}' does not exist.")
        return self

    def drop_duplicates(self):
        """
        Drop duplicate rows from the DataFrame.

        Returns:
        self: The DataCleaner instance to enable method chaining.
        """
        duplicates = self.df[self.df.duplicated()]
        self.df.drop_duplicates(inplace=True)
        self.log_changes("Dropped Duplicates", {"duplicates_removed": len(duplicates)})
        return self

    def remove_outliers(self, columns=None):
        """
        Remove outliers using the IQR method.

        Parameters:
        columns (list): Columns to check for outliers (default: all numeric columns).

        Returns:
        self: The DataCleaner instance to enable method chaining.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns
        outlier_info = {}
        for col in columns:
            Q1, Q3 = self.df[col].quantile([0.25, 0.75])
            IQR = Q3 - Q1
            outliers = self.df[(self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))]
            self.df.drop(outliers.index, inplace=True)
            outlier_info[col] = len(outliers)
        self.log_changes("Removed Outliers", outlier_info)
        return self
    
    def normalize_case(self, column, case_type="lowercase"):
        """
        Normalize the case of text data in a specified column.
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame.")
        
        if case_type == "lowercase":
            self.df[column] = self.df[column].str.lower()
        elif case_type == "uppercase":
            self.df[column] = self.df[column].str.upper()
        elif case_type == "titlecase":
            self.df[column] = self.df[column].str.title()
        return self

    def replace_values(self, column, to_replace, replacement):
        """
        Replace specific values in a column.
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame.")
        
        self.df[column] = self.df[column].str.replace(to_replace, replacement, regex=False)
        return self

    def get_logs(self):
        """
        Return a log of changes.

        Returns:
        list: Logs of changes made during cleaning.
        """
        return self.logs

    def get_cleaned_data(self):
        """
        Return the cleaned DataFrame.

        Returns:
        pd.DataFrame: The cleaned DataFrame.
        """
        return self.df
