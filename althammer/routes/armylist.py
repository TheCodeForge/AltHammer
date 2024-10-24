from althammer.helpers.get import *

from flask import *

from althammer.__main__ import app


@app.post('/armylist/')
def post_armylist():

    faction=request.form.get('faction')
    unit_id=request.form.get('unit_id')
    qty=request.form.get('qty')

    session[f"qty_{faction}_{unit_id}"] = int(qty)

    return "",204