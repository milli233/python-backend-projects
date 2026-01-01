# Advanced Backend Calculator

A single `/calculate` endpoint API built with FastAPI.  
Supports addition, subtraction, multiplication, and division with proper error handling.

## How to run
1. Install dependencies: `pip install -r requirements.txt`
2. Run server: `uvicorn main:app --reload`
3. Open Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Endpoint
- POST /calculate
- JSON Body Example:
```json
{
  "a": 10,
  "b": 5,
  "operation": "divide"
}
