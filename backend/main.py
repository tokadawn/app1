from fastapi import FastAPI
import mysql.connector
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv()

app = FastAPI()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

@app.post("/register")
def register_user(name: str, email: str, password: str):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, hashed.decode("utf-8"))
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "User registered successfully"}

@app.get("/users")
def list_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, created_at FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"users": users}
