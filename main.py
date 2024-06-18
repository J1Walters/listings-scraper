from sites import gradcracker
from scraper import Scraper

def main():
    gc_scraper = Scraper(gradcracker())
    gc_scraper.get_links()

if __name__ == '__main__':
    main()
