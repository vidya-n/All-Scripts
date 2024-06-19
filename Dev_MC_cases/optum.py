import requests
import json
import time
import hashlib
from bs4 import BeautifulSoup as bs

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Optum(BaseScript):
    
    def process_data(self):
        profiles = []
        print("hitting the url")
        page_count = 1
        offset = 0
        while page_count <= 155:
            print("test")
            url = f'https://liveapi.yext.com/v2/accounts/me/answers/vertical/query?experienceKey=optum_socal_plu&api_key=dcd422373a6ece12ff06a8366c6d5a1b&v=20190101&version=PRODUCTION&locale=en&input=Doctor+near+me&verticalKey=healthcare_professionals&limit=50&offset={offset}&retrieveFacets=true&facetFilters=%7B%7D&session_id=6606662b-6e3a-49a5-91c2-e85b9788fcc7&sessionTrackingEnabled=true&sortBys=%5B%5D&referrerPageUrl=https%3A%2F%2Fwww.optum.com%2Fen%2Fcare%2Flocations%2Fcalifornia%2Foptum-california.html&source=STANDARD&jsLibVersion=v1.11.1'
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cookie': '__cf_bm=pKwxCwgiq7N_1iNqGujBo2CeCJOpl71_POwhFkRzQ_A-1718677481-1.0.1.1-KxI1AngfFrFFpw0SQtO8AmTbzER.YOj6akMo9GxZyARP2bvJ1..d0qS_EZKdFDFsPiAs97wpab0u1gh4OLmcqnocZ9E_sLSuuPRcvjZClKc; _cfuvid=7rCzMAYaYx4edyGtDZH1efJbrgIkWJg4_EnZEwGCELU-1718677481900-0.0.1.1-604800000',
                'Referer': 'https://answers-embed-socal.optum.com.pagescdn.com/',
                'Sec-Cha-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'Sec-Cha-Ua-Mobile': '?0',
                'Sec-Cha-Ua-Platform': '"Windows"',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
            }
            r = requests.get(url, headers=headers) # type: ignore
            elements = r.json()['response']['results']
            if elements:
                for i in elements:
                    doc_url = i['data']['c_soCalPagesURL']
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
