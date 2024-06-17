import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, website):
        self.website = website

    def scrape_gradcracker(self):
        """Scrape from Gradcracker"""
        print('foo')

    def scrape_indeed(self):
        """Scrape from Indeed"""
        print('bar')

    def scrape(self):
        if self.website.name == 'Gradcracker':
            self.scrape_gradcracker()
        elif self.website.name == 'Indeed':
            self.scrape_indeed()
        else:
            pass
