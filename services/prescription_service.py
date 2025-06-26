# import sqlite3
# from config.database import get_db_connection
# from config.settings import logger
#
#
# def add_prescription(patient_id: int, doctor_id: int, prescription: str, date: str):
#     """
#     Adds a new prescription for a patient.
#     """
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     try:
#         cursor.execute("""
#             INSERT INTO prescriptions (patient_id, doctor_id, prescription, date)
#             VALUES (?, ?, ?, ?)
#         """, (patient_id, doctor_id, prescription, date))
#
#         conn.commit()
#         logger.info(f"Prescription added for patient {patient_id} by doctor {doctor_id}.")
#         return {"message": "Prescription added successfully"}
#
#     except sqlite3.Error as e:
#         logger.error(f"Error adding prescription: {str(e)}")
#         return {"error": str(e)}
#
#     finally:
#         conn.close()
#
#
# def get_prescriptions(patient_id: int):
#     """
#     Retrieves all prescriptions for a specific patient.
#     """
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     try:
#         cursor.execute("SELECT * FROM prescriptions WHERE patient_id=?", (patient_id,))
#         prescriptions = cursor.fetchall()
#
#         if not prescriptions:
#             logger.warning(f"No prescriptions found for patient {patient_id}.")
#             return {"message": "No prescriptions found"}
#
#         result = [dict(row) for row in prescriptions]
#         logger.info(f"Retrieved prescriptions for patient {patient_id}.")
#         return result
#
#     except sqlite3.Error as e:
#         logger.error(f"Error fetching prescriptions: {str(e)}")
#         return {"error": str(e)}
#
#     finally:
#         conn.close()
# import sqlite3
# import pandas as pd
# from config.database import get_db_connection
#
# def export_prescriptions_to_excel():
#     conn = get_db_connection()
#     query = "SELECT * FROM prescriptions"
#     df = pd.read_sql(query, conn)
#     conn.close()
#
#     excel_path = "exports/prescriptions.xlsx"
#     df.to_excel(excel_path, index=False)
#     return excel_path
import sqlite3
import pandas as pd
import os
from config.database import get_db_connection
from config.settings import logger

PRESCRIPTION_EXPORT_DIR = "exports"

# Ensure export directory exists
os.makedirs(PRESCRIPTION_EXPORT_DIR, exist_ok=True)

def add_prescription(patient_id: int, doctor_id: int, prescription: str, date: str):
    """
    Adds a new prescription for a patient.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO prescriptions (patient_id, doctor_id, prescription, date) VALUES (?, ?, ?, ?)",
                       (patient_id, doctor_id, prescription, date))
        conn.commit()
        conn.close()

        logger.info(f"Prescription added for patient {patient_id} by doctor {doctor_id}.")
        return {"message": "Prescription added successfully"}

    except Exception as e:
        logger.error(f"Error adding prescription: {str(e)}")
        return {"error": "Internal Server Error"}

def get_prescriptions(patient_id: int):
    """
    Fetches all prescriptions for a patient.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM prescriptions WHERE patient_id=?", (patient_id,))
        prescriptions = cursor.fetchall()
        conn.close()

        if not prescriptions:
            return {"message": "No prescriptions found"}

        logger.info(f"Retrieved {len(prescriptions)} prescriptions for patient {patient_id}.")
        return [dict(zip([column[0] for column in cursor.description], row)) for row in prescriptions]

    except Exception as e:
        logger.error(f"Error fetching prescriptions for patient {patient_id}: {str(e)}")
        return {"error": "Internal Server Error"}

def export_prescriptions_to_excel(patient_id: int):
    """
    Exports all prescriptions of a patient to an Excel file.
    """
    try:
        conn = get_db_connection()
        query = "SELECT id, doctor_id, prescription, date FROM prescriptions WHERE patient_id=?"
        df = pd.read_sql_query(query, conn, params=(patient_id,))
        if df.empty:
            logger.warning(f"No prescriptions found for patient {patient_id}.")
            return None

        file_path = os.path.join(PRESCRIPTION_EXPORT_DIR, f"prescriptions_{patient_id}.xlsx")
        df.to_excel(file_path, index=False)

        logger.info(f"Prescriptions exported for patient {patient_id} to {file_path}.")
        return file_path

    except Exception as e:
        logger.error(f"Error exporting prescriptions for patient {patient_id}: {str(e)}")
        return None
        conn.close()


