import requests
import json
import time
import hashlib
from bs4 import BeautifulSoup as bs

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Sutterhealth(BaseScript):
    
    def process_data(self):
        profiles = []
        print("hitting the url")
        base_url = 'https://www.sutterhealth.org/find-clinician/'
        page_count = 1
        offset = 1
        while page_count <= 531:
            print("test")
            url = f'https://www.sutterhealth.org/widgets/json-doctor-results?location=&zip=&lat=&lng=&provider-gender=&medical-group=alta-bates-summit-medical-center-alta-bates-campus^^alta-bates-summit-medical-center-summit-campus&q=&online-services=&specialty=&provider-language=&health-plan=&health-plan-product=&start={offset}'
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.sutterhealth.org/doctor-search/results?location=&zip=&lat=&lng=&provider-gender=&medical-group=alta-bates-summit-medical-center-alta-bates-campus&medical-group=alta-bates-summit-medical-center-summit-campus&q=&online-services=&specialty=&provider-language=&health-plan=&health-plan-product=',
                'Sec-Cha-Ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'Sec-Cha-Ua-Mobile': '?0',
                'Sec-Cha-Ua-Platform': '"Windows"',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
            }
            r = requests.get(url, headers=headers)  # type: ignore
            #print(r.text)  # Log the raw response for inspection

            if r.status_code == 200:
                try:
                    elements = r.json()['payload1']['autnresponse']['responsedata']['hit']
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    print(f"Response text: {r.text}")  # Log the problematic response
                    continue  # Skip to the next page
            else:
                print(f"Request failed with status code: {r.status_code}")
                continue  # Skip to the next page
            
            if elements:
                for i in elements:
                    doc_name = i['content']['PROVIDER']['URL']['$']
                    doc_url = base_url + doc_name
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
                page_count += 1
                offset += 10
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
