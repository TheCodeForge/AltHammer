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
def faction_faction_unit_unit(faction, unit):

    f=get_faction(faction)

    u = f.unit(unit, id=unit)

    return render_template("unit.html", f=f, u=u)