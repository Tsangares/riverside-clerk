# Dependencies

You must install beautiful soup, either:

    pip isntall -r requirements.txt
	
or 

    pip install bs4

# Quickstart

The file `parser.py` is executable using either,

    python parser.py filename.html
	
or just

    ./parser.py filename.html

Will output the parsed html file.

## Write to file

To write to a file use

    python parser.py filename.html output.json

to write the content to a file.

# Summary

Currently the parser outputs json format files. The file `parser.py` will parse the page looking for the appropriate parsers located in `parser_tables.py` for each table found. Currently parsing the tables:

 - Defendants
 - Status
 - Charges
 - Probation
 - Cases
 - Actions & Minutes
 - File Information
 
*WARNING:* Currently the code is skipping the section "Related Cases On Calendar" and the section "Probation" needs to be fixed for proper use.