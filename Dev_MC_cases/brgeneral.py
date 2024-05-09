from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import hashlib

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class BRGeneral(BaseScript):
          
    def process_data(self):
        url = 'https://www.brgeneral.org/find-a-provider/'
        base_url = 'https://www.brgeneral.org/'
        count = 1
        profiles = []
        print("hitting the url")
        self.driver.get(url)
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//input[contains(@name, "PhysicianSearch$HDR0$MedicalGroup")]/..').click()
        time.sleep(5)
        
        while True:
            print("test")
            page_count = count
            elements = self.driver.find_elements(By.XPATH, '//li[contains(@class, "half item-")]/a')
            if elements:
                for i in elements:
                    doc_url = i.get_attribute('href')
                    print(doc_url)
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
                # Wait for the "Next" button to be present
                next_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "next")]'))
                )
                # Scroll to the "Next" button
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                # Click the "Next" button using JavaScript executor
                driver.execute_script("arguments[0].click();", next_button)

                time.sleep(5)
                print(f"Page {page_count} done.")
                count = count + 1
            except Exception as e:
                print("Pagination failed")
                print(e)
                break
            
            print(len(profiles))
            if self.check_repeated_pages(profiles):
                break
            # else:
            #     break
            # return profiles
        return self.profiles
