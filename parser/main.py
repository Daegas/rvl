import argparse
from bible_1909_parser import Bible1909Parser


def main():
    parser = argparse.ArgumentParser(prog='rvl1909', description='Analizador Sintáctico')
    parser.add_argument('--rv1909', help='Analiza la versión de 1909', action='store_true')
    args = parser.parse_args()
	
    if args.rv1909:
        parser = Bible1909Parser()
        parsed_data = parser.get_parsed_bible()



if __name__ == '__main__':
    main()