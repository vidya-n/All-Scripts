import requests
import json
import time
import hashlib
from bs4 import BeautifulSoup as bs

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Nyp(BaseScript):
    
    def process_data(self):
        profiles = []
        print("hitting the url")
        base_url = 'https://doctors.nyp.org/'
        page_count = 1
        offset = 0
        token = 1
        aff = 'false'
        while token <= 2:
            print("token loop")
            if token == 1:
                aff = 'true'
                total_pages = 8
            elif token == 2:
                aff = 'false'
                total_pages = 4
            while page_count <= total_pages:
                print("test")
                url = f'https://doctors.nyp.org/?offset={offset}&zt=xh4HDF4h--2P22qe0yiwOfMErE3ES5d9thE296tc3pQEQfpHJWxoBZcQaFEuzeeTjDfCKknnmKsbDmUZaktZsplueyWfem8Cdlun-hrtuVcG6F-cyhbCIMY3b5ByuGonR2Fq-JaBNGtj_autEDC4AQ==&aff={aff}&hf=5491523'
                
                headers = {
                    'Accept': 'application/json',
                    'Accept-Encoding': 'gzip, deflate, br, zstd',
                    'Cookie': 'ppms_privacy_283ac5bc-49a7-4696-ac18-648eb17a43f4={%22visitorId%22:%223b3e4ae2-92ca-4313-9cee-254d6b4c40c4%22%2C%22domain%22:{%22normalized%22:%22nyp.org%22%2C%22isWildcard%22:true%2C%22pattern%22:%22*.nyp.org%22}%2C%22consents%22:{%22analytics%22:{%22status%22:-1}%2C%22remarketing%22:{%22status%22:-1}%2C%22ab_testing_and_personalization%22:{%22status%22:-1}%2C%22conversion_tracking%22:{%22status%22:-1}}%2C%22staleCheckpoint%22:%222024-04-01T02:44:52.671Z%22}; __cf_bm=3XT1Ck5JexRZKGFzCiMoRYiA_zsb2c4tu9b.Hx9ykp8-1728191961-1.0.1.1-eY95dZFzjj95x7wdAPU3rA5diSEi0XZYBauKyEYPkzMlMWWL4U1WTsYkP7IWHVw8MKxuHq5MNlDbOSTL.I7D1w; _pk_ses.283ac5bc-49a7-4696-ac18-648eb17a43f4.473a=*; _pk_id.283ac5bc-49a7-4696-ac18-648eb17a43f4.473a=3bc7efc95c48b7df.1711939495.23.1728192128.1728191967.',
                    'Referer': 'https://doctors.nyp.org/',
                    'Sec-Cha-Ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                    'Sec-Cha-Ua-Mobile': '?0',
                    'Sec-Cha-Ua-Platform': '"Windows"',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/000000000 Safari/537.36'
                }
                r = requests.get(url, headers=headers) # type: ignore
                elements = r.json()['response']['entities']
                if elements:
                    for i in elements:
                        doc_url = i['profile']['websiteUrl']
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
                    print(f'Page {page} with aff= {aff}: ', len(profiles))
                    page_count += 1
                    offset += 20
                except Exception as e:
                    print(e)
                    break
                
                print("Total doc_count:", len(profiles))
                if self.check_repeated_pages(profiles):
                    break
                # else:
                #     break
                # return profiles
            token += 1
            page = 1  # Reset page for the next token
            offset = 0  # Reset offset for the next token
        return self.profiles
