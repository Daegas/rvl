import re
import json
import pathlib
from utils import *
from slugify import slugify
from get_contents import GetContents

class BaseParser(GetContents):

    BOOKS_REGEX = r'<book>.+?</book>'
    FIRST_SLUG_NEW_TESTAMENT = 'mateo'
    START_BOOKS = 10
    END_BOOKS = None           # Pick just n books -> get_raw_books()[1]
    START_CHAPTERS = 0
    END_CHAPTERS = None     # Pick a few chapters activate sleep when removing None for all
    SLEEP = 5           #If isn't on caché waits n second to make the requests, to prevent weird activity detection 
    RESULT_ROOT_PATH = f'{pathlib.Path(__file__).parent.parent}/bibles/'

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
        'fix-n-tilde': {
            'regex': r'&ntilde;',
            'replacement': 'ñ',
            'flags': 0
        },
        'fix-n-tilde': {
            'regex': r'&deg;',
            'replacement': '',
            'flags': 0
        },
        'extra-info': {
            'regex': r'<hr\swidth=50%\ssize=1\salign=left>',
            'replacement': '',
            'flags': 0
        },
        'a-tags': {
            'regex': r'(<A.[^>]*>|</A>)',
            'replacement': '',
            'flags': 0
        },
        'numbers': {
            'regex': r'<p.[^>]*>\s*(\d+:\d+)\s*</p>',
            'replacement': '',
            'flags': 0
        },
        'versicles': {
            'regex': r'<p.[^>]*>\s*(.*?)\s*</p>',
            'replacement': '<versicle>\\1</versicle>',
            'flags': re.DOTALL
        },
        'chapters-names': {
            'regex': r'<h2>(.*?)</h2>',
            'replacement': '',
            'flags': 0
        },
		'empty-tags': {
			'regex': r'<versicle>(\s|&nbsp;)*</versicle>',
			'replacement': '',
			'flags': 0
		},
        'weird-spaces': {
            'regex': r'\r\n',
            'replacement': ' ',
			'flags': 0
        }
    }

    def clean_content(self, content):
        for key, data in self._replacements.items():
            content = re.sub(data['regex'], data['replacement'], content, 0, data['flags'])
        return content

    def get_parsed_bible(self):
        parsed_bible = self.parse_books()
        return parsed_bible

    def parse_books(self):
        book = {}

        new_testament = False
        for raw_book in self.get_raw_books()[self.START_BOOKS:self.END_BOOKS]:
            book['raw-name'] = raw_book
            book['name'] = re.sub('(<[^<]+?>)|;|,', '', raw_book)
            book['slug'] = slugify(re.sub(r'&.*?;', '', book['name']))
            if self.FIRST_SLUG_NEW_TESTAMENT == book['slug']: new_testament = True
            book['testament'] = 'Nuevo Testamento' if new_testament else 'Antiguo Testamento'
            book['capitulos'] = self.get_chapters(raw_book)
            self.save_file(book)
        
        return book

    def get_raw_books(self):
        return re.findall(self.BOOKS_REGEX, self._content)
    
    def get_chapters(self, book_content):
        chapters = {}
        regex = r'{}\s*<ul\stype=square><li><font\ssize=1>\s*(.*?)(?=<br><br>)'.format(re.escape(book_content))
        chapter_link = re.search(regex, self._content, re.DOTALL | re.IGNORECASE)

        if chapter_link:
            chapter_link = chapter_link.group(0)
            parts = re.split(r'<a\shref=', chapter_link)[1:]
            parts = parts[self.START_CHAPTERS:self.END_CHAPTERS]

            self._content = self._content.replace(chapter_link, '')
            for i in range(len(parts)):
                parsed = self.parse_chapters(self.SLEEP, parts[i], book_content)
                chapters[i] = parsed

        return chapters
    
    def parse_chapters(self, sleep, raw_chapter_url, book):
        source_root_path = self._source
        chapter_url = source_root_path.replace('_INDEX.HTM', '') + re.sub('>\d+</a>\.', '', raw_chapter_url).strip()
        response = GetContents.get_response(self, chapter_url, sleep_t=sleep).text
        chapter_content = self.clean_content(response)
        return self.get_versicles(chapter_content)

    def get_versicles(self, chapter_content):
        parts = re.findall(r'(?<=<versicle>).*?(?=</versicle>)', chapter_content, re.DOTALL)
        if len(parts) == 0:
            print(f'Vericles not found inside{chapter_content}\n')
            return parts

        return {i: parts[i] for i in range(len(parts))}
    
    def save_file(self,book):
        file_name = self.RESULT_ROOT_PATH + self._result_path + book['slug'] + '.json'
        try:
            book_file = pathlib.Path(file_name)

            if not book_file.parent.exists():
                book_file.parent.mkdir(parents=True)

            print(f'Writing file {book_file}')
            with open(book_file, 'w') as jsonfile:
                json.dump(book, jsonfile, indent=2)
                return True

        except Exception as e:
            print(f'Error with file: {book_file}\nException: {str(e)}')




