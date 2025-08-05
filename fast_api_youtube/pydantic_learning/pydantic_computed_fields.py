from pydantic import BaseModel, EmailStr, AnyUrl, computed_field
from typing import List, Dict

class Patient(BaseModel):
    name: str
    age: int 
    height: float # mtr
    weight: float # kg
    email: EmailStr
    linkedin_url: AnyUrl  
    married: bool = False   
    allergies: List[str] 
    contact: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/ (self.height)**2, 2)
        return bmi


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.contact)
    print("BMI", patient.bmi)
    print('Patient Inserted Successfully')

patient_info = {'name': 'aman', 'age': 85, 'height': 1.75, 'weight': 75, 'email': 'abc@gmail.com', 'linkedin_url': 'https://www.linkedin.com/in/dipesh-yadav-datascientist', 'allergies': ['pollen', 'dust'], 'contact': {'phone': '2132343211', 'emergency': '1322344432'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)