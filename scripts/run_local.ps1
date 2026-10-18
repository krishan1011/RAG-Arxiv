# Start backend in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\.venv\Scripts\python.exe main.py"

# Start frontend in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; .\.venv\Scripts\python.exe -m http.server 5500"

Write-Host "Backend and frontend started!"
Write-Host "Frontend available at: http://localhost:5500"