#!/usr/bin/env python3
'''
Parser for Riverside case project.
'''
from bs4 import BeautifulSoup
from parse_tables import *
from itertools import repeat
from multiprocessing import Pool
import pprint,json,os,time,csv
import pandas as pd
import glob

pp = pprint.PrettyPrinter(indent=2)

def parse_case_document(html):
    if "500 - Internal server error." in html:
        return 500
    if 'Insufficient Security Settings' in html:
        return 403
            
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

#Returns true on a successful parse
def parseFile(filename,outPath=None):
    #Parse a single html file
    html = open(filename,encoding="ISO-8859-1").read()
    html = unicodedata.normalize("NFKD", html)
    try:
        data = parse_case_document(html)
        if data == 500:
            logging.warning(f"File has no contents [Error 500]: {filename}")
            return 500
        elif data == -1:
            logging.warning(f"Insufficient privileges [Error 403]: {filename}")
            return 403
    except Exception as e:
        logging.error(f"Failed on {filename}")
        return 1000
    if outPath is not None:
        if os.path.isdir(outPath):
            filename = '.'.join(filename.split('/')[-1].split('.')[:-1]+['json'])
            outPath= os.path.join(outPath,filename)
        elif '.json' not in outPath.lower():
            outPath += '.json'
        logging.info(f'Saving {outPath}')
        json.dump(data,open(outPath,'w+'),indent=2)
        #pd.DataFrame.to_csv(outFilename, index=False, encodint='utf8')
    else:
        pp.pprint(data)
    return True
    

#If run from cli
if __name__ == "__main__":
    #Implement cli arguments
    import argparse 
    parser = argparse.ArgumentParser(description='Parse case documents from Riverside.')
    parser.add_argument("input",type=str,help="Either a file or directory to parse")
    parser.add_argument("output",nargs='?',type=str,help="Either a file or directory to output files.",default=None)
    parser.add_argument("--processors",type=int,help="Use this many processes when multiprocessing.",default=1)
    args = parser.parse_args()
    outPath = args.output
    path = args.input
    #Parse given html file & run parser
    is_directory = os.path.isdir(path)
    if is_directory:
        #Parse a directory of html files
        if outPath is None:
            raise Exception("When parsing a directory an output path must be given.")
        
        files = [os.path.join(path,f) for f in os.listdir(path) if '.htm' in f.lower()]
        os.makedirs(outPath,exist_ok=True)
        with Pool(args.processors) as pool:
            success = pool.starmap(parseFile,zip(files,repeat(outPath)))

        #Write filed files to csv
        failed_files = [{'filename': filename,'error': error} for filename,error in zip(files,success) if error != True]
        with open(f'log_parser_{int(time.time())}.csv','w+') as f:
            writer = csv.DictWriter(f,fieldnames=['filename', 'error'])
            writer.writeheader()
            writer.writerows(failed_files)
    else:
        parseFile(path,outPath)
    
