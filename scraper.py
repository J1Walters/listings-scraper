import time
import re
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from joblisting import JobListing
from selenium_config import load_selenium_driver
from sqlite_config import DATABASE_PATH

class Scraper:
    # Get Selenium driver
    driver = load_selenium_driver()

    def __init__(self, website):
        self.website = website

    def __get_soup(self, url):
        """Get the BeautifulSoup HTML from the given URL"""
        try:
            # Make connection to site and wait for loading
            Scraper.driver.get(url)
            time.sleep(5)
        except Exception as e:
            print(e)
            return None

        return BeautifulSoup(Scraper.driver.page_source, 'html.parser')

    def __get_links(self, soup):
        """Get a list of all the links from the given soup"""
        # Get HTML as BeautifulSoup object
        link_list = []

        # Add href to link_list if present
        for link in soup.find_all('a'):
            if 'href' in link.attrs:
                link_list.append(link.attrs.get('href'))

        return link_list
    
    def __get_next_page(self, soup):
        """Find the link to the next page in the given soup"""
        # For Gradcracker
        if self.website.name == 'Gradcracker':
            try:
                next_page = soup.find('a', rel='next').attrs.get('href')
            except Exception as e:
                print(e)
                return None
        # For Indeed
        elif self.website.name == 'Indeed':
            try:
                next_page = soup.select('a[data-testid="pagination-page-next"]')[0].attrs.get('href')
            except Exception as e:
                print(e)
                return None
        
        return next_page

    def __scrape_gradcracker(self, url, db_con):
        """Scrape from Gradcracker"""
        # Get list of all links on page
        try:
            soup = self.__get_soup(url)
        except Exception as e:
            print(e)
            return None

        link_list = self.__get_links(soup)
        next_page = self.__get_next_page(soup)
        
        # Filter list of links for job listings
        job_filter = re.compile(r'https:\/\/www\.gradcracker\.com\/.*\/graduate-job\/.*')
        filtered_list = list(filter(job_filter.match, link_list))
        # # DEBUG:
        # print(filtered_list)
        # print(next_page)

        # Visit job listing links and get the data we want
        for link in filtered_list:
            try:
                listing_soup = self.__get_soup(link)
            except Exception as e:
                print(e)
                listing_soup = None

            if listing_soup is not None:
                print('Found Job!')

                # Find job info in HTML
                try:
                    company = listing_soup.find('input', id=self.website.company_tag).attrs.get('value')
                except Exception:
                    company = 'NULL'

                try:
                    jobtitle = listing_soup.find(self.website.title_tag).get_text()
                except Exception:
                    jobtitle = 'NULL'

                try:
                    location = listing_soup.find('div', text=self.website.location_tag).parent.get_text()
                except Exception:
                    location = 'NULL'

                try:
                    pay = listing_soup.find('div', text=self.website.pay_tag).parent.get_text()
                except Exception:
                    pay = 'NULL'

                try:
                    desc = listing_soup.find('div', class_=self.website.desc_tag).get_text()
                except Exception:
                    desc = 'NULL'

                timestamp = datetime.now().date().isoformat()
            
                # Make instance of JobListing class and dump info to database
                job = JobListing(self.website.name, company, jobtitle, location, pay, desc, timestamp)
                job.dump_to_db(db_con)

                # # DEBUG
                # print(company, jobtitle, location, pay)
                # print(desc)
            
        # # DEBUG:
        # print(next_page)
        
        if next_page is not None:
            next_url = 'https://www.gradcracker.com' + next_page
            print('Moving to next page...')
            self.__scrape_gradcracker(next_url, db_con)

    def __navigate_to_indeed_jobs(self, url):
        """Navigates to the job listings on Indeed and returns the URL"""
        # Attempt to connect to url
        try:
            Scraper.driver.get(url)
            time.sleep(2)
        except Exception as e:
            print(e)
            return None

        # Reject cookies
        accept_cookies = Scraper.driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        accept_cookies.click()
        time.sleep(2)
        
        # Submit search term into search bar
        search_box = Scraper.driver.find_element(By.ID, 'text-input-what')
        submit_button = Scraper.driver.find_element(By.CLASS_NAME, 'yosegi-InlineWhatWhere-primaryButton')

        search_box.send_keys('technology')
        time.sleep(1)
        submit_button.click()
        
        # Filter to only show jobs requiring bachelor degrees and higher
        # Locate and open education level selection
        time.sleep(1)
        education_lvl_button = Scraper.driver.find_element(By.ID, 'filter-taxo2')
        education_lvl_button.click()
        # Wait until filters have loaded
        WebDriverWait(Scraper.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[value="HFDVW"]')))
        # Locate and select filters
        bachelors_button = Scraper.driver.find_element(By.CSS_SELECTOR, 'input[value="HFDVW"]')
        masters_button = Scraper.driver.find_element(By.CSS_SELECTOR, 'input[value="EXSNN"]')
        phd_button = Scraper.driver.find_element(By.CSS_SELECTOR, 'input[value="6QC5F"]')
        filter_button = Scraper.driver.find_element(By.CSS_SELECTOR, 'button[form="filter-taxo2-menu"]')
        bachelors_button.click()
        masters_button.click()
        phd_button.click()
        filter_button.click()
        # Return the URL for the filtered results
        return Scraper.driver.current_url

    def __scrape_indeed(self, url, db_con):
        """Scrape from Indeed"""
        # Navigate to tech job list and get URL if starting from original URL
        if url == self.website.url:
            jobs_url = self.__navigate_to_indeed_jobs(url)

            # Get the soup and links from the job listing page
            try:
                soup = self.__get_soup(jobs_url)
            except Exception as e:
                print(e)
                return None
        else:
            # Get the soup and links from the given URL
            try:
                soup = self.__get_soup(url)
            except Exception as e:
                print(e)
                return None
        
        # Get list of links and link to next page
        link_list = self.__get_links(soup)
        next_page = self.__get_next_page(soup)
        # # DEBUG:
        # print(link_list)
        # print(next_page)

        # Filter list of links for job listings
        job_filter = re.compile(r'\/pagead\/.*')
        filtered_list = list(filter(job_filter.match, link_list))
        # # DEBUG:
        # print(filtered_list)
        
        # Visit job listing links and get the data we want
        for link in filtered_list:
            try:
                listing_soup = self.__get_soup('https://uk.indeed.com' + link)
            except Exception as e:
                print(e)
                listing_soup = None

            if listing_soup is not None:
                print('Found Job!')

                # Find job info in HTML
                try:
                    company = listing_soup.find('span', class_=self.website.company_tag).a.attrs.get('aria-label')
                    company = company.replace('(opens in a new tab)', '')
                except Exception:
                    company = 'NULL'

                try:
                    jobtitle = listing_soup.find(self.website.title_tag).get_text()
                except Exception:
                    jobtitle = 'NULL'

                try:  
                    location = listing_soup.find('div', id=self.website.location_tag).get_text()
                except Exception:
                    location = 'NULL'

                try:
                    pay = listing_soup.find('span', class_=self.website.pay_tag).get_text()
                except Exception:
                    pay = 'NULL'

                try:
                    desc = listing_soup.find('div', id=self.website.desc_tag).get_text()
                except Exception:
                    desc = 'NULL'

                timestamp = datetime.now().date().isoformat()

                # Make instance of JobListing class and dump info to database
                job = JobListing(self.website.name, company, jobtitle, location, pay, desc, timestamp)
                job.dump_to_db(db_con)

                # # DEBUG
                # print(company)
                # print(jobtitle)
                # print(location)
                # print(pay)
                # print(desc)
                
        # Scrape from next page
        if next_page is not None:
            next_url = 'https://uk.indeed.com' + next_page
            print('Moving to next page...')
            self.__scrape_indeed(next_url, db_con)

    def scrape(self):
        """Scrapes from the website"""
        print(f'Scraping from {self.website.name}...')

        # Open database connection
        con = sqlite3.connect(DATABASE_PATH)

        # Run scraping function for corresponding website
        if self.website.name == 'Gradcracker':
            self.__scrape_gradcracker(self.website.url, con)
        elif self.website.name == 'Indeed':
            self.__scrape_indeed(self.website.url, con)

        # Close database connection
        con.close()

        print('Finished!')
