export PYTHONPATH="${PYTHONPATH}:./server"
uvicorn server.main:app --reload