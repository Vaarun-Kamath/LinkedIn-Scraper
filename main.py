from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.chrome.service import Service
from colorama import Fore, Back, Style
from colorama import init as init_colorama
import time
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
from datetime import datetime
from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx
register_path = r'Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice'
with OpenKey(HKEY_CURRENT_USER, register_path) as key:
    print(QueryValueEx(key, 'ProgId'))

load_dotenv() # Loads the environment variables
init_colorama() # Initializes the colorama instance

linkedInLoggedIn = False
chromedriver = "C:/Users/Adhesh/Desktop/heknite/Email-Scraper/Webdrivers/chromedriver"


# binary = FirefoxBinary('/path/to/firefox/binary')


# Given variable name returns the value in .env
def env(var: str) -> str:
    try:
        return os.environ[var]
    except Exception as e:
        print(Fore.RED + f" {var}" + Style.RESET_ALL + " is not in the environment")
        quit()

def waitFor(text:str, element,successMessage = '',refreshOnFail = False) -> bool:
    try:
        assert text in element
    except AssertionError as a:
        if refreshOnFail:
            browser.refresh()
            print(Fore.RED + "Refresing browser" + Style.RESET_ALL)
            time.sleep(1)
        print("❌ "+"Waiting for page load...")
        return False
    print(Fore.GREEN + "✅ " + successMessage + Style.RESET_ALL )
    return True


# Given email address and password, function will login to LinkedIn
def loginLinkedIn(email, password):
    global linkedInLoggedIn
    browser.get('https://www.linkedin.com/')
    # Waits for element to load
    while(not waitFor('LinkedIn: Log In or Sign Up', browser.title,"LinkedIn page loaded successfully ",refreshOnFail = True)):
        continue
    # loginLinkedIn(env('LINKEDIN_MAIL'),env('LINKEDIN_PASS'))
    email_input = browser.find_element(By.XPATH,'//*[@id="session_key"]')
    pass_input = browser.find_element(By.XPATH,'//*[@id="session_password"]')
    login_button = browser.find_element(By.XPATH,'/html/body/main/section[1]/div/div/form/div[2]/button')

    email_input.send_keys(email)
    pass_input.send_keys(password)

    # assert email in email_input.get_attribute('value')
    waitFor(email, email_input.get_attribute('value'),"Entered credentials successfully")

    login_button.click()
    while(not waitFor('Feed | LinkedIn', browser.title,"Logged in on LinkedIn",refreshOnFail = True)):
        continue

    linkedInLoggedIn = True

# https://www.linkedin.com/company/google/people/?facetGeoRegion=102713980&keywords=HR
def scrapeCompanyLink():
    if not linkedInLoggedIn:
        print(Fore.RED + "\n❌ To scrape emails you need to be logged in on LinkedIn\n" + Style.RESET_ALL)
        return
    df = pd.read_csv('Datasets/Dataset.csv')

    companies = list(df['CompanyName'])
    searchBar = browser.find_element(By.XPATH,'/html/body/div[5]/header/div/div/div/div[1]/input')
    companyLinks = []
    companyIds = []
    txtsave = "companies.txt"
    errorlogsave = f"ErrorLogs_{datetime.now().strftime('%d_%m_%Y %H-%M-%S')}_.txt"
    f = open(errorlogsave, "w")
    f.close()
    for company in companies:
        searchBar.send_keys(Keys.CONTROL + 'a' + Keys.BACKSPACE)
        searchBar.send_keys(company)
        searchBar.send_keys(Keys.ENTER)
        giveup = False
        giveUpMargin = 2000

        while(not waitFor(company, browser.title,f"LinkedIn search loaded successfully: {company}",refreshOnFail = False)):
            giveUpMargin -= 1
            if giveUpMargin == 0:
                giveup = True
                break
            continue
        if giveup:
            print(f"Given Up on {company}")
            companyLinks.append("Gave up")
            with open(txtsave, "a") as file:
                file.write(f"{company}:Gave up" + "\n")
            continue
        # Find required data from the webpage, If not found then fill with None
        try:
            searchResults = browser.find_element(By.XPATH,'/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div')
            links = searchResults.find_elements(By.TAG_NAME,'a')
            links = [link.get_attribute('href') for link in links if '/company/' in link.get_attribute('href')]
            companyIdValue = browser.find_element(By.XPATH,'/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/div/ul/li/div').get_attribute('data-chameleon-result-urn')
            if "company" not in companyIdValue:
                raise Exception(f"Company {company} not in SearchResult")
        except Exception as e:
            # f.close()
            print(f"Error at company {company}, Logs at: {errorlogsave}")
            with open(errorlogsave, "a") as file:
                file.write(f"{e}")
            companyLinks.append(None)
            companyIds.append(None)
            with open(txtsave, "a") as file:
                file.write(f"{company} : None" + "\n")
            time.sleep(3)
            os.system('cls')
            continue

        if links: # Maybe companyIdValue 
            print(f"{giveUpMargin}: [{companyIdValue}] : {company} : {links[0]}")
            companyLinks.append(links[0])
            companyIds.append(companyIdValue)
            with open(txtsave, "a") as file:
                file.write(f"[{companyIdValue}]: {company}: {links[0]}" + "\n")
        else:
            print(company," : None")
            companyLinks.append(None)
            companyIds.append(None)
            with open(txtsave, "a") as file:
                file.write(f"{company} : None" + "\n")
        os.system('cls')
        # break
    df['LinkedIn'] = companyLinks
    df.to_csv('CompanyLinkedIn.csv',index = False)
        # break
    print("Scraping email...")

def scrapeCompanies():
    pageno = 1
    n = -1
    while n%10 != 0:
        n = int(input("How many companies you want to scrape (order of 10): "))
    initTitle = "Companies & Reviews | Glassdoor"
    df = pd.DataFrame(columns=['CompanyName','Rating','Reviews','Salaries','Jobs','Location','Industry','Description'])
    while len(df) < n:
        address = f"""https://www.glassdoor.co.in/Reviews/index.htm?overall_rating_low=4&page={pageno}&locId=2940587&locType=C&locName=Bengaluru&filterType=RATING_OVERALL"""
        browser.get(address)
        while(not waitFor(initTitle, browser.title,f"Glassdoor Page:{pageno}: loaded successfully ",refreshOnFail = True)):
            continue
        results = browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div[1]/div[4]/div[2]').find_elements(By.CSS_SELECTOR,"[data-test='employer-card-single']")
        # print(results)
        # print(len(results))
        i = 1
        for card in results:
            try:
                companyName = card.find_element(By.CSS_SELECTOR, "[data-test='employer-short-name']")
                rating = card.find_element(By.CSS_SELECTOR, "[data-test='rating']")
                reviews = card.find_element(By.CSS_SELECTOR, "[data-test='cell-Reviews-count']")
                salaries = card.find_element(By.CSS_SELECTOR, "[data-test='cell-Salaries-count']")
                jobs = card.find_element(By.CSS_SELECTOR, "[data-test='cell-Jobs-count']")
                location = card.find_element(By.CSS_SELECTOR, "[data-test='employer-location']")
                industry = card.find_element(By.CSS_SELECTOR, "[data-test='employer-industry']")
                # Handling the case when the description element is missing
                try:
                    description = card.find_element(By.XPATH, ".//div/div[6]/div/p")
                    # print(Fore.LIGHTGREEN_EX + f"Description Found for {companyName.text} : {description.text.split(' ')[0]}" + Style.RESET_ALL)
                    
                except Exception as e:
                    description = None
                    print(Fore.LIGHTRED_EX + f"Error in getting description for {companyName.text}" + Style.RESET_ALL)
                df.loc[len(df)] = {
                    'CompanyName': companyName.text,
                    'Rating': rating.text,
                    'Reviews': reviews.text,
                    'Salaries': salaries.text,
                    'Jobs': jobs.text,
                    'Location': location.text,
                    'Industry': industry.text, # Set to None if industry is None
                    'Description': description.text if description else None  # Set to None if description is None
                }
            except Exception as e:
                # Handle the case when any of the required elements are missing
                print("Some elements not found. Skipping this entry.")
                continue
            # break
        print(f"Number of companies scraped: {len(df)}/{n}")
        pageno += 1
        # break

    print(len(df))
    print(df['Description'])
    df.to_csv('CompanyDataFalse.csv',index = False) # Change False to True to have index at start
        # break
if key == 'Opera GXStable' or 'Chrome':
    #brop='chrome_options'
    while True:
        bool_head = input("Do you want to run it headless? (y/n): ")
        chrome_options = Options()
        if bool_head.lower() == 'y':
            chrome_options.add_argument("--headless")
            browser = webdriver.Chrome(options = chrome_options)
            break
        elif bool_head.lower() == 'n':
            browser = webdriver.Chrome()
            break
        else:
            print("Enter only 'y' or 'n'!")
elif key == 'Firefox':
    #brop='chrome_options'
    while True:
        bool_head = input("Do you want to run it headless? (y/n): ")
        firefox_options = Options()
        if bool_head.lower() == 'y':
            firefox_options.add_argument("--headless")
            browser = webdriver.Firefox(options = firefox_options)
            break
        elif bool_head.lower() == 'n':
            browser = webdriver.Firefox()
            break
        else:
            print("Enter only 'y' or 'n'!")
else:
    while True:
        bool_head = input("Do you want to run it headless? (y/n): ")
        firefox_options = Options()
        if bool_head.lower() == 'y':
            firefox_options.add_argument("--headless")
            browser = webdriver.Edge(options = firefox_options)
            break
        elif bool_head.lower() == 'n':
            browser = webdriver.Edge()
            break
        else:
            print("Enter only 'y' or 'n'!")

    



while True:
    if env('AUTO_LOGIN'):
        print(Fore.RED + "\nAuto-login enabled. Logging in..." + Fore.LIGHTBLACK_EX + "\nTo disable auto login, change environment variable AUTO_LOGIN to False.\n" + Style.RESET_ALL)
        loginLinkedIn(env('LINKEDIN_MAIL'),env('LINKEDIN_PASS'))
    if not linkedInLoggedIn:
        print("(l): Login to LinkedIn")
    
    print("(c): Scrape Companies on Glassdoor")
    print("(s): Scrape Company LinkedIn Links")
    print("(q): Quit")
    print("LinkedIn login status:","✅" if linkedInLoggedIn else "❌")
    choice = input(": ")
    if choice == 'q':
        break
    elif choice == 's':
        scrapeCompanyLink()
    elif choice == 'c':
        scrapeCompanies()
    elif choice == 'l':
        if not linkedInLoggedIn:
            loginLinkedIn(env('LINKEDIN_MAIL'),env('LINKEDIN_PASS'))
        else:
            print("Already logged in :)")
    else:
        print("Unknown choice")

browser.quit()
quit()
