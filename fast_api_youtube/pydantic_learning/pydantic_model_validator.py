from pydantic import BaseModel, EmailStr, AnyUrl, model_validator
from typing import List, Dict

class Patient(BaseModel):
    name: str
    age: int 
    weight: float
    email: EmailStr
    linkedin_url: AnyUrl  
    married: bool = False   
    allergies: List[str] 
    contact: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact:
            raise ValueError('Patient older than 60 must have emergency contanct number')
        return model
        


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.contact)
    print('Patient Inserted Successfully')

patient_info = {'name': 'aman', 'age': 85, 'weight': 65.3, 'email': 'abc@gmail.com', 'linkedin_url': 'https://www.linkedin.com/in/dipesh-yadav-datascientist', 'allergies': ['pollen', 'dust'], 'contact': {'phone': '2132343211', 'emergency': '1322344432'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)