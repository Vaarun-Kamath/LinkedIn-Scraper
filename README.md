# LinkedIn and Glassdoor Data Scraper
This Python script is designed to scrape data from both LinkedIn and Glassdoor. It provides a versatile toolset for collecting information on companies and their LinkedIn profiles, as well as scraping company data from Glassdoor. The script utilizes Selenium for web automation and Pandas for data handling.

## Features
### LinkedIn Scraper
- **Login Functionality:** The script allows you to log in to your LinkedIn account automatically using your email and password, or manually if needed.
- **Company LinkedIn Links:** It can scrape LinkedIn links for a list of companies. You can provide a CSV file containing company names to scrape their LinkedIn links. The script searches for companies on LinkedIn and retrieves their profile links.
### Glassdoor Scraper
- **Company Data Scraping:** This feature scrapes company data from Glassdoor. You can specify how many companies you want to scrape, and the script will fetch details such as company name, rating, reviews, salaries, jobs, location, industry, and description.


## Disclaimer
- **Use with Caution:** This script is intended for educational purposes and should be used responsibly and in compliance with the terms of service of the websites you scrape.

- **Account Verification:** Using this script multiple times on the same LinkedIn account might trigger LinkedIn's security measures, such as CAPTCHA challenges and other methods to verify your identity. Use this script carefully and only when you are confident that it will work without raising suspicion.

- **Respect Usage Policies:** Always respect the websites' robots.txt files and usage policies when scraping data.


## Usage
1. Environment Setup: Before using the script, ensure that you have set the necessary environment variables for LinkedIn login (LINKEDIN_MAIL and LINKEDIN_PASS) in a .env file.
2. Auto-login: You can enable auto-login by setting the AUTO_LOGIN environment variable to True. This allows the script to log in to your LinkedIn account automatically.
3. LinkedIn Scraper: Use option (s) to scrape LinkedIn company links. Provide a CSV file with a list of company names, and the script will search for them on LinkedIn and retrieve their profile links.
4. Glassdoor Scraper: Use option (c) to scrape company data from Glassdoor. Specify how many companies you want to scrape, and the script will fetch relevant details for each company.

## Dependencies
- Selenium: Used for web automation.
- Pandas and NumPy: Used for data handling and manipulation.
- Colorama: Provides colorful console output for better readability.
- Dotenv: Loads environment variables from a .env file.

## Output
- The script generates two CSV files for Glassdoor data: "CompanyDataFalse.csv" and "CompanyDataTrue.csv." The former has the index column disabled, while the latter includes it.
- For LinkedIn scraping, the script creates a CSV file named "CompanyLinkedIn.csv" containing the LinkedIn profile links for the scraped companies.

## Prerequisites
- You need to have Firefox installed and provide the path to the Firefox binary (commented out in the code) if you're using Firefox. Alternatively, you can adapt the script to use other browsers by changing the WebDriver.
- Ensure that you have installed all the required Python packages mentioned in the script.

## Disclaimer
This script is intended for educational purposes and should be used responsibly and in compliance with the terms of service of the websites you scrape. Always respect the websites' robots.txt files and usage policies.

## Authors
Varun Kamath

## License
This project is licensed under the MIT License - see the LICENSE file for details.
