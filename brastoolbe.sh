source venv/bin/activate
fuser -k 9090/tcp
uvicorn index:app --port 9090 --host 0.0.0.0 --reload