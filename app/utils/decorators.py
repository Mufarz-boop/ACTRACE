from functools import wraps
from flask import session, redirect, url_for, flash

def student_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Silakan login terlebih dahulu.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped