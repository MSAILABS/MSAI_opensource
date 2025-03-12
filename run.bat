@echo off
start cmd /k "cd /d .\ui && npm run dev"
start cmd /k "cd /d .\agents && venv\scripts\activate && python main.py"
start cmd /k "cd /d .\backend && venv\scripts\activate && python main.py"