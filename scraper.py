import requests
import time
from selenium_config import load_selenium_driver
from bs4 import BeautifulSoup

class Scraper:
    driver = load_selenium_driver()
    def __init__(self, website):
        self.website = website
        self.headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,\
                        image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Accept-Language':'en-US,en;q=0.9',
                        'Sec-CH-UA-Mobile':'?1',
                        'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
                        'Viewport-Width':'980'
        }

    def get_links(self):
        """Get a list of all the links from the websites URL"""
        try:
            Scraper.driver.get(self.website.url)
            time.sleep(2)
        except Exception as e:
            print(e)
            return None
        
        soup = BeautifulSoup(Scraper.driver.page_source, 'html.parser')
        link_list = []
        
        for link in soup.find_all('a'):
            if 'href' in link.attrs:
                link_list.append(link.attrs['href'])
        
        return link_list

    def scrape_gradcracker(self):
        """Scrape from Gradcracker"""
        try:
            r = requests.get(self.website.url)
        except Exception:
            print('An Error Occurred')
            return None
        return BeautifulSoup(r.text, 'html.parser')

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
