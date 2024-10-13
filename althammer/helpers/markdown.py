from mistletoe.span_token import SpanToken
from mistletoe.block_token import BlockToken
from mistletoe.html_renderer import HTMLRenderer
import re

class Keyword(SpanToken):

    pattern = re.compile(r"\+((\[|\b).{3,25}?(\]|\b))\+")
    parse_inner = False

    def __init__(self, match_obj):
        self.target = match_obj.group(1)

class HOneBlock(BlockToken):

    pattern = re.compile(r"^#{1} .+?\n\n(.+?)(?=\n#)")
    parse_inner = True

    def __init__(self, match_obj):
        self.target = match_obj.group(1)

class HTwoBlock(HOneBlock):
    pattern = re.compile(r"^#{2} .+?\n\n(.+?)(?=\n#)")

class HThreeBlock(HOneBlock):
    pattern = re.compile(r"^#{3} .+?\n\n(.+?)(?=\n#)")

class HFourBlock(HOneBlock):
    pattern = re.compile(r"^#{4} .+?\n\n(.+?)(?=\n#)")

class HFiveBlock(HOneBlock):
    pattern = re.compile(r"^#{5} .+?\n\n(.+?)(?=\n#)")

class HSixBlock(HOneBlock):
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
        super().__init__(HOneBlocklock, HTwoBlock, HThreeBlock, HFourBlock, HFiveBlock, HSixBlock)

    def render_h_one_block(self, token):
        return f'<div class="h1-block">{token.target}</div>'

    def render_h_two_block(self, token):
        return f'<div class="h2-block">{token.target}</div>'

    def render_h_three_block(self, token):
        return f'<div class="h3-block">{token.target}</div>'

    def render_h_four_block(self, token):
        return f'<div class="h4-block">{token.target}</div>'

    def render_h_five_block(self, token):
        return f'<div class="h5-block">{token.target}</div>'

    def render_h_six_block(self, token):
        return f'<div class="h6-block">{token.target}</div>'