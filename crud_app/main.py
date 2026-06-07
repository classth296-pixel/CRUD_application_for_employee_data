from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine,base
from typing import List

# ensure database tables are created
models.base.metadata.create_all(bind=engine)

app=FastAPI()

#dependency with with the DB
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()  

# end points
@app.post("/employees/", response_model=schemas.EmployeeOut)
def create_employee(employee:schemas.EmployeeCreate, db:Session=Depends(get_db)):
    return crud.create_employee(db=db,employee=employee)


# get all employees
@app.get('/employees',response_model=List[schemas.EmployeeOut])
def get_employees(db: Session=Depends(get_db)):
    return crud.get_employees(db=db)

#get a specific employee
@app.get('/employees/{emp_id}',response_model=schemas.EmployeeOut)
def get_employee(emp_id:int, db: Session=Depends(get_db)):
    employee=crud.get_employee(db,emp_id=emp_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

#update an employee
@app.put('/employees/{emp_id}',response_model=schemas.EmployeeOut)
def update_employee(emp_id:int, employee:schemas.EmployeeUpdate, db: Session=Depends(get_db)):
    db_employee=crud.update_employee(db,emp_id=emp_id,employee=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

#delete an employee
@app.delete('/employees/{emp_id}',response_model=schemas.EmployeeOut)
def delete_employee(emp_id:int, db: Session=Depends(get_db)):
    db_employee=crud.delete_employee(db,emp_id=emp_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"detail": "Employee deleted successfully"}
