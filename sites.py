class Website:
    def __init__(self, name, url, listingClass, listingFormat):
        self.name = name
        self.url = url
        self.listingClass = listingClass
        self.listingFormat = listingFormat
        
indeed = Website('Indeed', 'test.com', 'jobsearch-RightPane css-1wwhdud eu4oa1w0', 'imbedded')

gradcracker = Website('Gradcracker',
                    'https://www.gradcracker.com/search/computing-technology/jobs',
                    'tw-p-4 result-item',
                    'new-page'
                    )
