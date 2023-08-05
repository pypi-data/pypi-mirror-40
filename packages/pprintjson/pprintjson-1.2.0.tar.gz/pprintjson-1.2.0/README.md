# [pprintjson](https://pypi.org/project/pprintjson/)

[![PyPi release](https://img.shields.io/pypi/v/pprintjson.svg)](https://pypi.org/project/pprintjson/)
[![Downloads](https://pepy.tech/badge/pprintjson)](https://pepy.tech/project/pprintjson)

A json pretty printer for Python 🐍.

## Installation

```bash
$ pip install pprintjson
```

## Usage

```text

usage: pprintjson.py [-h] [-i num] [-o file] [-s str] [-v] [file]

A pretty-printing function for json.

positional arguments:
  file                    json <file> to pretty-print

optional arguments:
  -h, --help              show this help message and exit
  -i num, --indent num    indent <num> number of spaces at each level (default: 4)
  -o file, --output file  write output to <file> instead of stdout (default: stdout)
  -s str, --string str    json <str> to pretty-print
  -v, --version           show program's version number and exit

```

### Script

Pretty print JSON from a **file** using the `pprintjson` CLI.

```bash
$ pprintjson "./path/to/file.json"
```

Pretty print JSON from a **string** using the `pprintjson` CLI.

```bash
$ pprintjson -s '{ "a": 1, "b": "string", "c": true }'
```

Pretty print JSON from a **string** with an *indent* of **1**.

```bash
$ pprintjson -s '{ "a": 1, "b": "string", "c": true }' -i 1
```

Pretty print JSON from a **string** and save *output* to a file **output.json**.

```bash
$ pprintjson -s '{ "a": 1, "b": "string", "c": true }' -o ./output.json
```

### Module

Pretty print JSON from a **dict** using the `pprintjson` module.

```python

# 1. import the "pprintjson" function.
from pprintjson import pprintjson as ppjson

# 2. pretty print JSON.
obj = { "a": 1, "b": "string", "c": True }

ppjson(obj)
```

![stdout](https://raw.githubusercontent.com/clarketm/pprintjson/master/pprintjson.png)

## License

MIT &copy; [**Travis Clarke**](https://blog.travismclarke.com/)
