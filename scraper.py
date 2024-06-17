import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, website):
        self.website = website

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
