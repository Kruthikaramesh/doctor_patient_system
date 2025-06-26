from fastapi import APIRouter, HTTPException, UploadFile, File
import sqlite3
import os
import shutil
from config.database import get_db_connection, REPORTS_DIR
from config.settings import logger

router = APIRouter()


@router.post("/patients/")
def add_patient(name: str, age: int, gender: str, contact: str, address: str):
    """
    Adds a new patient to the database.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (name, age, gender, contact, address) VALUES (?, ?, ?, ?, ?)",
                       (name, age, gender, contact, address))
        conn.commit()
        conn.close()

        logger.info(f"Patient '{name}' added successfully.")
        return {"message": "Patient added successfully"}

    except Exception as e:
        logger.error(f"Error adding patient: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/patients/{patient_id}")
def update_patient(patient_id: int, name: str = None, age: int = None, gender: str = None, contact: str = None,
                   address: str = None):
    """
    Updates patient details.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        update_fields = []
        update_values = []

        if name:
            update_fields.append("name=?")
            update_values.append(name)
        if age:
            update_fields.append("age=?")
            update_values.append(age)
        if gender:
            update_fields.append("gender=?")
            update_values.append(gender)
        if contact:
            update_fields.append("contact=?")
            update_values.append(contact)
        if address:
            update_fields.append("address=?")
            update_values.append(address)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update.")

        update_values.append(patient_id)
        query = f"UPDATE patients SET {', '.join(update_fields)} WHERE id=?"
        cursor.execute(query, tuple(update_values))

        conn.commit()
        conn.close()

        logger.info(f"Patient {patient_id} updated successfully.")
        return {"message": "Patient updated successfully"}

    except Exception as e:
        logger.error(f"Error updating patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    """
    Retrieves patient details.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
        patient = cursor.fetchone()
        conn.close()

        if patient:
            logger.info(f"Retrieved patient: {patient_id}")
            return dict(patient)

        logger.warning(f"Patient {patient_id} not found.")
        raise HTTPException(status_code=404, detail="Patient not found")

    except Exception as e:
        logger.error(f"Error fetching patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/patients/{patient_id}/reports")
def get_reports(patient_id: int):
    """
    Fetches all reports for a given patient.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reports WHERE patient_id=?", (patient_id,))
        reports = cursor.fetchall()
        conn.close()

        if not reports:
            logger.warning(f"No reports found for patient {patient_id}.")
            return {"message": "No reports found"}

        logger.info(f"Retrieved reports for patient {patient_id}.")
        return [dict(report) for report in reports]

    except Exception as e:
        logger.error(f"Error fetching reports for patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    """
    Deletes a patient from the database.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
        conn.commit()
        conn.close()

        logger.info(f"Patient {patient_id} deleted successfully.")
        return {"message": "Patient deleted successfully"}

    except Exception as e:
        logger.error(f"Error deleting patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/patients/{patient_id}/submit_test/")
async def submit_test(patient_id: int, test_name: str, file: UploadFile = File(...)):
    """
    Submits a test report for a patient.
    """
    try:
        file_path = os.path.join(REPORTS_DIR, f"{patient_id}_{test_name}_{file.filename}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reports (patient_id, test_name, report_path) VALUES (?, ?, ?)",
                       (patient_id, test_name, file_path))
        conn.commit()
        conn.close()

        logger.info(f"Test {test_name} submitted for patient {patient_id}. File saved at {file_path}.")
        return {"message": "Test submitted successfully", "file_path": file_path}

    except Exception as e:
        logger.error(f"Error submitting test for patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
