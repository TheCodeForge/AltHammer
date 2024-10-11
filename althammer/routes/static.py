import sass
import cssutils
from flask import *
from werkzeug.utils import safe_join

from althammer.__main__ import app

@app.get('/')
def home():
    return render_template(
        "home.html"
        )

@app.get("/core_rules")
def core_rules():
    return render_template("core_rules.html")

@app.get("/assets/style/<stylefile>.css")
def light_css(stylefile):
    with open(safe_join("althammer/assets/style/", stylefile)+'.scss') as stylesheet:
        scss=stylesheet.read()
        scss=scss.replace('{primary}', app.config['COLOR_PRIMARY'])
        scss=scss.replace('{secondary}', app.config['COLOR_SECONDARY'])

        css=sass.compile(string=scss)


    #pseudo rtlcss postprocessing
    #==EXPERIMENTAL==
    if request.args.get('rtl'):

        cssutils.ser.prefs.resolveVariables=False

        sheet = cssutils.parseString(css)

        for rule in sheet:

            if not isinstance(rule, cssutils.css.CSSStyleRule):
                continue

            rule.selectorText = rule.selectorText.replace("left","right").replace("Left", "Right").replace("LEFT","RIGHT")

        css=sheet.cssText

    return Response(
        css,
        mimetype="text/css"
        )

@app.post("/toggle_darkmode")
def post_toggle_darkmode():
    session["darkmode"] = not session.get('darkmode', False)
    return "", 201

@app.get("/robots.txt")
def robots_txt():
    return send_file("./assets/robots.txt")