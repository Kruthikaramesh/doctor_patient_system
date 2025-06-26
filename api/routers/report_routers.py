from fastapi import APIRouter, HTTPException, UploadFile, File
import os
import shutil
from config.database import get_db_connection, REPORTS_DIR
from config.settings import logger

router = APIRouter()

@router.post("/patients/{patient_id}/upload_report/")
async def upload_report(patient_id: int, test_name: str, file: UploadFile = File(...)):
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

        logger.info(f"Report uploaded for patient {patient_id} at {file_path}")
        return {"message": "Report uploaded successfully", "file_path": file_path}
    except Exception as e:
        logger.error(f"Error uploading report for patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
