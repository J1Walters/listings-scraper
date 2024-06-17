"""Contains information on the websites to scrape from"""

class Website:
    def __init__(self, name, url, listing_class, listing_format, company_tag, title_tag,
                 location_tag, pay_tag, desc_tag):
        self.name = name
        self.url = url
        self.listing_class = listing_class
        self.listing_format = listing_format
        self.company_tag = company_tag
        self.title_tag = title_tag
        self.location_tag = location_tag
        self.pay_tag = pay_tag
        self.desc_tag = desc_tag

indeed = Website('Indeed', 'test.com', 'jobsearch-RightPane css-1wwhdud eu4oa1w0', 'embedded')

def gradcracker():
    """Return an instance of the website class for Gradcracker"""
    site = Website(name = 'Gradcracker',
                   url = 'https://www.gradcracker.com/search/computing-technology/jobs',
                   listing_class = 'tw-p-4 result-item',
                   listing_format = 'new-page',
                   company_tag = None,
                   title_tag = 'tw-text-xl tw-font-semibold tw-text-employer-500 tw-text-balance',
                   location_tag = 'tw-pb-1 tw-font-semibold tw-text-employer-500',
                   pay_tag = 'tw-pb-1 tw-font-semibold tw-text-employer-500',
                   desc_tag = 'aria-labelledby="description"'
    )
    return site

def foo():
    pass
