class JobListing:
    """Class for all job listings"""
    def __init__(self, website, company, title, location, pay, description, timestamp):
        self.website = website
        self.company = company
        self.title = title
        self.location = location
        self.pay = pay
        self.description = description
        self.timestamp = timestamp
  
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
        # Create cursor
        cur = db_con.cursor()
        # Add website to website table only if not already in there else pass
        try:
            cur.execute('INSERT INTO website (id, name) VALUES (NULL, ?)', (self.website,))
        except Exception:
            pass
        # Add comapny to company table only if not already in there else pass
        try:
            cur.execute('INSERT INTO company (id, name) VALUES (NULL, ?)', (self.company,))
        except Exception:
            pass
        # Get the website and company IDs from the tables
        web_res = cur.execute('SELECT id FROM website WHERE name = ?', (self.website,))
        website_id = web_res.fetchone()[0]
        company_res = cur.execute('SELECT id FROM company WHERE name = ?', (self.company,))
        company_id = company_res.fetchone()[0]
        # Add job listing to the jobs table
        cur.execute('INSERT INTO job (id, website_id, company_id, title, location, pay, description, timestamp) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)',
                    (website_id, company_id, self.title, self.location, self.pay, self.description, self.timestamp)
        )
        # Commit changes
        db_con.commit()
