import requests
import json
import time
import hashlib
from bs4 import BeautifulSoup as bs

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Intermountainhealth(BaseScript):
    
    def process_data(self):
        profiles = []
        base_url = 'https://brownmed.org'
        url = 'https://brownmed.org/provider-results'
        page_count = 1
        print("hitting the url")
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': '_ga=GA1.2.1788794410.1711508443; _ga_WYRX7LTFGL=GS1.2.1717062591.9.0.1717062591.0.0.0',
            'Referer': 'https://brownmed.org/find-a-provider/',
            'Sec-Cha-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Sec-Cha-Ua-Mobile': '?0',
            'Sec-Cha-Ua-Platform': '"Windows"',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'  
        }
        r = requests.get(url, headers=headers)
        soup = bs(r.text, 'lxml')
        for td in soup.find_all('td'):
            elements = td.find('a')
            if elements:
                p_url = elements['href']
                p_url = p_url.split('..')[-1]
                doc_url = base_url + p_url
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
                
        print("Total doc_count:", len(profiles))
        if self.check_repeated_pages(profiles):
            pass
        # else:
        #     break
        # return profiles
        return self.profiles
