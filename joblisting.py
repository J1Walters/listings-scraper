class JobListing:
    """Class for all job listings"""
    def __init__(self, website, company, title, location, pay, description):
        self.website = website
        self.company = company
        self.title = title
        self.location = location
        self.pay = pay
        self.description = description
  
    def print(self):
        """Print attributes"""
        print(f'From: {self.website}')
        print(f'Company: {self.company}')
        print(f'Job Title: {self.title}')
        print(f'Location: {self.location}')
        print(f'Pay: {self.pay}')
        print(f'Description: {self.description}')

    def dump_to_db(self, db_con):
        """Insert listing info into database"""
        cur = db_con.cursor()
        cur.execute('INSERT INTO website (name) VALUES (?)', self.website)
        cur.execute('INSERT INTO company (name) VALUES (?)', self.company)
        db_con.commit()
