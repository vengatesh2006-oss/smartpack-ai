@echo off
echo Running pytest...
python -m pytest backend/app/tests

echo Running test harness...
python scripts/run_test_harness.py
pause
