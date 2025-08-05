from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    age: int 
    weight: float
    email: EmailStr
    linkedin_url: AnyUrl  
    married: bool = False   
    allergies: List[str] 
    contact: Dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['gmail.com', 'yahoo.com', 'outlook.com']
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value
    
    @field_validator('name', mode='after')      # mode decide when the value is provided i.e. befor or after type coresion 
    @classmethod
    def transform_name(cls, value):
        return value.capitalize()
    
    @field_validator('age', mode= 'before')     # it will give error if we passes str age because mode is set to before
    @classmethod
    def validate_age(cl, value):
        if not 0 < value <= 100:
            raise ValueError('Age should be between 0 to 100')
        return value



def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.contact)
    print('Patient Inserted Successfully')

patient_info = {'name': 'aman', 'age': 21, 'weight': 65.3, 'email': 'abc@gmail.com', 'linkedin_url': 'https://linkedin.com/dipesh-yadav-datascientist', 'allergies': ['pollen', 'dust'], 'contact': {'phone': '2132343211'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)