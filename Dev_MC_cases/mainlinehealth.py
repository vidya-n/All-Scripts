import requests
import json
import time
import hashlib
from bs4 import BeautifulSoup as bs

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Mainlinehealth(BaseScript):
    
    def process_data(self):
        profiles = []
        print("hitting the url")
        page_count = 1
        offset = 0
        while page_count <= 65:
            print("test")
            url = f'https://liveapi.yext.com/v2/accounts/me/answers/vertical/query?experienceKey=fad-answers-updated&api_key=22d3f337d3e8f508f826f314acd668e2&v=20190101&version=PRODUCTION&locale=en&input=&verticalKey=healthcare_professionals&limit=50&offset={offset}&retrieveFacets=true&facetFilters=%7B%22c_primaryHospitalAffiliation%22%3A%5B%5D%2C%22c_fADSpecialties.name%22%3A%5B%5D%2C%22gender%22%3A%5B%5D%2C%22c_raceAndEthnicity%22%3A%5B%5D%2C%22languages%22%3A%5B%5D%2C%22c_insuranceAcceptedAnswers%22%3A%5B%5D%2C%22c_onlineSchedulingFilter%22%3A%5B%5D%2C%22c_topDoc2024%22%3A%5B%5D%2C%22acceptingNewPatients%22%3A%5B%5D%7D&session_id=15892a3f-b8bd-40e5-a697-bc6534e26b4b&sessionTrackingEnabled=true&sortBys=%5B%5D&referrerPageUrl=https%3A%2F%2Fwww.mainlinehealth.org%2Fmain-line-healthcare&source=STANDARD&queryId=01902f5f-3dce-41cb-fb79-f48174246242&jsLibVersion=v1.11.1'
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cookie': '__cf_bm=NbgwbIjKiwTKo.MdZdU__GCaMg_pCg_5ldilFQy9A_o-1718781662-1.0.1.1-hXJrqwIQXek0uUeeeYaJvokIZ7nToIz.bga2s3aLM3dI_jWd0z2KhRip3zxvMQjAqVBAj3KXoHDGsA12CNnKU6pm7ofhKXWaNikIM_VjPjo; _cfuvid=51Gz700VSX66ES9VbE9frH5P._WMPvXDGBChifQ80jU-1718781662617-0.0.1.1-604800000',
                'Referer': 'https://answers-embed.mainlinehealth.org.pagescdn.com/',
                'Sec-Cha-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'Sec-Cha-Ua-Mobile': '?0',
                'Sec-Cha-Ua-Platform': '"Windows"',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
            }
            r = requests.get(url, headers=headers) # type: ignore
            elements = r.json()['response']['results']
            if elements:
                for i in elements:
                    if 'landingPageUrl' in i['data']:
                        doc_url = i['data']['landingPageUrl']
                    else:
                        pass
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
                offset += 50
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
