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

    parse_inner = True

    @staticmethod
    def start(line):
        return line.startswith("# ")

    @staticmethod
    def read(lines):
        line_buffer = [next(lines)]
        for line in lines:
            if line.startswith('#'):
                break
            line_buffer.append(line)
        return line_buffer

class HTwoBlock(HOneBlock):

    @staticmethod
    def start(line):
        return line.startswith("## ")

class HThreeBlock(HOneBlock):

    @staticmethod
    def start(line):
        return line.startswith("### ")

class HFourBlock(HOneBlock):

    @staticmethod
    def start(line):
        return line.startswith("#### ")

class HFiveBlock(HOneBlock):

    @staticmethod
    def start(line):
        return line.startswith("##### ")

class HSixBlock(HOneBlock):

    @staticmethod
    def start(line):
        return line.startswith("###### ")



class CustomRenderer(HTMLRenderer):

    def __init__(self, *args, **kwargs):
        super().__init__(Keyword, *args, **kwargs)

        for i in kwargs:
            self.__dict__[i] = kwargs[i]

    def render_keyword(self, token):
        return f'<span class="keyword">{token.target}</span>'

class NumberedRenderer(CustomRenderer):

    def __init__(self, **kwargs):
        super().__init__(HOneBlock, HTwoBlock, HThreeBlock, HFourBlock, HFiveBlock, HSixBlock)

    def render_h_one_block(self, lines):
        return f'{lines[0]}<div class="h1-block">{'\n\n'.join(lines[1:])}</div>'

    def render_h_two_block(self, lines):
        return f'{lines[0]}<div class="h2-block">{'\n\n'.join(lines[1:])}</div>'

    def render_h_three_block(self, lines):
        return f'{lines[0]}<div class="h3-block">{'\n\n'.join(lines[1:])}</div>'

    def render_h_four_block(self, lines):
        return f'{lines[0]}<div class="h4-block">{'\n\n'.join(lines[1:])}</div>'

    def render_h_five_block(self, lines):
        return f'{lines[0]}<div class="h5-block">{'\n\n'.join(lines[1:])}</div>'

    def render_h_six_block(self, lines):
        return f'{lines[0]}<div class="h6-block">{'\n\n'.join(lines[1:])}</div>'