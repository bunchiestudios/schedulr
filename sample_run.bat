set FLASK_APP=app
set FLASK_ENV=development
set SCHEDULR_SETTINGS=%cd%/config/config.py
python -m flask run --port 80
