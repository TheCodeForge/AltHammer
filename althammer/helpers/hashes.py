import hmac
import secrets

from .b36 import *

from flask import g, session
from os import environ

from althammer.__main__ import app

def generate_hash(string):

    msg = bytes(string, "utf-16")

    return hmac.new(key=bytes(app.config["SECRET_KEY"], "utf-16"),
                    msg=msg,
                    digestmod='md5'
                    ).hexdigest()


def validate_hash(string, hashstr):

    return hmac.compare_digest(hashstr, generate_hash(string))

def logged_out_csrf_token():

    if "session_id" not in session:
        session["session_id"]=secrets.token_hex(16)

    return generate_hash(f"{g.time}+{session['session_id']}")

def validate_logged_out_csrf_token(t, token):

    #logged out csrf tokens expire after 1hr
    if g.time-t > 3600:
        return False

    return validate_hash(f"{t}+{session['session_id']}", token)

def compute_otp_recovery_code(user, otp_secret):

    hashstr = generate_hash(f"{otp_secret}+{user.type_id}+{user.username}")

    removal_code = base36encode(int(hashstr,16))
    
    while len(removal_code)<25:
        removal_code="0"+removal_code

    return removal_code