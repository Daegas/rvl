
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-360/)

# Reina Valera Libre

Crea archivos _.json_ por cada libro de la biblia con la siguiente estructura:
```
{
  "raw-name": "<book>Ipsa</book>",
  "name": "Ipsa",
  "slug": "ipsa",
  "testament": "Antiguo Testamento",
  "capitulos": {
        "0": {
            "0": "Ipsa aut autem amet. "
        },
        "1": {
            "0": "Ipsa aut autem amet. ",
            "1": "Ipsa aut autem amet. "
        }
  }
}
```

## Uso
Para obtener Reina Valera 1909

`python3 parser/main.py --rv1909`

Esto creará los archivos .json en [/bibles/bible1909](/bibles/bible1909)
uno por cada libro

### [/parser](/parser)
Aquí  se encuentra la lógica del código

* [/parser/main.py](/parser/main.py) : Archivo pricipal
* [/parser/get_contents.py](/parser/get_contents.py) : 
Clase padre de _base_parser_ se encarga de hacer los requests y guardarlos en caché
* [/parser/base_parser.py](/parser/base_parser.py) : Es la clase padre de los parsers, genera los archivos .json
* [/parser/bible_1909_parser.py](/parser/bible_1909_parser.py) : Contiene variables que permiten parsear la versión 1909



