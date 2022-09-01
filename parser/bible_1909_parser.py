import re
import json
import itertools
from slugify import slugify
from base_parser import BaseParser

class Bible1909Parser(BaseParser):
	
	def __init__(self, source):
		super(Bible1909Parser, self).__init__(source)
		self._processable_content = self._cleaned_content

	

