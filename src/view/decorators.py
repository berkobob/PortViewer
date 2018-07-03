from flask import session, url_for, redirect, request
from functools import wraps

def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'login' not in session.keys() or not session['login']:
            return redirect(url_for('login', next=request.path))
        return func(*args, **kwargs)
    return decorated_function