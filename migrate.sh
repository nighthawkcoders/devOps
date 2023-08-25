sqlite3 instance/volumes/sqlite.db ".backup instance/volumes/sqlite-backup.db"
export FLASK_APP=main
export PYTHONPATH=.:$PYTHONPATH  # flask need . to find files
python3 -m flask db init
python3 -m flask db upgrade