from flask import Flask, render_template, request, redirect, url_for, session
from auth import (
    init_db,
    init_vault,
    setup_master_password,
    login,
    add_password,
    view_passwords,
    check_password_strength
)

app = Flask(__name__)
app.secret_key = "dev_secret_key"  # demo-only secret

# Initialize database and vault
init_db()
init_vault()

# -----------------------
# LOGIN PAGE
# -----------------------
@app.route("/", methods=["GET", "POST"])
def login_page():
    error = None

    if request.method == "POST":
        password = request.form["password"]

        if login(password):
            session["master_password"] = password
            return redirect(url_for("dashboard"))
        else:
            error = "Wrong master password"

    return render_template("login.html", error=error)


# -----------------------
# DASHBOARD
# -----------------------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "master_password" not in session:
        return redirect(url_for("login_page"))

    message = None
    strength = None

    if request.method == "POST":
        site = request.form["site"]
        username = request.form["username"]
        password = request.form["password"]

        strength, feedback = check_password_strength(password)

        if strength == "Weak":
            message = "Weak password: " + ", ".join(feedback)
        else:
            add_password(site, username, password, session["master_password"])
            message = f"Password saved successfully ({strength})"

    passwords = view_passwords(session["master_password"])

    return render_template(
        "dashboard.html",
        passwords=passwords,
        message=message,
        strength=strength
    )


# -----------------------
# LOGOUT
# -----------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


# -----------------------
# APP ENTRY POINT
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
