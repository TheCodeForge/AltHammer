import cssutils
import sass
import jinja2
from flask import *
from werkzeug.utils import safe_join

from althammer.__main__ import app, cache

@app.get('/')
def home():
    return render_template(
        "home.html"
        )

@app.get("/rules/<x>")
def rules_x(x):
    try:
        return render_template(safe_join("rules", f"{x}.html"))
    except jinja2.exceptions.TemplateNotFound:
        abort(404)

@app.get("/assets/style/<stylefile>.css")
@cache.memoize()
def light_css(stylefile):
    with open(safe_join("althammer/assets/style/", stylefile)+'.scss') as stylesheet:
        scss=stylesheet.read()
        scss=scss.replace('{primary}', app.config['COLOR_PRIMARY'])
        scss=scss.replace('{secondary}', app.config['COLOR_SECONDARY'])
        scss=scss.replace('{faction}', request.args.get('color',''))

        css=sass.compile(string=scss)


    # #pseudo rtlcss postprocessing
    # #==EXPERIMENTAL==
    # if request.args.get('rtl'):

    #     cssutils.ser.prefs.resolveVariables=False

    #     sheet = cssutils.parseString(css)

    #     for rule in sheet:

    #         if not isinstance(rule, cssutils.css.CSSStyleRule):
    #             continue

    #         rule.selectorText = rule.selectorText.replace("left","right").replace("Left", "Right").replace("LEFT","RIGHT")

    #     css=sheet.cssText

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