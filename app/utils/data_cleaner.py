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
        self.df = df.copy()  # Create a copy of the DataFrame to avoid modifying the original data
        self.logs = []  # Initialize an empty list to store logs of changes made to the DataFrame

    def log_changes(self, action, details):
        """
        Log changes made during data cleaning.

        Parameters:
        action (str): A description of the action performed (e.g., "Dropped Missing Values").
        details (dict): A dictionary with additional details about the action (e.g., affected columns or rows).
        """
        self.logs.append({"action": action, "details": details})

    def standardize_columns(self):
        """
        Standardize column names by stripping leading/trailing spaces, 
        converting to lowercase, and replacing spaces with underscores.
        
        Returns:
        self: The DataCleaner instance to enable method chaining.
        """
        old_columns = self.df.columns.tolist()  # Save the original column names
        self.df.columns = (
            self.df.columns
            .str.strip()  # Remove leading/trailing spaces from column names
            .str.lower()  # Convert column names to lowercase
            .str.replace(" ", "_")  # Replace spaces with underscores in column names
        )
        # Log the change to column names
        self.log_changes("Standardized Columns", {
            "before": old_columns,
            "after": self.df.columns.tolist()
        })
        return self  # Return the instance for method chaining

    def handle_missing_values(self, strategy="drop", fill_value=None):
        """
        Handle missing values in the DataFrame using the specified strategy.

        Parameters:
        strategy (str): The method to handle missing values. Options are:
                        'drop' (drop rows with any missing values),
                        'mean' (fill missing values with the mean of the column),
                        'median' (fill missing values with the median of the column),
                        'mode' (fill missing values with the mode of the column),
                        'fill' (fill missing values with a custom value provided via fill_value).
        fill_value (optional): The custom value to fill missing values when the strategy is 'fill'.

        Returns:
        self: The DataCleaner instance to enable method chaining.
        """
        if strategy == "drop":
            # Drop rows with any missing values
            affected_rows = self.df[self.df.isnull().any(axis=1)]  # Identify rows with missing values
            self.log_changes("Dropped Missing Values", affected_rows)  # Log the dropped rows
            self.df.dropna(axis=0, how='any', inplace=True)  # Drop the rows in place
        elif strategy == "mean":
            # Fill missing values with the mean of the respective columns
            missing_cols = self.df.columns[self.df.isnull().any()]  # Identify columns with missing values
            self.log_changes("Filled Missing Values with Mean", missing_cols.tolist())  # Log the columns affected
            self.df[missing_cols] = self.df[missing_cols].fillna(self.df[missing_cols].mean())  # Fill missing values
        elif strategy == "median":
            # Fill missing values with the median of the respective columns
            missing_cols = self.df.columns[self.df.isnull().any()]
            self.log_changes("Filled Missing Values with Median", missing_cols.tolist())
            self.df[missing_cols] = self.df[missing_cols].fillna(self.df[missing_cols].median())
        elif strategy == "mode":
            # Fill missing values with the mode of the respective columns
            missing_cols = self.df.columns[self.df.isnull().any()]
            self.log_changes("Filled Missing Values with Mode", missing_cols.tolist())
            self.df[missing_cols] = self.df[missing_cols].fillna(self.df[missing_cols].mode().iloc[0])
        elif strategy == "fill":
            # Fill missing values with a custom value
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
            raise ValueError("Invalid strategy for handling missing values.")  # Raise an error for invalid strategy
        return self  # Return the instance for method chaining
        
    def drop_column(self, column_name):
        """
        Drop a column from the DataFrame.

        Parameters:
        column_name (str): The name of the column to drop.

        Returns:
        self: The DataCleaner instance to enable method chaining.
        """
        if column_name in self.df.columns:
            self.df.drop(columns=[column_name], inplace=True)  # Drop the specified column
            self.log_changes("Dropped Column", {"column": column_name})  # Log the action
        else:
            raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")  # Raise an error if the column doesn't exist
        return self  # Return the instance for method chaining

    def drop_duplicates(self):
        """
        Drop duplicate rows from the DataFrame.

        Returns:
        self: The DataCleaner instance to enable method chaining.
        """
        duplicates = self.df[self.df.duplicated(keep=False)]  # Identify duplicate rows
        self.log_changes("Dropped Duplicates", duplicates)  # Log the duplicates
        self.df.drop_duplicates(inplace=True)  # Drop the duplicate rows in place
        return self  # Return the instance for method chaining

    def remove_outliers(self, columns=None):
        """
        Remove outliers from specified columns using the IQR method.

        Parameters:
        columns (list of str, optional): A list of column names to check for outliers. If None, all numeric columns are considered.

        Returns:
        self: The DataCleaner instance to enable method chaining.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns  # Select all numeric columns if none are specified
        outlier_details = {}
        for col in columns:
            Q1 = self.df[col].quantile(0.25)  # Calculate the first quartile (Q1)
            Q3 = self.df[col].quantile(0.75)  # Calculate the third quartile (Q3)
            IQR = Q3 - Q1  # Calculate the interquartile range (IQR)
            outliers = self.df[
                (self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))
            ]  # Identify outliers using the 1.5 * IQR rule
            outlier_details[col] = outliers  # Store the outliers for logging
            self.df = self.df.drop(outliers.index)  # Drop the outliers
        self.log_changes("Removed Outliers", outlier_details)  # Log the removed outliers
        return self  # Return the instance for method chaining

    def get_logs(self):
        """
        Return the log of changes made during the data cleaning process.

        Returns:
        list of dicts: The list of logs detailing each change made to the DataFrame.
        """
        return self.logs

    def get_cleaned_data(self):
        """
        Return the cleaned DataFrame.

        Returns:
        pd.DataFrame: The cleaned DataFrame.
        """
        return self.df