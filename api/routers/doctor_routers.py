# from fastapi import APIRouter, HTTPException
# import sqlite3
# from config.database import get_db_connection
# from config.settings import logger
#
# router = APIRouter()
#
#
# @router.get("/doctors/patients/{patient_id}")
# def get_patient_details(patient_id: int):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
#         patient = cursor.fetchone()
#         conn.close()
#
#         if patient:
#             logger.info(f"Doctor retrieved patient: {patient_id}")
#             return dict(patient)
#
#         logger.warning(f"Doctor requested non-existing patient {patient_id}.")
#         raise HTTPException(status_code=404, detail="Patient not found")
#     except Exception as e:
#         logger.error(f"Error fetching patient {patient_id}: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")
from fastapi import APIRouter, HTTPException, UploadFile, File
import os
import shutil
from config.database import get_db_connection, REPORTS_DIR
from config.settings import logger
from services.prescription_service import add_prescription
from services.report_service import add_report_to_db, get_report_path

router = APIRouter()

@router.get("/doctors/patients/{patient_id}")
def get_patient_details(patient_id: int):
    """
    Doctor retrieves patient details.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
        patient = cursor.fetchone()
        conn.close()

        if patient:
            logger.info(f"Doctor retrieved patient: {patient_id}")
            return dict(patient)

        logger.warning(f"Doctor requested non-existing patient {patient_id}.")
        raise HTTPException(status_code=404, detail="Patient not found")
    except Exception as e:
        logger.error(f"Error fetching patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/doctors/patients/{patient_id}/reports/")
async def upload_report(patient_id: int, test_name: str, file: UploadFile = File(...)):
    """
    Doctor uploads a lab test report for a patient.
    """
    try:
        file_path = os.path.join(REPORTS_DIR, f"{patient_id}_{test_name}_{file.filename}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        response = add_report_to_db(patient_id, test_name, file_path)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])

        logger.info(f"Doctor added report {test_name} for patient {patient_id}.")
        return response

    except Exception as e:
        logger.error(f"Error uploading report for patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/doctors/patients/{patient_id}/reports/")
def get_patient_reports(patient_id: int):
    """
    Doctor retrieves all reports of a patient.
    """
    response = get_report_path(patient_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response

@router.post("/doctors/patients/{patient_id}/prescriptions/")
def add_patient_prescription(patient_id: int, doctor_id: int, prescription: str, date: str):
    """
    Doctor adds a prescription for a patient.
    """
    response = add_prescription(patient_id, doctor_id, prescription, date)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response

@router.post("/doctors/patients/{patient_id}/request_test/")
def request_test(patient_id: int, test_name: str):
    """
    Doctor requests a lab test for a patient.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO test_requests (patient_id, test_name, status) VALUES (?, ?, 'requested')",
                       (patient_id, test_name))
        conn.commit()
        conn.close()

        logger.info(f"Doctor requested test '{test_name}' for patient {patient_id}.")
        return {"message": f"Test '{test_name}' requested successfully"}

    except Exception as e:
        logger.error(f"Error requesting test for patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/doctors/patients/{patient_id}/submit_result/")
def submit_test_result(patient_id: int, test_name: str, result: str):
    """
    Doctor submits a lab test result for a patient.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE test_requests SET result=?, status='completed' WHERE patient_id=? AND test_name=?",
                       (result, patient_id, test_name))
        conn.commit()
        conn.close()

        logger.info(f"Doctor submitted result for test '{test_name}' of patient {patient_id}.")
        return {"message": f"Result for '{test_name}' submitted successfully"}

    except Exception as e:
        logger.error(f"Error submitting test result for patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
