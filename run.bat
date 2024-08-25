@echo off

REM Activate virtual environment (if applicable)
REM If you don't use a virtual environment, comment out the next line
call .venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Run the FastAPI application
uvicorn main:app --reload 
