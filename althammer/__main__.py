from .classes import *
from .helpers.hashes import *

from flask import *
from os import environ
import secrets

app = Flask(
    __name__,
    template_folder='./templates',
    static_folder='./assets'
    )

from .routes import *

app.url_map.strict_slashes=False

app.config['SECRET_KEY']                    = environ.get("SECRET_KEY", secrets.token_hex(128))
app.config['SERVER_NAME']                   = environ.get("SERVER_NAME")
app.config['FORCE_HTTPS']                   = bool(int(environ.get("FORCE_HTTPS", 1)))
app.config['SESSION_COOKIE_SECURE']         = True

@app.before_request
def before_request():

    if app.config["FORCE_HTTPS"] and request.scheme=="http":
        return redirect(f"https://{app.config['SERVER_NAME']}{request.path}")

    session.permanent=True

    if "session_id" not in session:
        session["session_id"]=secrets.token_hex(16)


@app.after_request
def after_request(resp):

    #script nonce
    nonce=generate_hash(f"{session.get('session_id')}+{g.time}")
    
    resp.headers["Content-Security-Policy"] = f"default-src * data:; script-src 'self' code.jquery.com cdn.jsdelivr.net 'nonce-{nonce}'; object-src 'none'; style-src 'self' 'nonce-{nonce}' cdn.jsdelivr.net; media-src 'none';"
    resp.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    resp.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    resp.headers["Permissions-Policy"] = "geolocation=(self)"
    resp.headers["Referrer-Policy"] = "same-origin"
    resp.headers["Strict-Transport-Security"] = "max-age=31536000"
    resp.headers["X-Content-Type-Options"]="nosniff"
    resp.headers["X-Frame-Options"]="DENY"

    return resp