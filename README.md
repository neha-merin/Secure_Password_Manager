# 🔐 Secure Password Manager (Python + Flask)

A cybersecurity-focused password manager built using Python and Flask that securely stores credentials using strong authentication and encryption techniques.  
This project demonstrates **secure credential handling**, **defensive design**, and **separation of concerns**.

---

## 🚀 Features

- Master password authentication using **bcrypt hashing**
- Encrypted password vault using **AES (Fernet)**
- Encryption key derived from the master password
- Password strength checker (Weak / Medium / Strong)
- Flask-based web user interface
- Secure session-based login
- SQLite database for local storage

---

## 🧠 Security Design

### 🔑 Authentication
- The master password is **never stored in plaintext**
- It is stored as a **bcrypt hash**, making brute-force attacks impractical

### 🔐 Encryption
- All stored passwords are **encrypted**
- The encryption key is derived from the master password
- Passwords remain unreadable even if the database is compromised

### 🛡️ Threats Mitigated
- Database breaches
- Brute-force password attacks
- Rainbow table attacks
- Plaintext password storage

---

## 🧩 Architecture
User
↓
Flask Web UI (app.py)
↓
Secure Backend (auth.py)
↓
Encrypted SQLite Database (storage.db)


## 🌐 Demo
-LOGIN PAGE:
<img width="1920" height="878" alt="image" src="https://github.com/user-attachments/assets/6e3b18fe-dbd4-46cc-b24c-e1ed79dd16ae" />
-PASSWORD VAULT:
<img width="1920" height="826" alt="image" src="https://github.com/user-attachments/assets/f7060199-6d6f-4d09-9d3f-abf256805c0b" />
-PASSWORD CHECKER:
<img width="1797" height="811" alt="image" src="https://github.com/user-attachments/assets/cd3c4057-f842-41db-813c-1bbf25a8f8ac" />


This application is intended to run locally for security reasons.

A live public deployment is intentionally avoided to prevent exposure
of sensitive credential-handling functionality.

⚠️ Security Disclaimer

This project is intended for educational and demonstration purposes only.
It runs locally on localhost and is not production-hardened (no HTTPS, CSRF protection, or rate limiting).

🔮 Future Improvements

Auto-lock / inactivity timeout

Clipboard auto-clear


👩‍💻 Author

Built as a cybersecurity project to demonstrate secure authentication, encryption, and defensive software design principles.
