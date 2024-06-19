import requests
import json
import time
import hashlib

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Aurorahealthcare(BaseScript):
    
    def process_data(self):
        profiles = []
        print("hitting the url")
        offset = 0
        max = 7786
        page_count = 1
        while offset <= max:
            print("test")
            url = f'https://locator-api.localsearchprofiles.com/api/LocationSearchResults/?configuration=3428caf5-3f0a-4dd6-85a9-277a710ec0b0&&address=40.7127753%2C-74.0059728&searchby=address&start={offset}'
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Origin': 'https://www.aurorahealthcare.org',
                'Sec-Cha-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'Sec-Cha-Ua-Mobile': '?0',
                'Sec-Cha-Ua-Platform': '"Windows"',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
            }
            payload = {
                'configuration': '3428caf5-3f0a-4dd6-85a9-277a710ec0b0',
                'address': '40.7127753,-74.0059728',
                'searchby': 'address',
                'start': f'{offset}'
            }
            r = requests.get(url, headers=headers)
            elements = r.json()['Hit']
            if elements:
                for i in elements:
                    doc_url = i['Fields']['Url'][0]
                    #print(doc_url)
                    hash_object = hashlib.sha256(str(doc_url).encode('utf-8'))
                    profile_id = hash_object.hexdigest()
                    obj1 = str(self.client_id) + profile_id + self.runs + str(page_count)
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
                print(f"Page {page_count} done.")
                print(len(profiles))
                offset = (page_count-1)*10
                page_count += 1
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
