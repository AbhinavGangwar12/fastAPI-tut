from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Optional, Dict
import patient_manager

# -------------------- Pydantic Model --------------------

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient")]
    name: Annotated[str, Field(..., max_length=50, title="Patient Name")]
    city: Annotated[str, Field(..., title="Home City")]
    age: int = Field(..., gt=0, lt=120)
    gender: Optional[str] = None
    height: float = Field(..., gt=0, description="Height in meters")
    weight: float = Field(..., gt=0, description="Weight in kilograms")

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class UpdatePatient(BaseModel):
    name: Optional[str] = Field(None, max_length=50, title="Patient Name")
    city: Optional[str] = Field(None, title="Home City")
    age: Optional[int] = Field(None, gt=0, lt=120)
    gender: Optional[str] = None
    height: Optional[float] = Field(None, gt=0, description="Height in meters")
    weight: Optional[float] = Field(None, gt=0, description="Weight in kilograms")

# -------------------- FastAPI App --------------------

app = FastAPI(
    title="Patient Manager API",
    description="API to manage patient records",
    version="1.0.0"
)


# -------------------- Routes --------------------

@app.get("/")
def home():
    return {"message": "Welcome to Patient Manager"}


@app.get("/about")
def about():
    return {"message": "This app helps you manage patients"}


@app.get("/view")
def view_all_patients() -> Dict[str, dict]:
    return patient_manager.get_info()


@app.get("/patient/{patient_id}", response_model=Patient)
def get_patient(
    patient_id: str = Path(..., description="Patient ID", example="p001")
):
    data = patient_manager.get_info()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient_data = data[patient_id]
    return Patient(id=patient_id, **patient_data)


@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    data = patient_manager.get_info()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude={"id"})
    patient_manager.save_data(data)

    return {"message": "Patient created successfully"}

@app.put("/update/{patient_id}", status_code=200)
def update_patient(patient_id: str, request: UpdatePatient):
    data = patient_manager.get_info()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient_data = data[patient_id]
    updated_fields = request.model_dump(exclude_unset=True)

    patient_data.update(updated_fields)

    # Validate with Patient model
    validated_patient = Patient(id=patient_id, **patient_data)

    # Save without id (id is the key)
    data[patient_id] = validated_patient.model_dump(exclude={"id"})
    patient_manager.save_data(data)

    return {
        "message": "Patient updated successfully",
        "patient": validated_patient
    }



