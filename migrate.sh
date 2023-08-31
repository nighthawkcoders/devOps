sqlite3 instance/volumes/sqlite.db ".backup instance/volumes/sqlite-backup-1.db"
export FLASK_APP=main
export PYTHONPATH=.:$PYTHONPATH  # flask need . to find files
rm -rf migrate/
python3 -m flask db init
python3 -m flask db migrate
python3 -m flask db upgrade
