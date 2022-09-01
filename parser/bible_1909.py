import os
import json
import argparse
import shutil
from bible_1909_parser import Bible1909Parser

SOURCE = 'http://www.intratext.com/IXT/ESL0021/_INDEX.HTM'

def main():
    parser = argparse.ArgumentParser(prog='rvl1909', description='Analizador Sintáctico')
    parser.add_argument('--1909', help='Analiza la versión de 1909', action='store_true')
    args = parser.parse_args()
	
    parser = Bible1909Parser(SOURCE)
    parsed_data = parser.get_parsed_bible()

if __name__ == '__main__':
    main()