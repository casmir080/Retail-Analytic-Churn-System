from backend.db.connection import engine
from sqlalchemy import text

def create_tables():
    with open("backend/db/create_tables.sql", "r") as file:
        sql = file.read()

    with engine.begin() as conn: 
        conn.execute(text(sql))

    print("TABLES CREATED SUCCESSFULLY")

if __name__ == "__main__":
    create_tables()