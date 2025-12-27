from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Numbers(BaseModel):
    a: int
    b: int
    
@app.get("/calculator")
def read_root():
    return {"message": "Welcome to My Calculator!"}

@app.post("/add")
def add(numbers: Numbers):
    return{"result":numbers.a + numbers.b}


@app.post("/subtract")
def subtract(numbers: Numbers):
    return{"result":numbers.a - numbers.b}


@app.post("/multiply")
def multiply(numbers: Numbers):
    return{"result":numbers.a * numbers.b}


@app.post("/divide")
def divide(numbers: Numbers):
    if numbers.b == 0:
        raise HTTPException(
            status_code = 400,
            detail = "b cannot be zero"
            )
    return{"result":numbers.a / numbers.b}


