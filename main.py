from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from colorama import Fore, Back, Style
from colorama import init as init_colorama
import time
from dotenv import load_dotenv
import os

load_dotenv() # Loads the environment variables
init_colorama() # Initializes the colorama instance


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
    email_input = browser.find_element(By.XPATH,'//*[@id="session_key"]')
    pass_input = browser.find_element(By.XPATH,'//*[@id="session_password"]')
    login_button = browser.find_element(By.XPATH,'/html/body/main/section[1]/div/div/form/div[2]/button')

    email_input.send_keys(email)
    pass_input.send_keys(password)

    # assert email in email_input.get_attribute('value')
    waitFor(email, email_input.get_attribute('value'),"Entered credentials successfully")

    login_button.click()


def scrapeEmail():
    print("Enter Company Name")


browser = webdriver.Firefox()
browser.get('https://www.linkedin.com/')

# Waits for element to load
while(not waitFor('LinkedIn: Log In or Sign Up', browser.title," LinkedIn page loaded successfully ",refreshOnFail = True)):
    continue
    
# loginLinkedIn(env('LINKEDIN_MAIL'),env('LINKEDIN_PASS'))


while True:
    print("(s): Scrape Emails on LinkedIn ")
    print("(q): Quit")
    choice = input(": ")
    if choice == 'q':
        break
    elif choice == 's':
        scrapeEmail()

browser.quit()
quit()