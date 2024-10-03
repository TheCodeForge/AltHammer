from althammer.helpers.get import *
from althammer.__main__ import app

@app.get("/faction/<faction>")
def faction_faction(faction):

    f = get_faction(faction)

    return render_template("faction.html", f=f)