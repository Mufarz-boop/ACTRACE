from flask import render_template, session
from app.student import student_bp
from app.utils.decorators import student_required
from app.db import get_db_connection

@student_bp.get("/dashboard")
@student_required
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT COUNT(*) AS total FROM journals WHERE user_id=%s", (session["user_id"],))
        total = cur.fetchone()["total"]
        cur.execute(
            "SELECT activity_date, title FROM journals WHERE user_id=%s ORDER BY activity_date DESC, journal_id DESC LIMIT 1",
            (session["user_id"],),
        )
        latest = cur.fetchone()
    finally:
        cur.close()
        conn.close()
    return render_template("student/dashboard.html", total_journals=total, latest_activity=latest)

@student_bp.get("/journals")
@student_required
def journals():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT journal_id, activity_date, title, description FROM journals WHERE user_id=%s ORDER BY activity_date DESC",
            (session["user_id"],),
        )
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()
    return render_template("student/journals.html", journals=rows)
