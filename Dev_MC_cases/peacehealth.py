from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import hashlib

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Nchdoctors(BaseScript):
          
    def process_data(self):
        count = 1
        profiles = []
        print("hitting the url")
        url = 'https://www.peacehealth.org/find-care-providers'
        self.driver.get(url)
        self.driver.find_element(By.XPATH, '//button[contains(., "More Filters")]').click()
        self.driver.find_element(By.XPATH, '//label[contains(., "PeaceHealth employed providers")]/preceding-sibling::input').click()
        self.driver.find_element(By.XPATH, '//button[contains(., "Search")]').click()
        time.sleep(5)
        
        while True:
            print("test")
            page_count = count
            elements = self.driver.find_elements(By.XPATH, '//h1/a')
            if elements:
                for i in elements:
                    doc_url = i.get_attribute('href')
                    #print(doc_url)
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

            try:
                self.driver.find_element(By.XPATH, '//button[contains(., "More")]').click()
                time.sleep(3)
                print(f'Page {count} done.')
                print(len(profiles))
                count = count + 1
            except Exception as e:
                print(e)
                break
            
            print("Total doc_count:", len(profiles))
            if self.check_repeated_pages(profiles):
                break
            # else:
            #     break
            # return profiles
        return self.profiles
