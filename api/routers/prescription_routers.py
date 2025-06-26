# from fastapi import APIRouter, HTTPException
# from services.prescription_service import add_prescription, get_prescriptions
#
# router = APIRouter()
#
# @router.post("/patients/{patient_id}/prescriptions/")
# def create_prescription(patient_id: int, doctor_id: int, prescription: str, date: str):
#     response = add_prescription(patient_id, doctor_id, prescription, date)
#     if "error" in response:
#         raise HTTPException(status_code=500, detail=response["error"])
#     return response
#
# @router.get("/patients/{patient_id}/prescriptions/")
# def fetch_prescriptions(patient_id: int):
#     response = get_prescriptions(patient_id)
#     if "error" in response:
#         raise HTTPException(status_code=500, detail=response["error"])
#     return response

# from fastapi import APIRouter, HTTPException
# from config.database import get_db_connection
# from config.settings import logger
#
# router = APIRouter()
#
# @router.post("/prescriptions/{patient_id}")
# def add_prescription(patient_id: int, prescription: str):
#     """
#     Adds a prescription for a patient.
#     """
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO prescriptions (patient_id, prescription) VALUES (?, ?)",
#                        (patient_id, prescription))
#         conn.commit()
#         conn.close()
#
#         logger.info(f"Prescription added for patient {patient_id}.")
#         return {"message": "Prescription added successfully"}
#
#     except Exception as e:
#         logger.error(f"Error adding prescription for patient {patient_id}: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")
#
from fastapi import APIRouter, HTTPException, Response
from services.prescription_service import add_prescription, get_prescriptions, export_prescriptions_to_excel
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/patients/{patient_id}/prescriptions/")
def fetch_prescriptions(patient_id: int):
    """
    Retrieves all prescriptions for a patient.
    """
    response = get_prescriptions(patient_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response

@router.get("/patients/{patient_id}/prescriptions/download/")
def download_prescriptions(patient_id: int):
    """
    Exports all prescriptions for a patient as an Excel file and allows downloading.
    """
    file_path = export_prescriptions_to_excel(patient_id)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="No prescriptions found for download")

    return FileResponse(file_path, filename=f"prescriptions_{patient_id}.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

