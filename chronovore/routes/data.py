from althammer.helpers.get import *

from flask import *

from althammer.__main__ import app

@app.get("/faction/<faction>")
def faction_faction(faction):

    f = get_faction(faction)

    return render_template("faction.html", f=f)


@app.get("/faction/<faction>/detachment/<detachment>")
def faction_faction_detachment_detachment(faction, detachment):

    f = get_faction(faction)

    d = f.detachment(detachment)

    return render_template("detachment.html", f=f, d=d)

@app.get("/faction/<faction>/unit/<unit>")
@app.get("/faction/<faction>/detachment/<detachment>/unit/<unit>")
def faction_faction_unit_unit(faction, unit, detachment=None):

    f=get_faction(faction)
    color=f.color

    u = f.unit(unit)

    if detachment:
        d=f.detachment(detachment)
        if not d.is_legal(u):
            abort(404)
        color=d.color
    else:
        d=None

    return render_template(
        "unit.html", 
        f=f, 
        u=u, 
        d=d, 
        color=color)