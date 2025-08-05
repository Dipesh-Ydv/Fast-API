from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50,title='Name of Patient', description='Enter the name of patient', examples=['Aman', 'Chaman'])]
    age: int = Field(gt=0, lt=120, description='Enter the age of patient')
    weight: Annotated[float, Field(gt=0, strict=True)]
    email: EmailStr
    linkedin_url: AnyUrl    # for checking a valid url
    married: bool = False   
    allergies: List[str] = Field(default=None, max_length=5)    # We used List[str] instead of list because to perform two step validation i.e. allergies should be list as well as of str data type
    contact: Optional[Dict[str, str]] = None    # Optional is used to make this field optional but we have to provide a default value i.e. None

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.contact)
    print('Patient Inserted Successfully')

patient_info = {'name': 'Aman', 'age': '22', 'weight': 65.3, 'email': 'abc@gmail.com','linkedin_url': 'https://linkedin.com/dipesh-yadav-datascientist','allergies': ['pollen', 'dust']}#'contact': {'phone': '2132343211'}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)

