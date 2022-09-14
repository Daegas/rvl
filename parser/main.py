import argparse
from bible_1909_parser import Bible1909Parser
from bible_1960_parser import Bible1960Parser


def main():
    parser = argparse.ArgumentParser(description='Analizador Sintáctico')

    parser.add_argument('--rv1909', help='Analiza la versión de 1909', action='store_true')
    parser.add_argument('--rv1960', help='Analiza la versión de 1960', action='store_true')
    args = parser.parse_args()
	
    if args.rv1909:
        parser = Bible1909Parser()
        parsed_data = parser.get_parsed_bible()
    elif args.rv1960:
        parser = Bible1960Parser()
        parsed_data = parser.get_parsed_bible()
    else:
        parser.print_help()



if __name__ == '__main__':
    main()