from .hashes import *

from althammer.__main__ import app

@app.template_filter('nonce')
def nonce(x):
    return generate_hash(f"{session.get('session_id')}+{x}")