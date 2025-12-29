from fastapi import FastAPI, Path, HTTPException
import patient_manager
import json

app = FastAPI()

@app.get("/")
def hello():
    return {'message' : 'Welcome to Patient Manager'}

@app.get('/about')
def about():
    return {'message' : 'This app helps you to manage patients'}

@app.get("/view")
def get_info():
    data = patient_manager.get_info()
    return data 

@app.get('/patient/{patiend_id}')
def get_patient(patient_id : str = Path(..., description="ID of the patient in the DB", example="p001")):
    data = patient_manager.get_info()
    if patient_id in data :
        return data[patient_id]
    return HTTPException(status_code=404, detail='Patient not found!')