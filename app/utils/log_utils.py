import pandas as pd

class LogsUtils:
    """
    A utility class to display and summarize the logs generated during data cleaning.
    """

    def __init__(self, logs):
        """
        Initialize LogDisplay with logs from DataCleaner.

        Parameters:
        logs (list): The list of logs generated during data cleaning.
        """
        self.logs = logs

    def display_logs(self):
        """
        Display all logs in a human-readable format.

        Returns:
        str: Formatted log string.
        """
        if not self.logs:
            return "No actions were performed."

        log_output = ["Data Cleaning Summary:"]
        
        for log in self.logs:
            action = log["action"]
            details = log["details"]
            log_output.append(f"\n- Action: {action}")
            log_output.append(f"  Affected: {self.format_details(details)}")
        
        return "\n".join(log_output)

    def format_details(self, details):
        """
        Format the details for each log entry.

        Parameters:
        details (any): The details related to the action performed.

        Returns:
        str: A string representation of the affected data.
        """
        if isinstance(details, dict):
            return self.format_dict(details)
        elif isinstance(details, list):
            return ', '.join(str(d) for d in details)
        elif isinstance(details, pd.DataFrame):
            return f"{len(details)} rows affected"
        else:
            return str(details)

    def format_dict(self, details):
        """
        Format dictionary details in a readable way.

        Parameters:
        details (dict): The dictionary to format.

        Returns:
        str: Formatted string of dictionary details.
        """
        formatted = []
        for key, value in details.items():
            if isinstance(value, pd.DataFrame):
                formatted.append(f"{key}: {len(value)} rows affected")
            elif isinstance(value, list):
                formatted.append(f"{key}: {', '.join(map(str, value))}")
            else:
                formatted.append(f"{key}: {value}")
        return "\n    ".join(formatted)

    def get_summary(self):
        """
        Generate a summary of data cleaning actions.

        Returns:
        str: A concise summary of the data cleaning process.
        """
        if not self.logs:
            return "No actions were performed during data cleaning."

        summary = ["Data Cleaning Summary:"]
        
        for log in self.logs:
            action = log["action"]
            details = log["details"]
            summary.append(f"- {action}: {self.summarize_details(details)}")
        
        return "\n".join(summary)

    def summarize_details(self, details):
        """
        Provide a short summary of the details.

        Parameters:
        details (any): The details related to the action performed.

        Returns:
        str: A short summary of the affected data.
        """
        if isinstance(details, dict):
            return f"Changes to columns/rows: {', '.join(details.keys())}"
        elif isinstance(details, list):
            return f"Affected columns: {', '.join(details)}"
        elif isinstance(details, pd.DataFrame):
            return f"{len(details)} rows were modified"
        else:
            return str(details)