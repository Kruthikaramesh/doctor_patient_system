import pandas as pd
import sqlite3
from config.database import get_db_connection
from config.settings import logger


def export_reports_to_excel():
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM reports", conn)
        conn.close()

        file_path = "exports/reports.xlsx"
        df.to_excel(file_path, index=False)

        logger.info("Reports exported to Excel successfully.")
        return file_path
    except Exception as e:
        logger.error(f"Error exporting reports to Excel: {str(e)}")
        raise Exception("Failed to export reports")
