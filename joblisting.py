class JobListing:
    """Class for all job listings"""
    def __init__(self, jobID, company, title, location, pay, description):
        self.jobID = jobID
        self.company = company
        self.title = title
        self.location = location
        self.pay = pay
        self.description = description
        
    def print(self):
        """Print attributes"""
        print(f'Job ID: {self.jobID}')
        print(f'Company: {self.company}')
        print(f'Job Title: {self.title}')
        print(f'Location: {self.location}')
        print(f'Pay: {self.pay}')
        print(f'Description: {self.description}')

    def dump_to_db():
        pass
