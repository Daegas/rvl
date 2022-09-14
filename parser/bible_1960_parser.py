from base_parser import BaseParser
import pathlib
from bs4 import BeautifulSoup
from slugify import slugify
import json


class Bible1960Parser(BaseParser):

	RESULT_PATH = 'bible1960/'
	SOURCE = f'{pathlib.Path(__file__).parent.parent}/tmp/Reina_Valera_1960.xmm'
	FIRST_SLUG_NEW_TESTAMENT = 'mateo' #
	START_BOOKS = 0
	END_BOOKS = None           # Pick just n books -> get_raw_books()[1] None for all indexmateo = 39 indexapocalipsis=65
	START_CHAPTERS = None
	END_CHAPTERS = None     # Pick a few chapters activate sleep when removing None for all
	
	def __init__(self):
		super(Bible1960Parser, self).__init__(self.SOURCE, self.RESULT_PATH)

	def clean_content(self, content):
		return BeautifulSoup(content, "xml")

	def get_parsed_bible(self):
		parsed_bible = self.parse_books()
		return parsed_bible

	def parse_books(self):
		bible = {}

		new_testament = True if self.START_BOOKS > 39 else False
		book_number = self.START_BOOKS if self.START_BOOKS else 0

		for raw_book in self.get_raw_books()[self.START_BOOKS:self.END_BOOKS]:
			book = {}
			book['book_number'] = str(book_number)
			book['raw-name'] = raw_book.get('n')
			book['name'] = raw_book.get('n')
			book['slug'] = slugify(raw_book.get('n'))
			if self.FIRST_SLUG_NEW_TESTAMENT == book['slug']: new_testament = True
			book['testament'] = 'Nuevo Testamento' if new_testament else 'Antiguo Testamento'
			book['capitulos'] = self.get_chapters(raw_book)
			bible.update({book['slug'] : book})
			self.save_file(book)
			book_number += 1
			
		# return bible

	def get_raw_books(self):
		return self._content.find_all('b')

	def get_chapters(self, book_content):
		chapters = {}

		for chapter in book_content.find_all('c'):
			parsed = self.get_versicles(chapter)
			chapters[chapter.get('n')] = parsed

		return chapters

	def get_versicles(self, chapter_content):
		versicles = {}

		for versicle in chapter_content.find_all('v'):
			versicles[versicle.get('n')] = versicle.get_text().strip()
		
		return versicles


