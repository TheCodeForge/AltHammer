from althammer.helpers.get import *

from flask import *

from althammer.__main__ import app


@app.post('/armylist/')
def post_armylist():

    faction=request.form.get('faction')
    unit_id=request.form.get('unit_id')
    qty=request.form.get('qty')

    session[f"qty_{faction}_{unit_id}"] = qty

    return "",204


@app.post('/hide_rows/<x>')
def post_toggle_hide_rows_x(x):

    if x not in ['0','1']:
        abort(404)

    session['hide_rows']=bool(int(x))

    return "", 204