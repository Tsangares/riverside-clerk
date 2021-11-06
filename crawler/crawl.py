################PREAMBLE######################################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pandas as pd
import glob

def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(options=chrome_options)
    return browser

configs = {line.split('=')[0]:line.split('=')[1].strip() for line in open('/opt/conf.env').readlines()}
BUCKET = configs['BUCKET']
FAILURE_SNS_TOPIC = configs['FAILURE_SNS_TOPIC']
PASSWORD = configs['PASSWORD']
USERNAME = configs['USERNAME']
FILENAME = configs['FILENAME']

#Load list of case numbers
# os.chdir(r"Z:\Claremont\Riverside Scraping")
df = pd.read_csv(FILENAME,skiprows=0, encoding = "ISO-8859-1")

def get_crawled_casenumbers():
    return [i.split('_')[1].split('.')[0] for i in glob.glob('/data/output/*.html')]

def get_errors():
    return [i.split('.')[0] for i in glob.glob('/data/errors/*.html')]



#List names
htmllist=[]

#Load the browser and log in
browser=get_browser()
browser.get('https://ecomm1.riverside.courts.ca.gov/')
login=browser.find_element_by_css_selector('body > div:nth-child(2) > div > form:nth-child(10) > table > tbody > tr:nth-child(1) > td:nth-child(2) > input[type=Text]')
browser.execute_script("arguments[0].scrollIntoView();", login)
login.clear()
login.send_keys(USERNAME)

password=browser.find_element_by_css_selector('body > div:nth-child(2) > div > form:nth-child(10) > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=password]')
browser.execute_script("arguments[0].scrollIntoView();", password)
password.clear()
password.send_keys(PASSWORD)
password.send_keys(Keys.ENTER)

#Go to search site
browser.get('https://public-access.riverside.courts.ca.gov/OpenAccess/CaseSearch.asp')

# for case in df[df['CourtNumber'].notnull()]['CourtNumber']:
for case in df[df['CourtNumber'].notnull()]['CourtNumber'].sample(frac=1):
    crawled_casenumbers = get_crawled_casenumbers()
    crawled_errors = get_errors()
    if case in crawled_casenumbers:
        print('%s already crawled, skipping' % case)
        continue
    if case in crawled_errors:
        print('%s already failed, skipping' % case)
        continue
    print(case)
    time.sleep(1)
    searchbar=browser.find_element_by_css_selector('#txtCaseNumber')
    searchbar.clear()
    searchbar.send_keys(case)
    searchbar.send_keys(Keys.ENTER)
    #Here, it may redirect me to the account page for whatever reason. If it does, proceed back to the search.
    try:
        continuebutton=browser.find_element_by_xpath("//*[@value='Continue to Public Access']")
        browser.execute_script("arguments[0].scrollIntoView();", continuebutton)
        Hover = ActionChains(browser).move_to_element(continuebutton)
        Hover.click().perform()  
    except:
        print("No continue button found.")
 
    #At this stage it shows the results. I get from the layout that in some cases, there may be more than one result. This may only be if name is searched by. Will double check with Greg.  
    try:
        caselink=browser.find_element_by_xpath("//*[text() = '%s']"%(case))
    except NoSuchElementException as e:
        open('/data/errors/%s.html' % case,'w').write(browser.page_source)
        print("Error with case %s" % case)
        continue
    browser.execute_script("arguments[0].scrollIntoView();", caselink)
    Hover = ActionChains(browser).move_to_element(caselink)
    #Clicking on the link will create a popup. Need to use window_handles to switch back and forth
    window_before = browser.window_handles[0] #Set ID for original window
    Hover.click().perform()
    window_after = browser.window_handles[1] #Set ID for popup window
    browser.switch_to.window(window_after) #Switch to popup
    
    html = browser.page_source
    text_file = open("/data/output/index_%s.html" %(case), "w")
    text_file.write(html)
    text_file.close()
    
    #Go back to original window and close other window
    browser.close()
    browser.switch_to.window(window_before)

    time.sleep(1)
    
    
    
    
    
