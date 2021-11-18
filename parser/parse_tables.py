'''
All the table specific parser to each component in the case document's html.
'''
from bs4 import BeautifulSoup
import pprint,logging,unicodedata

pp = pprint.PrettyPrinter(indent=2)

#Go through the defendants table and convert it to a dict type.
def parse_defendants(table):
    cache = []
    aliases = []
    for i,row in enumerate(table.find_all('tr')):
        for j,cell in enumerate(row.find_all('td')):
            text = cell.text.strip()
            if text == '': continue
            if i == 0:
                cache.append([text,None])
            elif i == 1:
                cache[j][1] = text
            else:
                aliases.append(text.replace('ALIAS: ','').title())
    output = dict(cache)
    output['aliases'] = aliases
    return output

#Go through the status table and collect all info into a dict.
def parse_status(table):
    output = {}
    key = None
    for i,row in enumerate(table.find_all('tr')):
        for j,cell in enumerate(row.find_all('td')):
            text = cell.text.strip()
            if key is None and text=='': continue
            elif key is None:
                key = text
            else:
                output[key] = text
                key = None

    #There are two seperate tables for the status section.
    #Get & parse next table
    table = table.find_next_sibling('table')
    prefix = ""
    cache = []
    count = 0
    for i,row in enumerate(table.find_all('tr')):
        for j,cell in enumerate(row.find_all('td')):
            text = cell.text.strip()
            if j==0 and i%2==0:
                #Title Cell
                prefix = text
            elif j==0 and i%2==1:
                #Empty Cell
                continue
            elif i%2==0:
                #Header
                cache.append([f'{prefix}_{text}',None])
            else:
                #Values
                cache[count][1] = text
                count += 1
    output.update(dict(cache))
    return output

#A dict of two lists of dictionaries
def parse_charges(table):
    if table is None: return None
    output = {}
    title = None
    columnTitles = []
    for i,row in enumerate(table.find_all('tr')):
        cells = row.find_all('td')
        if len(cells) == 1:
            #If there is only one cell its a title
            text = cells[0].text.strip()            
            title = text
            output[title] = []
            columnTitles = []
        elif len(cells) > 1:
            values = [cell.text.strip() for cell in cells]
            if len(columnTitles) == 0:
                columnTitles = values
            else:
                output[title].append({k:v for k,v in zip(columnTitles,values)})
    return output

#Parsing probation
def parse_probation(table):
    if table is None: return None
    if table.find('table') is None:
        return table.text
    else:
        logging.error("Parsing probation has not been setup yet!")
        logging.error("Please send this html document to William!")
    return table

#Parse other cases; simple table with columns.
def parse_other_cases(table):
    if table is None: return None
    output = []
    titles = []
    #Cleaning when converting Latin encoding to UTF-8.
    clean = lambda cell: unicodedata.normalize("NFKD", cell.text.strip())
    for i,row in enumerate(table.find_all('tr')):
        cells = row.find_all('td')
        values = [clean(cell) for cell in cells]
        if len(titles) == 0:
            titles = values
        else:
            output.append({k:v for k,v in zip(titles,values)})
    return output
    
    
#Parsing the actions and minutes section
def parse_actions_minutes(table):
    if table is None: return None
    table = table.find_next_sibling('table')
    output = []
    titles = []
    
    #Cleaning when converting Latin encoding to UTF-8.
    clean = lambda cell: unicodedata.normalize("NFKD", cell.text.strip())
    for i,row in enumerate(table.find_all('tr')):
        #Get minuites row
        if len(row.find_all('input')) > 0: continue
        
        cells = row.find_all('td')
        values = [clean(cell) for cell in cells]
        if len(titles) == 0:
            titles = values
        elif values[0]=='':
            continue #Some empty rows
        else:
            output.append({k:v for k,v in zip(titles,values)})
    return output

def parse_fine_information(table):
    if table is None: return None
    output = {}
    key = None
    for i,row in enumerate(table.find_all('tr')):
        for j,cell in enumerate(row.find_all('td')):
            text = cell.text.strip()
            if key is None and text=='': continue
            elif key is None:
                key = text
            else:
                output[key] = text
                key = None

    
    #There are two seperate tables for the status section.
    #Get & parse next table
    table = table.find_next_sibling('table')
    outputs = []
    titles = []
    #Cleaning when converting Latin encoding to UTF-8.
    clean = lambda cell: unicodedata.normalize("NFKD", cell.text.strip())
    rows = table.find_all('tr')
    for i,row in enumerate(rows):
        cells = row.find_all('td')
        values = [clean(cell) for cell in cells]
        if i+1 == len(rows):
            #Last row/total
            titles = titles[-3:]
            values = values[1:]
            for title,value in zip(titles,values):
                output[f'total_{title.replace(" ","_")}'.lower()] = value
        elif len(titles) == 0:
            titles = values
        else:
            outputs.append({k:v for k,v in zip(titles,values)})
    output['fines'] = outputs
    return output

