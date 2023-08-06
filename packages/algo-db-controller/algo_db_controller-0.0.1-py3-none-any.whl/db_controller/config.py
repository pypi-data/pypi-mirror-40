import os

DATABASE_CONFIG = {
    "dbname": os.environ['DB_NAME'],
    "user": os.environ["DB_USER"]
}

try:
    DATABASE_CONFIG["host"] = os.environ['DB_HOST']
    DATABASE_CONFIG["password"] = os.environ['DB_PASSWORD']
    DATABASE_CONFIG["port"] = os.environ['DB_PORT']
except KeyError:
    pass
