#!/usr/bin/env python3
'''
Parser for Riverside case project.
'''
from bs4 import BeautifulSoup
from parse_tables import *
import pprint,json
import pandas as pd
import glob

pp = pprint.PrettyPrinter(indent=2)

def parse_case_document(html):
    #if html is a filename, open & read content
    if '.htm' in html.lower(): html=open(html).read()

    #open parser
    soup = BeautifulSoup(html,'html.parser')

    #All the titles are font objects
    fonts = soup.find_all('font')

    #Find title text in font objects
    find_text_in_fonts = lambda text: next(iter([obj for obj in fonts if text in obj.text]),None)

    #Shift from title to table below
    shift = lambda element: element.parent.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling

    #Extract title text from a given title keyword.
    get_title = lambda title: find_text_in_fonts(title).text

    #Extract the content from a given title keyword.
    get_content = lambda title: shift(find_text_in_fonts(title))

    #Parse through each section formatting them into dictionaries per table
    return {
        'title': get_title('- Defendants').split('-')[0].strip(),
        'defendants': parse_defendants(get_content('- Defendants')),
        'status': parse_status(get_content('- Status')),
        'charges': parse_charges(get_content('- Charges')),
        'probation': parse_probation(get_content('- Probation')),
        'cases': parse_other_cases(get_content('- All of Defendant')),
        'actions_minutes': parse_actions_minutes(get_content('- Actions & Minutes')),
        'fine_information': parse_fine_information(get_content('- Fine Information'))
    }


#If run from cli
if __name__ == "__main__":
    #Implement cli arguments
    import argparse 
    parser = argparse.ArgumentParser(description='Parse case documents from Riverside.')
    parser.add_argument("parse",help="Ignore this ")
    parser.add_argument("--filename",type=str,help="The input file to parse.")
    parser.add_argument("--output",type=str,help="Output json file to save to.",default=None)
    #parser.add_argument("--distance",action="store_true", help="Annotate distance")
    args = parser.parse_args()
    print(args)

    #Parse given html file & run parser
    files = glob.glob(args.filename + '*')
    out = []
    for fn in files:
        html = open(fn,encoding="ISO-8859-1").read()
        html = unicodedata.normalize("NFKD", html)
        print(len(out))
        data = parse_case_document(html)
        out.append(data)

    df = pd.DataFrame(out)
    if args.output is not None:
        outFilename = args.output
        if '.csv' not in outFilename.lower():
            outFilename += '.csv'
        pd.to_csv(outFilename, index=False, encodint='utf8')
    else:
        pp.pprint(data)
    

    
