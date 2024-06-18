import requests
import time
import re
from selenium_config import load_selenium_driver
from bs4 import BeautifulSoup

class Scraper:
    # Get Selenium driver
    driver = load_selenium_driver()

    def __init__(self, website):
        self.website = website

    def get_links(self):
        """Get a list of all the links from the websites URL"""
        try:
            # Make connection to site and wait for loading
            Scraper.driver.get(self.website.url)
            time.sleep(2)
        except Exception as e:
            print(e)
            return None

        # Get HTML as BeautifulSoup object
        soup = BeautifulSoup(Scraper.driver.page_source, 'html.parser')
        link_list = []

        # Add href to link_list if present
        for link in soup.find_all('a'):
            if 'href' in link.attrs:
                link_list.append(link.attrs['href'])

        return link_list

    def scrape_gradcracker(self):
        """Scrape from Gradcracker"""
        # Get list of all links on page
        try:
            link_list = self.get_links()
        except Exception as e:
            print(e)
            return None

        # Filter list of links for job listings
        job_filter = re.compile('https:\/\/www\.gradcracker\.com\/.*\/graduate-job\/.*')
        filtered_list = list(filter(job_filter.match, link_list))
        print(filtered_list)
        

    def scrape_indeed(self):
        """Scrape from Indeed"""
        print('bar')

    def scrape(self):
        if self.website.name == 'Gradcracker':
            return self.scrape_gradcracker()
        elif self.website.name == 'Indeed':
            return self.scrape_indeed()
        else:
            pass
