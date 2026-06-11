@echo off
cd "d:\AINT-7A MID + FINAL\FYP\backend"
echo Installing psycopg2-binary...
python -m pip install psycopg2-binary==2.9.9
echo.
echo Installation complete!
echo.
echo Now try running: python manage.py runserver
pause
