from base_parser import BaseParser


class Bible1909Parser(BaseParser):

	RESULT_PATH = 'bible1090/'
	SOURCE = 'http://www.intratext.com/IXT/ESL0021/_INDEX.HTM'
	
	def __init__(self):
		super(Bible1909Parser, self).__init__(self.SOURCE, self.RESULT_PATH)

	

