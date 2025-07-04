@echo off
call .\.venv\Scripts\activate
.\.venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 10000
