
import bcrypt
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    current_app,
)

from app.auth import auth_bp
from app.db import get_db_connection


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("student.dashboard"))

    if request.method == "POST":
        identity = request.form.get("identity", "").strip()
        password = request.form.get("password", "")

        if not identity or not password:
            flash(
                "Username/email dan kata sandi wajib diisi.",
                "error"
            )
            return render_template("auth/login.html")

        conn = None
        cur = None

        try:
            conn = get_db_connection()
            cur = conn.cursor(dictionary=True)

            cur.execute(
                """
                SELECT
                    user_id,
                    student_code,
                    full_name,
                    password_hash
                FROM users
                WHERE username = %s OR email = %s
                LIMIT 1
                """,
                (identity, identity),
            )

            user = cur.fetchone()

        except RuntimeError:
            current_app.logger.exception(
                "Gagal mengakses database saat login."
            )
            flash(
                "Layanan sedang mengalami gangguan. "
                "Silakan coba kembali.",
                "error"
            )
            return render_template("auth/login.html")

        finally:
            if cur is not None:
                cur.close()

            if conn is not None:
                conn.close()

        valid = False

        if user:
            try:
                valid = bcrypt.checkpw(
                    password.encode("utf-8"),
                    user["password_hash"].encode("utf-8")
                )
            except (ValueError, AttributeError):
                valid = False

        if not valid:
            flash(
                "Identitas atau kata sandi tidak sesuai.",
                "error"
            )
            return render_template("auth/login.html")

        session.clear()
        session.permanent = True

        session["user_id"] = user["user_id"]
        session["student_code"] = user["student_code"]
        session["full_name"] = user["full_name"]

        return redirect(url_for("student.dashboard"))

    return render_template("auth/login.html")


@auth_bp.post("/logout")
def logout():
    session.clear()
    flash("Kamu berhasil keluar dari ACTRACE.", "success")
    return redirect(url_for("auth.login"))