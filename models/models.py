from pydantic import BaseModel
from typing import Optional

class Patient(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    gender: str
    contact: str
    address: str

class Report(BaseModel):
    id: Optional[int] = None
    patient_id: int
    test_name: str
    report_path: str
    disease: Optional[str] = None

class Prescription(BaseModel):
    id: Optional[int] = None
    patient_id: int
    doctor_id: int
    prescription: str
    date: str
