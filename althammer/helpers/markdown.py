from mistletoe.span_token import SpanToken
from mistletoe.block_token import BlockToken
from mistletoe.html_renderer import HTMLRenderer
import re

class Keyword(SpanToken):

    pattern = re.compile(r"\+((\[|\b).{3,25}?(\]|\b))\+")
    parse_inner = False

    def __init__(self, match_obj):
        self.target = match_obj.group(1)

class HBlock(BlockToken):

    start_pattern = re.compile(r"^#{1,6} ")

    @classmethod
    def start(line):
        return bool(re.match(line, self.start_pattern))





class CustomRenderer(HTMLRenderer):

    def __init__(self, *args, **kwargs):
        super().__init__(Keyword, *args, **kwargs)

        for i in kwargs:
            self.__dict__[i] = kwargs[i]

    def render_keyword(self, token):
        return f'<span class="keyword">{token.target}</span>'

class NumberedRenderer(CustomRenderer):

    def __init__(self, **kwargs):
        super().__init__(HBlock)

    def render_h_block(self, lines):
        return f'{lines[0]}<div class="ms-3">{'\n\n'.join(lines[1:])}</div>'