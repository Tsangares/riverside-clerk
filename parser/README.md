# Dependencies

You must install beautiful soup, either:

    pip install -r requirements.txt
	
or 

    pip install bs4

# Quickstart

The file `parser.py` is executable using either,

    python parser.py filename.html
	
or just

    ./parser.py filename.html

Will output the parsed html file.

# Parse a directory

You can parse a whole directory by passing a directory full of `htm` or `html` files into it, and giving and output directory to put json files. Here is an exmaple where all the html files are in `data/output`. The path `data/json` will be created if it is not there.

    python parser.py data/output data/json
	
## Mutliprocessing

To multiprocess a directory the parsing just pass the number of processors,

	python parser.py data/output data/json --processors 8

## Write to file

To write to a file use

    python parser.py filename.html output.json

to write the content to a file.

# Summary

The parser is both a command line utility and also a libaray. The file `parser.py` is the main entry to the file and `parser_tables.py` has all the functions used to parse each specific table section. Currently the parser outputs json format files. The file `parser.py` will parse the page looking for the appropriate parsers located in `parser_tables.py` for each table found. Currently parsing the tables:

 - Defendants
 - Status
 - Charges
 - Probation
 - Cases
 - Actions & Minutes
 - File Information
 
*WARNING:* Currently the code is skipping the section "Related Cases On Calendar" and the section "Probation" needs to be fixed for proper use.
