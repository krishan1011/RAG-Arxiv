#!/bin/bash

# Start backend in a new terminal window (for macOS/Linux)
# For macOS:
# osascript -e 'tell app "Terminal" to do script "cd backend; ../.venv/Scripts/python main.py"'
# For Linux (using gnome-terminal):
# gnome-terminal -- bash -c "cd backend; ../.venv/Scripts/python main.py; exec bash"

# Start frontend in a new terminal window
# For macOS:
# osascript -e 'tell app "Terminal" to do script "cd frontend; ../.venv/Scripts/python -m http.server 5500"'
# For Linux (using gnome-terminal):
# gnome-terminal -- bash -c "cd frontend; ../.venv/Scripts/python -m http.server 5500; exec bash"

# Since we're in a Git Bash environment on Windows, let's use start commands
echo "Starting backend and frontend..."
echo "To run manually:"
echo "Backend: cd backend && .venv/Scripts/python.exe main.py"
echo "Frontend: cd frontend && .venv/Scripts/python.exe -m http.server 5500"
echo ""
echo "Frontend will be available at: http://localhost:5500"