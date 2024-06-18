import time
import re
from bs4 import BeautifulSoup
from selenium_config import load_selenium_driver

class Scraper:
    # Get Selenium driver
    driver = load_selenium_driver()

    def __init__(self, website):
        self.website = website

    def __get_html(self, url):
        """Get the HTML from the given URL"""
        try:
            # Make connection to site and wait for loading
            Scraper.driver.get(url)
            time.sleep(2)
        except Exception as e:
            print(e)
            return None

        return Scraper.driver.page_source

    def get_links(self):
        """Get a list of all the links from the websites URL"""
        try:
            # Get HTML
            html = self.__get_html(self.website.url)
        except Exception as e:
            print(e)
            return None

        # Get HTML as BeautifulSoup object
        soup = BeautifulSoup(html, 'html.parser')
        link_list = []

        # Add href to link_list if present
        for link in soup.find_all('a'):
            if 'href' in link.attrs:
                link_list.append(link.attrs['href'])

        return link_list

    def __scrape_gradcracker(self):
        """Scrape from Gradcracker"""
        # Get list of all links on page
        try:
            link_list = self.get_links()
        except Exception as e:
            print(e)
            return None

        # Filter list of links for job listings
        job_filter = re.compile(r'https:\/\/www\.gradcracker\.com\/.*\/graduate-job\/.*')
        filtered_list = list(filter(job_filter.match, link_list))
        # # DEBUG:
        # print(filtered_list)

        # Visit job listing links and get the data we want
        for link in filtered_list:
            try:
                html = self.__get_html(link)
            except Exception as e:
                print(e)

            soup = BeautifulSoup(html, 'html.parser')
            jobtitle = soup.find(self.website.title_tag).get_text()
            location = soup.find('div', text=self.website.location_tag).parent.get_text()
            print(jobtitle, location) # TODO: Put job data into job listing class

    def __scrape_indeed(self):
        """Scrape from Indeed"""
        print('bar')

    def scrape(self):
        if self.website.name == 'Gradcracker':
            return self.__scrape_gradcracker()
        elif self.website.name == 'Indeed':
            return self.__scrape_indeed()
        else:
            pass
