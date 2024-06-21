import time
import re
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
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
            time.sleep(2)
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
        try:
            next_page = soup.find('a', rel='next').attrs.get('href')
        except Exception:
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

            if listing_soup is not None:
                print('Found Job!')
            
                # Find job info in HTML
                company = listing_soup.find('input', id=self.website.company_tag).attrs.get('value')
                jobtitle = listing_soup.find(self.website.title_tag).get_text()
                location = listing_soup.find('div', text=self.website.location_tag).parent.get_text()
                pay = listing_soup.find('div', text=self.website.pay_tag).parent.get_text()
                desc = listing_soup.find('div', class_=self.website.desc_tag).get_text()
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

        # Submit search term into search bar
        search_box = Scraper.driver.find_element(By.ID, 'text-input-what')
        submit_button = Scraper.driver.find_element(By.CLASS_NAME, 'yosegi-InlineWhatWhere-primaryButton')

        search_box.send_keys('technology')
        submit_button.click()

        # Filter to only show jobs requiring bachelor degrees and higher
        
        

    def __scrape_indeed(self, url, db_con):
        """Scrape from Indeed"""
        # Navigate to tech job list



    def scrape(self):
        print(f'Scraping from {self.website.name}...')

        # Open database connection
        con = sqlite3.connect(DATABASE_PATH)

        # Run scraping function for corresponding website
        if self.website.name == 'Gradcracker':
            self.__scrape_gradcracker(self.website.url, con)
        elif self.website.name == 'Indeed':
            return self.__scrape_indeed(self.website.url, con)

        # Close database connection
        con.close()

        print('Finished!')
