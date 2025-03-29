import streamlit as st
import mysql.connector
import hashlib

DB_CONFIG = st.secrets["db_config"]

def ensure_database():
    """Ensure that the 'leetcode-db' database exists."""
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"]
    )
    with conn.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS `leetcode-db`;")
    conn.commit()
    conn.close()

def get_db_connection():
    """Return a new database connection."""
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"]
    )

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()
