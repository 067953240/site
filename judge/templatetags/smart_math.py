from HTMLParser import HTMLParser
from django.template import Node, Library, Variable, FilterExpression, TemplateSyntaxError
import math
import re
import logging

register = Library()

CGI_BIN = 'http://www.forkosh.com/mathtex.cgi'

template = r'''
<span>
    <img src="%s?\1"/>
    <span style="display:none">~\1~</span>
</span>
''' % CGI_BIN


@register.filter(name='smart_math', is_safe=True)
def math(page):
    class MathHTMLParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.new_page = ''
            self.data_buffer = ''

        def handle_starttag(self, tag, attrs):
            self.new_page += '<' + tag + ' '.join('%s="%s"' % p for p in attrs.iteritems()) + '>'

        def handle_endtag(self, tag):
            self.new_page += re.sub('~(.*?)~', template, self.data_buffer)
            self.data_buffer = ''
            self.new_page += '<' + tag + '>'

        def handle_data(self, data):
            self.data_buffer += data

    parser = MathHTMLParser()
    parser.feed(page)
    return parser.new_page