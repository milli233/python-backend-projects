# Basic Backend Calculator

A simple calculator API built with FastAPI.

## How to run
1. Install dependencies: `pip install -r requirements.txt`
2. Run server: `uvicorn main:app --reload`
3. Open Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Endpoints
- POST /add
- POST /subtract
- POST /multiply
- POST /divide

## Example JSON Body
```json
{
  "a": 10,
  "b": 5
}
