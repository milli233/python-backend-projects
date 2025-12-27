from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Calculation(BaseModel):
    a: float
    b: float
    operation: str  # "add", "subtract", "multiply", "divide"

@app.post("/calculate")
def calculate(data: Calculation):
    if data.operation == "add":
        result = data.a + data.b
    elif data.operation == "subtract":
        result = data.a - data.b
    elif data.operation == "multiply":
        result = data.a * data.b
    elif data.operation == "divide":
        if data.b == 0:
            raise HTTPException(status_code=400, detail="Division by zero not allowed")
        result = data.a / data.b
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")
    
    return {
        "a": data.a,
        "b": data.b,
        "operation": data.operation,
        "result": result
    }
