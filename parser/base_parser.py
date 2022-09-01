from dbm import dumb
import re
import json
from time import sleep
from utils import *
from slugify import slugify
from sys import flags
from get_contents import GetContents

class BaseParser(GetContents):

    BOOKS_REGEX = r'<book>.+?</book>'

    _replacements = {
		'books': {
			'regex': r'<li><font size=2>(.[^<]*)</font>',
			'replacement': '<book>\\1</book>',
			'flags': 0,
		},
        'accents': {
            'regex': r'&([aeiou])acute;',
            'replacement': '\\1',
            'flags': re.IGNORECASE
        },
        'extra-info': {
            'regex': r'<hr\swidth=50%\ssize=1\salign=left>',
            'replacement': '',
            'flags': 0
        }
    }

    def clean_content(self, content):
        for key, data in self._replacements.items():
            content = re.sub(data['regex'], data['replacement'], content, 0, data['flags'])

        return content

    def get_parsed_bible(self):
        parsed_bible = self.parse_books()
        # print(parsed_bible)

        return parsed_bible

    def parse_books(self):
        book = {
            'name': '',
            'raw-name': '',
			'capitulos': []
		}

        for raw_book in self.get_raw_books()[1]:
            book['raw-name'] = raw_book
            book['name'] = re.sub('(<[^<]+?>)|;|,', '', raw_book)
            book['slug'] = slugify(book['name'])
            book['capitulos'] = self.get_chapters(raw_book)
            # dump(book)

    def get_raw_books(self):
        return re.findall(self.BOOKS_REGEX, self.cleaned_content())
    
    def get_chapters(self, book):
        versicles = []
        regex = r'{}\s*<ul\stype=square><li><font\ssize=1>\s*(.*?)(?=<br><br>)'.format(re.escape(book))
        versicle_link = re.search(regex, self._processable_content, re.DOTALL | re.IGNORECASE)
        if versicle_link:
            versicle_link = versicle_link.group(0)
            parts = re.split(r'<a\shref=',versicle_link)[1:]
            self._processable_content = self._processable_content.replace(versicle_link, '')
            for i in range(0, len(parts)):
                parsed = self.parse_versicles(parts[i], book)
                versicles.append(parsed)
        # else:
        #     if 'children' not in heading:
        #         print('Articles not found for {}\nRegexp: {}\nContent: {}'.format(dump(heading), regex, self._processable_content))
        return versicles
    
    def parse_versicles(self, versicle_url, book):
        versicle_url = 'http://www.intratext.com/IXT/ESL0021/' + re.sub('>\d+</a>\.', '', versicle_url)
        sleep(3)
        # response = GetContents.get_response(self, versicle_url, 1).text
        # print('RESPONSE:' , versicle_url, "\n", response)
