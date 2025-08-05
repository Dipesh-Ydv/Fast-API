from fastapi import FastAPI, Path, HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

class Patient(BaseModel):

    id: Annotated[str, Field(..., description='Id of the patient', examples=['P001', 'P002'])]
    name: Annotated[str, Field(..., description='Name of the patient', examples=['Raman', 'Aman'])]
    city: Annotated[str, Field(..., description='City from where patient belongs')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/ (self.height**2), 2)
    
    @computed_field
    @property
    def verdict(self) -> float:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else: 
            return 'Obese'

class UpdatedPatient(BaseModel):

    name: Annotated[str, Field(None, description='Name of the patient', examples=['Raman', 'Aman'])]
    city: Annotated[str, Field(None, description='City from where patient belongs')]
    age: Annotated[int, Field(None, gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(None, description='Gender of the patient')]
    height: Annotated[float, Field(None, gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(None, gt=0, description='Weight of the patient in kgs')]

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Patients Management System API"}

@app.get("/about")
def about():
    return {'message': "A fully functional API for managing patients records"}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='Id of the Patient in DB', example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found!')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight, or bmi'), order: str = Query('asc', description='Order in which data is sorted i.e. asc or desc')):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by.lower() not in valid_fields:
        raise HTTPException(status_code=404, detail=f'Invalid Field! Select from {valid_fields}')
    
    if order.lower() not in ['asc', 'desc']:
        raise HTTPException(status_code=404, detail='Invalid Order! Select between asc or desc')
    
    data = load_data()
    sort_order = True if order.lower() == 'desc' else False

    sorted_data = sorted(data.values(), key= lambda x: x.get(sort_by.lower(), 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    #loading the data
    data = load_data()
    
    # checking whether patient already existed or not
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already existed')
    
    # adding new patient to database
    data[patient.id] = patient.model_dump(exclude='id')

    # saving the data into json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient added successfully'})

@app.put('/update/{patient_id}')
def update_patient(patient_id: str, update_details: UpdatedPatient):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    update_patient_info = update_details.model_dump(exclude_unset=True)

    for key, value in update_patient_info.items():
        existing_patient_info[key] = value

    # existing_patient_info -> pydantic object (Patient) -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_info_pydantic = Patient(**existing_patient_info)
    # -> pydantic object -> dict
    existing_patient_info = patient_info_pydantic.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # saving the updated data
    save_data(data)

    return JSONResponse(status_code=200, content={'message' : f'Patient: {patient_id} details updated successfully'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message' : f'Patient: {patient_id} deleted successfully'})



