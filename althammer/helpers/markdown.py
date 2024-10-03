from .get import *

from mistletoe.span_token import SpanToken
from mistletoe.html_renderer import HTMLRenderer
import os.path
import re

from flask import g

#preprocess re

enter_re=re.compile("(\n\r?\w+){3,}")



# add token/rendering for @username mentions


class Keyword(SpanToken):

    pattern = re.compile("\+\b(.{3,25})\b\+")
    parse_inner = False

    def __init__(self, match_obj):
        self.target = match_obj.group(1)


class CustomRenderer(HTMLRenderer):

    def __init__(self, **kwargs):
        super().__init__(Keyword)

        for i in kwargs:
            self.__dict__[i] = kwargs[i]

    def render_user_mention(self, token):
        space = token.target[0]
        target = token.target[1]

        return f'<span class="keyword">{target}</span>'