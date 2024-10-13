from mistletoe.span_token import SpanToken
from mistletoe.block_token import BlockToken, tokenize
from mistletoe.html_renderer import HTMLRenderer
import re

class Keyword(SpanToken):

    pattern = re.compile(r"\+((\[|\b).{3,25}?(\]|\b))\+")
    parse_inner = False

    def __init__(self, match_obj):
        self.target = match_obj.group(1)

class HBlock(BlockToken):

    start_pattern = re.compile(r"^#{1,6} ")

    def __init__(self, match):
        self.children = [match[0]]+tokenize(match[1:])

    @classmethod
    def start(cls, line):
        return bool(re.match(cls.start_pattern, line))

    @classmethod
    def read(cls, lines):
        #Reads lines until encountering an equal or higher heading
        child_lines=[next(lines)]
        hash_count = str(len(child_lines[0].split()[0]))
        end_pattern = re.compile(r"^#{1,"+hash_count+r"} ")

        for line in lines:
            if re.match(end_pattern, line):
                break
            child_lines.append(line)

        return child_lines #[child_lines[0]]+tokenize(child_lines[1:])

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

    def render_h_block(self, token):

        header = token.children[0]
        tier = len(header.split()[0])
        header = header.lstrip("#")
        header = header.lstrip()

        output = f'<h{tier}>{header}</h{tier}><div class="h-block">'
        for line in token.children[1:]:
            output += str(line)

        output += "</div>"
        return output