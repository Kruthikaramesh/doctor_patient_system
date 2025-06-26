import uvicorn
from fastapi import FastAPI
from api.routers.patient_routers import router as patient_router
from api.routers.doctor_routers import router as doctor_router
from api.routers.report_routers import router as report_router
from api.routers.prescription_routers import router as prescription_router
from config.settings import logger
import handlers.mqtt_handler

app = FastAPI()

app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(report_router)
app.include_router(prescription_router)

@app.get("/")
def home():
    logger.info(API is running.")
    return {"message": "Doctor-Patient System API is running"}

if __name__ == "__main__":
    logger.info("Starting FastAPI server...")
    uvicorn.run("main:app", host="localhost", port=12345, reload=True)
