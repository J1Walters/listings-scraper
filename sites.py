"""Contains information on the websites to scrape from"""

class Website:
    def __init__(self, name, url, company_tag, title_tag,
                 location_tag, pay_tag, desc_tag):
        self.name = name
        self.url = url
        self.company_tag = company_tag
        self.title_tag = title_tag
        self.location_tag = location_tag
        self.pay_tag = pay_tag
        self.desc_tag = desc_tag

def indeed():
    """Return an instance of the website class for Indeed"""
    site = Website(name = 'Indeed',
                   url = 'https://uk.indeed.com/',
                   company_tag = 'css-1saizt3 e1wnkr790',
                   title_tag = 'h1',
                   location_tag = 'jobLocationText',
                   pay_tag = 'css-19j1a75 eu4oa1w0',
                   desc_tag = 'jobDescriptionText'
    )
    return site

def gradcracker():
    """Return an instance of the website class for Gradcracker"""
    site = Website(name = 'Gradcracker',
                   url = 'https://www.gradcracker.com/search/computing-technology/jobs',
                   company_tag = 'ga_employerName',
                   title_tag = 'h1',
                   location_tag = 'Location',
                   pay_tag = 'Salary',
                   desc_tag = 'body-content'
    )
    return site
