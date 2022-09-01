import os
import sys
import html
import requests
import hashlib
import pathlib
import pickle

class GetContents(object):
	CACHE_PATH = f'{pathlib.Path(__file__).parent.parent}/tmp/response-cache'

	def __init__(self, source):
		self._source = source
		self._response = self.get_response(self._source)
		self._content = self._response.text
		# self._content = html.unescape(self._response.text) 
		self._cleaned_content = self.clean_content(self._content)
		self._processable_content = self._cleaned_content

	def get_response(self, url, retries=5):
		if self.get_response_from_cache(url):
			print(f'Working with cached version')
			return self.get_response_from_cache(url)

		try:
			response = requests.get(url)
			self.cache_response(url, response)
		except requests.exceptions.Timeout:
			if retries:
				return get_response(url, retries - 1)
		except requests.exceptions.RequestException as e:
			print(f'Invalid reponse for {self._source}:\n{e}')
			sys.exit(1)

		return response

	def cache_response(self, url, response):
		try:
			pathlib.Path(self.CACHE_PATH).mkdir(parents=True, exist_ok=True)
			key = hashlib.md5(url.encode('utf-8')).hexdigest()
			file = pathlib.Path(f'{self.CACHE_PATH}/{key}.data')
			file.write_bytes(pickle.dumps(response))
		except OSError as e:
			print(f'Error when caching {url}\nException: {e}')

	def get_response_from_cache(self, url):
		key = hashlib.md5(url.encode('utf-8')).hexdigest()
		file = pathlib.Path(f'{self.CACHE_PATH}/{key}.data')
		
		return pickle.loads(file.read_bytes()) if file.exists() else ''

	def content(self):
		return self._content

	def cleaned_content(self):
		return self._cleaned_content

	def clean_content(self, content):
		raise NotImplementedError('clean_content() function must be implemented')

	def get_parsed_bible():
		raise NotImplementedError('get_parsed_bible() function must be implemented')