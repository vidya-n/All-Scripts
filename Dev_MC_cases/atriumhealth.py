import requests
import json
import time
import hashlib
from bs4 import BeautifulSoup as bs

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Atriumhealth(BaseScript):
    
    def process_data(self):
        profiles = []
        print("hitting the url")
        page_count = 1
        while page_count <= 247:
            print("test")
            url = f'https://providers.atriumhealth.org/physicians.json?api=provider_search&appointment_grid_start_date=2024-10-04&open_scheduling=true&page={page_count}&passive_boosts=true&per_page=20&sort=best_match'
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Cookie': '_evga_e05d={%22uuid%22:%2224b680caf1a429a2%22}; _sfid_f3af={%22anonymousId%22:%2224b680caf1a429a2%22%2C%22consents%22:[]}; ahoy_visit=59433c6e-286f-47c8-a590-956f6a064b40; ahoy_visitor=2404644d-eab5-4b06-8634-7f552572917d; _sparkle_session=IFc%2BUOzeYWNUHb81byj158MAZZAO%2BPq0AJteU7W75rgbZt%2ByjW2EcB2aWLhCZODU346Fp%2FCiXRK0bxnO7tT2jq%2Br4mHu9sv%2FnlUWW%2BUUqLIosbg%3D--nvRNTAwbd%2F6oqvuF--XcZfsNKTOf%2FzJifGF4q8bQ%3D%3D',
                'Referer': 'https://atriumhealth.org/',
                'Sec-Cha-Ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'Sec-Cha-Ua-Mobile': '?0',
                'Sec-Cha-Ua-Platform': '"Windows"',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
            }
            r = requests.get(url, headers=headers) # type: ignore
            elements = r.json()['results']
            if elements:
                for i in elements:
                    doc_url = i['url']
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
