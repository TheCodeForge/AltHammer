from mistletoe.span_token import SpanToken
from mistletoe.block_token import BlockToken
from mistletoe.html_renderer import HTMLRenderer
import re

class Keyword(SpanToken):

    pattern = re.compile(r"\+((\[|\b).{3,25}?(\]|\b))\+")
    parse_inner = False

    def __init__(self, match_obj):
        self.target = match_obj.group(1)

class H1Block(BlockToken):

    pattern = re.compile(r"^#{1} .+?\n\n(.+?)(?=\n#)")
    parse_inner = True

    def __init__(self, match_obj):
        self.target = match_obj.group(1)

class H2Block(H1Block):
    pattern = re.compile(r"^#{2} .+?\n\n(.+?)(?=\n#)")

class H3Block(H1Block):
    pattern = re.compile(r"^#{3} .+?\n\n(.+?)(?=\n#)")

class H4Block(H1Block):
    pattern = re.compile(r"^#{4} .+?\n\n(.+?)(?=\n#)")

class H5Block(H1Block):
    pattern = re.compile(r"^#{5} .+?\n\n(.+?)(?=\n#)")

class H6Block(H1Block):
    pattern = re.compile(r"^#{6} .+?\n\n(.+?)(?=\n#)")



class CustomRenderer(HTMLRenderer):

    def __init__(self, *args, **kwargs):
        super().__init__(Keyword, *args, **kwargs)

        for i in kwargs:
            self.__dict__[i] = kwargs[i]

    def render_keyword(self, token):
        return f'<span class="keyword">{token.target}</span>'

class NumberedRenderer(CustomRenderer):

    def __init__(self, **kwargs):
        super().__init__(H1Block, H2Block, H3Block, H4Block, H5Block, H6Block)

    def render_h1_block(self, token):
        return f'<div class="h1-block">{token.target}</div>'

    def render_h2_block(self, token):
        return f'<div class="h2-block">{token.target}</div>'

    def render_h3_block(self, token):
        return f'<div class="h3-block">{token.target}</div>'

    def render_h4_block(self, token):
        return f'<div class="h4-block">{token.target}</div>'

    def render_h5_block(self, token):
        return f'<div class="h5-block">{token.target}</div>'

    def render_h6_block(self, token):
        return f'<div class="h6-block">{token.target}</div>'