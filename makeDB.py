"""
    This small script takes in either a connection string or the path to the app's config file
    and will use it to connect to the DBMS to create the required tables.
    PLEASE NOTE that most DBMSs will require the creation of a database beforehand, this is
    NOT implemented here as that depends too much on the target DB backend. You must do it by hand.
"""
import sys
from sqlalchemy import create_engine
from app import models

if len(sys.argv) != 3:
    print(f"Usage:\npython {sys.argv[0]} string <db-connection-string>\npython {sys.argv[0]} file <path/to/config.file>")
    exit()

db_string = None

if sys.argv[1] == 'string':
    db_string = sys.argv[2]
elif sys.argv[1] == 'file':
    with open(sys.argv[2], 'r') as f:
        confile = f.read()
    data = {}
    exec(confile, {'__builtins__': None}, data)
    if 'DB_STRING' in data:
        db_string = data['DB_STRING']
    else:
        print(f"Config file does not declare DB_STRING")
else:
    print(f"Invalid option: {sys.argv[1]}")

if db_string is None:
    exit()

print(f"Initializing DB in: {db_string}")

db_engine = create_engine(db_string)

models.Base.metadata.create_all(db_engine)

print("Success!")
