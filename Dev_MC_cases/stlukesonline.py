import requests
import json
import time
import hashlib

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Stlukesonline(BaseScript):
    
    def process_data(self):
        profiles = []
        base_url = 'https://www.stlukesonline.org'
        print("hitting the url")
        page_count = 1
        while page_count <= 65:
            print("test")
            url = f'https://www.stlukesonline.org/api/sitecore/providersearch/ProviderSearch?filters=language%3D%26genderPreference%3D%26searchZip%3D%26FromState%3D%26FromCity%3D%26FromAddress%3D%26distance%3D5%26keyword%3D%26perPage%3D50&page={page_count}
            headers= {
                'Accept': 'application/json, text/plain, */*', # type: ignore
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.stlukesonline.org/health-services/find-a-provider/provider-results?',
                'Sec-Cha-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'Sec-Cha-Ua-Mobile': '?0',
                'Sec-Cha-Ua-Platform': '"Windows"',
                #'Sec-Fetch-Dest': 'empty',
                #'Sec-Fetch-Mode': 'cors',
                #'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
            }
            payload = {
                'filters': 'language=&genderPreference=&searchZip=&FromState=&FromCity=&FromAddress=&distance=5&keyword=&perPage=50',
                'page': f'{page_count}'
            }
            r = requests.post(url, headers=headers) # type: ignore
            elements = r.json()['providers']
            if elements:
                for i in elements:
                    doc_url = base_url + i['url']
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
