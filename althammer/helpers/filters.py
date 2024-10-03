from .hashes import *
from .markdown import CustomRenderer

import mistletoe

from althammer.__main__ import app

@app.template_filter('app_config')
def app_config(x):
    approved_keys=[
        "COLOR_PRIMARY",
        "COLOR_SECONDARY",
        "SITE_NAME"
    ]
    if x not in approved_keys:
        raise ValueError(f"Not permitted to render config key `{x}`")
    return app.config[x]

@app.template_filter('qrcode_img_data')
def qrcode_filter(x):
  
    mem=io.BytesIO()
    qr=qrcode.QRCode()
    qr.add_data(x)
    img=qr.make_image(
        fill_color=f"#{app.config['COLOR_PRIMARY']}",
        back_color="white",
    )
    img.save(
        mem, 
        format="PNG"
    )
    mem.seek(0)
    
    data=base64.b64encode(mem.read()).decode('ascii')
    return f"data:image/png;base64,{data}"

@app.template_filter('full_link')
def full_link(x):
    return urlunparse(urlparse(x)._replace(scheme=f"http{ 's' if app.config['FORCE_HTTPS'] else '' }", netloc=app.config['SERVER_NAME']))

@app.template_filter('markdown')
def markdown_filter(x):
    with CustomRenderer() as renderer:
        return renderer.render(Document(x))

@app.template_filter('nonce')
def nonce(x):
    return generate_hash(f"{session.get('session_id')}+{x}")

