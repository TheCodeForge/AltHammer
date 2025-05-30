from os import environ
import secrets
import time
from flask import *
from flask_caching import Cache

app = Flask(
    __name__,
    template_folder='./templates',
    static_folder='./assets'
    )
app.config["CACHE_TYPE"]                    = "FileSystemCache"
app.config["CACHE_DIR"]                     = "flaskcache"
cache=Cache(app)

from .classes import *
from .helpers.filters import *
from .helpers.hashes import *
from .routes import *

app.url_map.strict_slashes=False

app.config['SECRET_KEY']                    = environ.get("SECRET_KEY", secrets.token_hex(128))
app.config['SERVER_NAME']                   = environ.get("SERVER_NAME")
app.config["SITE_NAME"]                     = environ.get("SITE_NAME", "AltHammer")
app.config['FORCE_HTTPS']                   = bool(int(environ.get("FORCE_HTTPS", 1)))
app.config['SESSION_COOKIE_SECURE']         = True

#===STYLE===
app.config['COLOR_PRIMARY']                 = environ.get("COLOR_PRIMARY", "0d6efd").lstrip().rstrip()
app.config['COLOR_SECONDARY']               = environ.get("COLOR_SECONDARY", "6c757d").lstrip().rstrip()


@app.before_request
def before_request():

    g.time=int(time.time())

    if app.config["FORCE_HTTPS"] and request.scheme=="http":
        return redirect(f"https://{app.config['SERVER_NAME']}{request.path}")

    session.permanent=True

    if "session_id" not in session:
        session["session_id"]=secrets.token_hex(16)

    #script nonce
    g.nonce=generate_hash(f"{session.get('session_id')}+{g.time}")

    #csrf
    g.csrf_token=generate_hash(session.get('session_id'))

    #anti-csrf
    if request.method in ["POST", "PUT", "DELETE"] and request.form.get("csrf_token") != g.csrf_token:
        abort(401)


@app.after_request
def after_request(resp):
    
    resp.headers["Content-Security-Policy"] = f"default-src * data:; script-src 'self' code.jquery.com cdn.jsdelivr.net 'nonce-{g.nonce}'; object-src 'none'; style-src 'self' 'nonce-{g.nonce}' cdn.jsdelivr.net; media-src 'none';"
    resp.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    resp.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    resp.headers["Permissions-Policy"] = "geolocation=(self)"
    resp.headers["Referrer-Policy"] = "same-origin"
    resp.headers["Strict-Transport-Security"] = "max-age=31536000"
    resp.headers["X-Content-Type-Options"]="nosniff"
    resp.headers["X-Frame-Options"]="DENY"

    if request.path.startswith("/assets/"):
        resp.headers["Cache-Control"] = "public, max-age=604800"

    return resp