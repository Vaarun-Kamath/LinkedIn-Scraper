from selenium import webdriver
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

load_dotenv() # Loads the environment variables
init_colorama() # Initializes the colorama instance


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
        print("Failed to wait for element")
        return False
    print(Fore.GREEN + successMessage + Style.RESET_ALL )
    return True


# Given email address and password, function will login to LinkedIn
def loginLinkedIn(email, password):

    browser.get('https://www.linkedin.com/')
    # Waits for element to load
    while(not waitFor('LinkedIn: Log In or Sign Up', browser.title," LinkedIn page loaded successfully ",refreshOnFail = True)):
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


def scrapeEmail():
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
    df.to_csv('CompanyDataFalse.csv',index = False)
    df.to_csv('CompanyDataTrue.csv',index = True)
        # break

browser = webdriver.Firefox()


while True:
    print("(c): Scrape Companies on Glassdoor")
    print("(l): Login to LinkedIn")
    print("(s): Scrape Emails on LinkedIn ")
    print("(q): Quit")
    choice = input(": ")
    if choice == 'q':
        break
    elif choice == 's':
        scrapeEmail()
    elif choice == 'c':

        scrapeCompanies()
    elif choice == 'l':
        loginLinkedIn(env('LINKEDIN_MAIL'),env('LINKEDIN_PASS'))
    else:
        print("Unknown choice")

browser.quit()
quit()