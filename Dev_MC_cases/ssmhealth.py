from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import hashlib

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By
import requests

class Nchdoctors(BaseScript):
          
    def process_data(self):
        count = 1
        offset = 0
        profiles = []
        print("hitting the url")
              
        
        while True:
            
            base_url = 'https://www.getcare.ssmhealth.com'
            url = f'https://womphealthapi.azurewebsites.net/api/OmniSearch?skip={offset}%2C0&top=20&location=Centralia%2C+IL+62801%2C+USA&HospitalAffiliation=SSM+Health+St.+Mary%27s+Hospital+-+Centralia&time=any&inferLocationFromSearch=false&locations=false&type=search&brand=ssm'
            #time.sleep(5)
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.getcare.ssmhealth.com/',
                'Sec-Cha-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'Sec-Cha-Ua-Mobile': '?0',
                'Sec-Cha-Ua-Platform': 'Windows',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
            }
            payload = {
                'skip': f'{offset},0',
                'top': '20',
                'location': 'Centralia, IL 62801, USA',
                'HospitalAffiliation': "SSM Health St. Mary's Hospital - Centralia",
                'time': 'any',
                'inferLocationFromSearch': 'false',
                'locations': 'false',
                'type': 'search',
                'brand': 'ssm'
            }
            page_count = count
            
            r = requests.get(url, headers=headers)
            print("test")
            data = json.loads(r.text)
            if data:
                print("data extracted")
                for i in data['results']:
                    try:
                        #doc_url = i.xpath("./a/@href")[0].strip() if "tuftsmedicalcenter.org" in i.xpath("./a/@href")[0].strip() else "https://tuftsmedicalcenter.org" + i.xpath("./a/@href")[0].strip()
                        doc_url = base_url + i['ProfileUrl']
                        #doc_name = (i.xpath("./a/text()"))[0].strip()
                        print("doc_url",doc_url)
                        #print("doc_name",doc_name)
                        hash_object = hashlib.sha256(str(doc_url).encode('utf-8'))
                        profile_id = hash_object.hexdigest()
                        obj1 = str(self.client_id) + profile_id + self.runs
                        # +str(page_count)
                        hex_dig1 = hashlib.sha256(str(obj1).encode('utf-8'))
                        # store = []
                        # print("Checkcheck")
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
                    except Exception as e:
                        print(e)
                        pass
            else:
                print("Not data found.")
            
            print(len(profiles))
            print(f'Page {count} done.')
            count = count + 1
            offset = (count-1) * 20
                        
            print("Total doc_count:", len(profiles))
            if self.check_repeated_pages(profiles):
                break
            # else:
            #     break
            # return profiles
        return self.profiles
