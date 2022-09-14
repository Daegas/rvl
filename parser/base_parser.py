import re
import json
import pathlib
from utils import *
from slugify import slugify
from get_contents import GetContents

class BaseParser(GetContents):
    
    def save_file(self,book):
        file_name = self.RESULT_ROOT_PATH + self._result_path + book['book_number'] + '_' + book['slug'] + '.json'
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




