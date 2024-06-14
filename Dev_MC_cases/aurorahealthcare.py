from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import hashlib

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Aurorahealthcare(BaseScript):
    
    def process_data(self):
        profiles = []
        print("hitting the url")
        print("test")
        url = 'https://www.aurorahealthcare.org/doctors/'
        self.driver.get(url)
        time.sleep(5)      

        while True:
            try:
                driver.find_element(By.XPATH, '//span[contains(., "Load more")]').click()
                time.sleep(5)
            except Exception as e:
                print(e)
                pass
        
        elements = self.driver.find_elements(By.XPATH, '//div[contains(@class, "list-card-name")]/a')
        
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

        """try:
            print(f"Page {page_count} done")
            print(len(profiles))
            count = count + 1
        except Exception as e:
            print(e)
            break"""
        
        print("Total doc_count:", len(profiles))
        if self.check_repeated_pages(profiles):
            pass
        # else:
        #     break
        # return profiles
        return self.profiles