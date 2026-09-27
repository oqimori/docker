import os
import time
from flask import Flask, jsonify

import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)

def get_connection(retries=10, delay=2):
    """Пытаемся подключиться к БД с повторами — Postgres стартует не сразу."""
    for attempt in range(1, retries + 1):
        try:
            return psycopg2.connect(
                host="db",
                port="5432",
                dbname="ASD",
                user="333",
                password="123",
            )
        except OperationalError as e:
            print(f"[{attempt}/{retries}] БД ещё не готова: {e}")
            time.sleep(delay)
    raise RuntimeError("Не удалось подключиться к PostgreSQL")

@app.route("/")
def hello():
    return "Hello, Docker!"

@app.route("/db")
def db_check():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify({"status": "ok", "postgres": version})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)