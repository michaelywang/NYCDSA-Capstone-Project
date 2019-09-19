from selenium import webdriver
#from bs4 import BeautifulSoup # For HTML parsing
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter # Keep track of our term counts
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
import pandas as pd # For converting results to a dataframe and bar chart plots
from selenium.webdriver.common import action_chains, keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pickle
import re
import csv
import json
import os.path
#from collections import OrderedDict
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

## login credentials
email_addr = 'neeraj.somani4@gmail.com'
password = '*****'

def init_driver():
    ''' Initialize chrome driver'''

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    #chrome_options.add_argument('--user-data-dir=C:\\Users\\\\AppData\\Local\\Google\\Chrome\\User Data')
    ##chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    #browser = webdriver.Chrome(driver, chrome_options=chrome_options)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    #browser = webdriver.Chrome()

    return browser

def searchJobs(browser, jobName, city=None, jobDict = None):
    '''Scrape for job listing'''
    job = browser.find_element_by_id("sc.keyword")  #job title, keywords, or company
    location = browser.find_element_by_id("sc.location") #location search
    job.send_keys(jobName)  #type in job name in search
    #location form is already populated.
    location.clear()
    location.send_keys(city) #type in location name in search
    sleep(1)
    browser.find_element_by_class_name('gd-btn-mkt').click()
    sleep(3)
    
    # Find brief description
    for i in range(2): #20  ####&&&&
        try:
            print('this is value of i...', i)
            # Extract useful classes
            jobPosting =browser.find_elements_by_class_name('jl')
            sleep(3)

            # Create a job Dictionary. Every job in glassDoor has a unique data-id.
            # data-id should be used as key for the dictionary
            #create a map of 2-tuple. 2-tuple => data-id and selenium webElement.
            jobTuple = map(lambda a: (a.get_attribute('data-id'), a), jobPosting)
            
            # Filter picks out only those data-ids that are not in jobDict.keys()
            newPost = list(filter(lambda b: b[0] not in jobDict.keys(),jobTuple) ) #list of 2-tuple
            print('this is size of newPost', len(newPost))

            #If there are new posts, update job dict and link list
            if newPost != []:   
                           
                jobData = list(map(do_new_stuff, newPost))
                print('this is jobData', len(jobData))
                ##print('this is jobData after do_new_stuff', jobData)
                # Update job dictionary;
                # Convert tuple to dictionary. structure ('job_id',['rating',...]) -> {'job_id':['rating',...]}
                #print('updating jobDict')
                tmp = dict((a[0],a[1]) for a in jobData)
                #print('this is tmp', tmp)
                ##print('this is tmp after do_new_stuff', tmp)
                
                jobDict.update(tmp) #add a new entry with unique key job_id
                # finally find the links:
                print('this is before link_lst')

                link_lst = list(map(lambda c: (c[0],c[1].find_element_by_tag_name('a').\
                    get_attribute('href')), newPost))
                #add the link to job dict
                #print('Adding to link')
                print('i am after link_lst, its size is', len(link_lst))

                tmp = [jobDict[c[0]].append(c[1]) for c in link_lst]
                # update link list. This will be used in get_data part.
                #link += link_lst
                

            browser.find_element_by_class_name('next').click() #next page
            try:
                #browser.find_element_by_class_name('xBtn').click() #pop-up
                browser.find_element_by_xpath('//*[@id="JAModal"]/div/div[2]/div/div[1]').click() #pop up
            except:
                pass

        except Exception as e:
            #pass
            print(type(e),e)

    return jobDict #, link

def text_cleaner(text):
    '''
    This function just cleans up the raw html.
    '''
    lines = (line.strip() for line in text.splitlines()) # break into lines
    #lines = [line.strip() for line in text.splitlines()]
    #print('this is lines - ', lines)
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
    #chunks = [phrase.strip() for line in lines for phrase in line.split("  ")]
    ##print('this is chunks - ', list(chunks))
    def chunk_space(chunk):
        chunk_out = chunk + ' ' # Need to fix spacing issue
        return chunk_out

    #print('Going for text!')
    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk) #.encode('utf-8') # Get rid of all blank lines and ends of line
    #print('this is text after encoding- ', text)
    #text = text.decode('unicode_escape').encode('ascii','ignore')

    '''
    # Now clean out all of the unicode junk (this line works great!!!)
    #print('cleaning out unicode junc from text!')
    try:
        #text = text.decode('unicode_escape').encode('ascii', 'ignore') # Need this as some websites aren't formatted    
    except:                                                            # in a way that this works, can occasionally throw
        return                                                         # an exception
    '''

    #print('getting rid of non-words from text!')
    #text = re.sub(b"[^a-zA-Z.+3]",b" ", text)  # Now get rid of any terms that aren't words (include 3 for d3.js)
                                                # Also include + for C++

    #print('make text lower case!')
    text = text.lower()  # Go to lower case

    #print('split text!')
    #text = text.split()  #  and split them apart

    
    #stopws = set(stopwords.words("english"))
    #print('removing stop words!')
    #text = [w for w in text if not w in stopws]
    


    #print('set of text')
    #text = list(set(text)) # Last, just get the set of these. Ignore counts
                           # we are just looking at whether a term existed or not on the website

    #print("We are done! Let's return it!")
    #print('this is final text....', text)
    return text

def do_new_stuff(a):
    if len(a) == 0:
        print('object is empty')
        return a

    tmp = a[1].text
    ##print('this is tmp in do_new_stuff', list(tmp))
    test = list(a[0], a[1].text.split('\n'))
   
    #rating = test[0] if test[0]!='' else ''
    #company = test[1] if test[1]!='' else ''
    #position = test[2] if test[2]!='' else ''
    #job_city_state = test[3] if test[3]!='' else ''
    #sal_range = test[4] if test[4]!='' else ''
    
    return (a[0],test)

get_link = True
get_data = False ##(not get_link) # either get_link or get_data

website = "https://www.glassdoor.com/index.htm"

# Initialize the webdriver
browser = init_driver()
browser.get(website)
main_page = browser.current_window_handle
browser.find_element_by_class_name('google.gd-btn.short').click()
sleep(2)

# changing the handles to access login page 
for handle in browser.window_handles: 
    if handle != main_page: 
        email_login_page = handle 

# change the control to email signin page         
browser.switch_to.window(email_login_page)
email = browser.find_element_by_id("identifierId")
email.send_keys(email_addr)
browser.find_element_by_id('identifierNext').click()
sleep(2)

# changing the handles to access login page 
for handle in browser.window_handles: 
    if handle != main_page: 
        password_login_page = handle 

# change the control to password signin page         
browser.switch_to.window(password_login_page)

passw = browser.find_element_by_class_name('whsOnd.zHQkBf')
passw.send_keys(password)
browser.find_element_by_id('passwordNext').click()
sleep(1)
# change control to main page 
browser.switch_to.window(main_page)
sleep(2)
try:
    #browser.find_element_by_class_name('xBtn').click() #pop-up
    #browser.find_element_by_xpath('//*[@id="JAModal"]/div/div[2]/div').click() #pop up
    browser.find_element_by_xpath('//*[@id="close"]').click() # close pop up
except:
    pass
sleep(3)

#json_file = open('reviews.json', 'w', encoding='utf-8')
#writer = json.writer(json_file)

if get_link :
    jobDict = {}
    iter_num = 0

    while iter_num <1: # default 1 ####&&&&
        print('Starting iteration number {}'.format(iter_num))
        #sleep(get_pause())
        browser.get(website)

        # Initialize cities and jobs

        jobName_lst = ['Data Analyst'] ## , 'Data Analyst','Data Engineer'
        jobName = np.random.choice(jobName_lst)
        

        city_lst = ['Princeton, NJ'] ## ,'New York','San Francisco','Detroit','Washington','Austin','Boston','Seattle','Chicago',' ', 'San Jose','Los Angeles'
        city = np.random.choice(city_lst)

        print('jobName = '+jobName+ ', city = '+city)
        
        # search for jobs (short description)
        try:
            # jobDict structure {'job_id':['rating','position','company','salary']}
            update_jobDict = searchJobs(browser, jobName, city, jobDict)
            #sleep(get_pause())
        except Exception as e:
            print(type(e),e)
            sys.exit("Error message")
            #pass
        #print('this is update_jobDict ---', update_jobDict)

        finalDF = pd.DataFrame(list(update_jobDict.values()), columns=['job_id', 'rating', 'company_name', 'position', 'job_city_state', 'sal_range', 'link'])
        finalDF.to_json('linkData.json')
        iter_num += 1

    browser.close()
 # 5- Scrape the job description, for every link

if get_data:

    #print('len(link) = '+str(len(link)))
    #dataDF = pd.read_json('data.json')
    #tempDF = dataDF[['']]
    while len(link) > 0: # originally 0, a hard coded solution for when only bad links are left.
    #for i in range(2): # debugging ####&&&&
        try:
            rnd_job = np.random.choice(range(len(link)))
            #print(rnd_job)
            ids = link[rnd_job][0]
            page = link[rnd_job][1]
            #print(ids)
            #print(page)

            browser.get(page)
            sleep(3)

            # Extract text
            
            desc_list = browser.find_element_by_xpath('//*[@id="JobDescriptionContainer"]/div[1]').text
            #print('desc_list '+ str(type(desc_list)))
            description = text_cleaner(desc_list)
            #description = desc_list
            #print('this is desc after text cleaner', description)

            jobDict[ids].append(description)
            #remove links already used
            dummy=link.pop(rnd_job)

            # if everything is fine, save
            #print("Going to save data!!")
            save_obj(jobDict, 'glassDoorDict')
            save_obj(link, 'glassDoorlink')

            print('Scraped successfully ' + ids)
        except:
            print( ids + ' is not working! Sleep for 6 seconds and retry')
            print( 'Still missing ' + str(len(link)) + ' links' )
            sleep(6)
    print('Done for now!! len(link) = '+str(len(link)))
    browser.close()