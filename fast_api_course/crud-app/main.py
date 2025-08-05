from fastapi import FastAPI, HTTPException, Depends
import models, schemas, crud
from database import Base, engine, SessionLocal
from typing import List
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

# dependence with DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/employees', response_model= schemas.EmployeeOut)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)

@app.get('/employees', response_model= List[schemas.EmployeeOut])
def get_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)

@app.get('/employees/{emp_id}', response_model=schemas.EmployeeOut)
def get_employee(emp_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, emp_id)
    
    if employee is None:
        raise HTTPException(status_code= 404, detail= {'message': 'Employee not found'})
    return employee

@app.put('/employees/{emp_id}', response_model= schemas.EmployeeOut)
def update_employee(emp_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = crud.update_employee(db, emp_id, employee)
    if employee is None:
        raise HTTPException(status_code= 404, detail= {'message': 'Employee not found'})
    return db_employee

@app.delete('/employees/{emp_id}', response_model=dict)
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    employee = crud.delete_employee(db, emp_id)
    if employee is None:
        raise HTTPException(status_code=404, detail={'message': 'Employee Not Found'})
    # return employee
    return {'message': 'Employee Deleted'}

