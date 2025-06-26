# import paho.mqtt.client as mqtt
# import json
# import sqlite3
# from config.database import get_db_connection
#
# MQTT_BROKER = "135.235.145.253"
# MQTT_PORT=1883
# MQTT_TOPIC = "medical/reports"
#
# mqtt_client = mqtt.Client()
# mqtt_client.connect(MQTT_BROKER, 1883, 60)
#
# def analyze_report(report_id: int, disease: str):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     cursor.execute("UPDATE reports SET disease=? WHERE id=?", (disease, report_id))
#     conn.commit()
#     conn.close()
#
#     mqtt_message = json.dumps({"report_id": report_id, "disease": disease})
#     mqtt_client.publish(MQTT_TOPIC, mqtt_message)
#
#     return {"message": "Report analyzed and updated."}
#
import os
import shutil
import pandas as pd
from config.database import get_db_connection, REPORTS_DIR
from fastapi import HTTPException, UploadFile

def save_report_to_disk(patient_id: int, test_name: str, file: UploadFile) -> str:
    """Save the uploaded report file to disk."""
    file_path = os.path.join(REPORTS_DIR, f"{patient_id}_{test_name}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path

def add_report_to_db(patient_id: int, test_name: str, file_path: str):
    """Insert the report details into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reports (patient_id, test_name, report_path) VALUES (?, ?, ?)",
                   (patient_id, test_name, file_path))
    conn.commit()
    conn.close()

def get_report_path(report_id: int) -> str:
    """Retrieve the file path of a report from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT report_path FROM reports WHERE id=?", (report_id,))
    report = cursor.fetchone()
    conn.close()
    if report:
        return report["report_path"]
    raise HTTPException(status_code=404, detail="Report not found")

def generate_reports_summary() -> str:
    """Generate an Excel file containing all reports."""
    conn = get_db_connection()
    reports = pd.read_sql_query("SELECT * FROM reports", conn)
    conn.close()
    excel_path = "reports_summary.xlsx"
    reports.to_excel(excel_path, index=False)
    return excel_path

