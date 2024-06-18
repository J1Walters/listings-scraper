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

# def indeed():
#     indeed = Website('Indeed', 'test.com', 'jobsearch-RightPane css-1wwhdud eu4oa1w0', 'embedded')
#     return indeed

def gradcracker():
    """Return an instance of the website class for Gradcracker"""
    site = Website(name = 'Gradcracker',
                   url = 'https://www.gradcracker.com/search/computing-technology/jobs',
                   listing_class = None,
                   listing_format = 'new-page',
                   company_tag = None,
                   title_tag = 'h1',
                   location_tag = 'Location',
                   pay_tag = 'Salary',
                   desc_tag = 'body-content'
    )
    return site
