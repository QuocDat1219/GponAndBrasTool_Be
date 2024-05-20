@echo off
python -m uvicorn index:app --host 0.0.0.0 --port 8000 --reload
