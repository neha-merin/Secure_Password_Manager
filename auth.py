import sqlite3
import bcrypt
import base64
import hashlib
from cryptography.fernet import Fernet

def init_db():
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS master (
            id INTEGER PRIMARY KEY,
            password_hash BLOB
        )
    """)
    conn.commit()
    conn.close()


def init_vault():
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY,
            site TEXT,
            username TEXT,
            password BLOB
        )
    """)
    conn.commit()
    conn.close()


def hash_master_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def setup_master_password(password: str):
    hashed = hash_master_password(password)
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO master (password_hash) VALUES (?)", (hashed,))
    conn.commit()
    conn.close()

def verify_master_password(password: str, stored_hash: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), stored_hash)

def login(password: str) -> bool:
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM master LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    if result:
        return verify_master_password(password, result[0])
    return False


 
def derive_key(master_password: str) -> bytes:
    hash_digest = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(hash_digest)

def encrypt_password(password: str, key: bytes) -> bytes:
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

def decrypt_password(encrypted_password: bytes, key: bytes) -> str:
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password).decode()

def add_password(site: str, username: str, password: str, master_password: str):
    key = derive_key(master_password)
    encrypted = encrypt_password(password, key)

    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO vault (site, username, password) VALUES (?, ?, ?)",
        (site, username, encrypted)
    )
    conn.commit()
    conn.close()


def view_passwords(master_password: str):
    key = derive_key(master_password)

    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute("SELECT site, username, password FROM vault")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for site, username, encrypted in rows:
        decrypted = decrypt_password(encrypted, key)
        results.append({
            "site": site,
            "username": username,
            "password": decrypted
        })

    return results

import re

def check_password_strength(password: str):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("At least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add an uppercase letter")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add a lowercase letter")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add a number")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add a special character")

    if score <= 2:
        return "Weak", feedback
    elif score == 3 or score == 4:
        return "Medium", feedback
    else:
        return "Strong", []
