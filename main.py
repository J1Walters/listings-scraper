from sites import gradcracker
from scraper import Scraper

def main():
    gc_scraper = Scraper(gradcracker())
    print(gc_scraper.scrape())

if __name__ == '__main__':
    main()
