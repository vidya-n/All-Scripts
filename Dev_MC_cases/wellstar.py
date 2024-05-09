import hashlib
import time

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By
import re

class Wellstar(BaseScript):
    #@property
    # def __int__(self):
        # use create chrome driver only If needed
        # self.selenium_utils = SeleniumUtils(self.driver, self.logger)
    
    def process_data(self):
        profiles = []
        count = 1
        base_url = 'https://www.wellstar.org/physicians/'
        url = 'https://www.wellstar.org/physicians?wellstar%2Bmedical%2Bgroup=1&v=1'
        print("hitting the url")
        self.driver.get(url)
        time.sleep(5)
        while True:
            print("test")
            page_count = count

            elements = self.driver.find_elements(By.XPATH, '//div[contains(@class, "PhysicianCard_cardTitle")]')
            if elements:
                print("data-extracted")
                for i in elements:
                    name = i.text
                    # Remove any non-alphanumeric characters except spaces and hyphens
                    name = re.sub(r'[^a-zA-Z0-9\s-]', '', name)
                    # Convert spaces and hyphens to dashes
                    name = re.sub(r'[\s-]+', '-', name)
                    # Convert to lowercase
                    doc_name = name.lower()
                    doc_url = base_url + doc_name
                    print("doctor url: ", doc_url)
                    hash_object = hashlib.sha256(str(doc_url).encode('utf-8'))
                    profile_id = hash_object.hexdigest()
                    obj1 = str(self.client_id) + profile_id + self.runs
                    # +str(page_count)
                    hex_dig1 = hashlib.sha256(str(obj1).encode('utf-8'))
                    # store = []
                    # print("Hash-check")
                    data_dict = {
                        'find_doctor_url': url,
                        'profile_link': doc_url,
                        'pages_count': page_count,
                        'dhc_id': str(self.client_id),
                        'domain_id': str(self.domain_id),
                        'domain_url': str(self.domain_url),
                        'profile_id': profile_id,
                        'text': "-",
                        'runs': self.runs,
                        'ajax': "-",
                        'extra': "-",
                        'json_data': "-",
                        'objectkey': hex_dig1.hexdigest()}
                    # store.append(doc_url)
                    # store.append(page_count)
                    # store.append(doc_name)
                    # print("CheckCheck1")
                    profiles.append(data_dict)
                    # yield store
                    #print(len(profiles))
                    
            print(len(profiles))
            if self.check_repeated_pages(profiles):
                break
            # else:
            #     break
            # return profiles

        return self.profiles
