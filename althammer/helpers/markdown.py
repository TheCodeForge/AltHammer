from mistletoe.span_token import SpanToken
from mistletoe.html_renderer import HTMLRenderer
import re

class Keyword(SpanToken):

    pattern = re.compile(r"\+[\[\b](.{3,25})[\]\b]\+")
    parse_inner = False

    def __init__(self, match_obj):
        self.target = match_obj.group(1)


class CustomRenderer(HTMLRenderer):

    def __init__(self, **kwargs):
        super().__init__(Keyword)

        for i in kwargs:
            self.__dict__[i] = kwargs[i]

    def render_keyword(self, token):
        return f'<span class="keyword">{token.target}</span>'