from sites import gradcracker, indeed
from scraper import Scraper

def main():
    gc_scraper = Scraper(gradcracker())
    # gc_scraper.scrape()
    indeed_scraper = Scraper(indeed())
    indeed_scraper.scrape()

if __name__ == '__main__':
    main()
