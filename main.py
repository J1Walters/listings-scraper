from sites import gradcracker, indeed
from scraper import Scraper

def main():
    # Scrape jobs from Gradcracker
    gc_scraper = Scraper(gradcracker())
    gc_scraper.scrape()

    # Scrape jobs from Indeed
    indeed_scraper = Scraper(indeed())
    indeed_scraper.scrape()

if __name__ == '__main__':
    main()
