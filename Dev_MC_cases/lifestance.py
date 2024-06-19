import requests
import json
import time
import hashlib
from bs4 import BeautifulSoup as bs

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Lifestance(BaseScript):
    
    def process_data(self):
        profiles = []
        print("hitting the url")
        page_count = 1
        offset = 0
        while page_count <= 16:
            print("test")
            url = f'https://lifestance.com/lsapi/provider/wide_search/card_html?search=&offset={offset}&limit=500'
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cookie': '_vwo_uuid=D45A7EA244BCA3500D1F84196E956EC26; _vwo_ds=3%241717664955%3A76.79986993%3A%3A; _vis_opt_s=2%7C; _vis_opt_test_cookie=1; _vwo_uuid_v2=D69B4767CAE38FAB704167C72FED5C623|1784d28bfd7e399e130253bbd84e319f; cf_clearance=dbrHykwSBIODSTIT7qafnJ4XwLYq_p1R7FDf5GmSp5A-1718608648-1.0.1.1-psg35UQMAN23idrI5N6NJx_goscNGOouJ8nTpLA9e2Av1Oi29nTXPuIfONpFNIvbhWgMphFWezbb9UwJyTvgXA; visitor_id979193=559894630; visitor_id979193-hash=71e42244aa2e411e3b50d81c49c013018534cf23d14e0c8c5c810ae2a27001edb0e292e38a5f82f9766eb28ecb98635f0e35e4fd; __cf_bm=qSgQJ3mjKIfpi1F3qBV1mUEzStYBWVUToQ_p6lToFmU-1718615079-1.0.1.1-XEGdcMf39Lx.WJL5XcHjh57px3IWdTkyFlMRbH6x8jR5UjEXeMHvmPObS1NcLPafjgbABXipBq2dP9ASnQVd5w; _hp2_ses_props.2882405371=%7B%22ts%22%3A1718615082949%2C%22d%22%3A%22lifestance.com%22%2C%22h%22%3A%22%2Fprovider%2F%22%7D; _vwo_sn=948878%3A3%3A%3A%3A1; _hp2_id.2882405371=%7B%22userId%22%3A%228219772706812850%22%2C%22pageviewId%22%3A%227502398765765075%22%2C%22sessionId%22%3A%221179561247295260%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; invoca_session=%7B%22ttl%22%3A%222024-07-17T09%3A05%3A45.246Z%22%2C%22session%22%3A%7B%22invoca_id%22%3A%22i-6e4833d4-9681-422c-8903-d95baa3a4084%22%7D%2C%22config%22%3A%7B%22ce%22%3Atrue%2C%22fv%22%3Afalse%2C%22rn%22%3Afalse%2C%22ba%22%3Atrue%2C%22br%22%3Atrue%7D%7D',
                'Sec-Cha-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'Sec-Cha-Ua-Mobile': '?0',
                'Sec-Cha-Ua-Platform': '"Windows"',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            r = requests.get(url, headers=headers) # type: ignore
            elements = r.json()['payload']
            if elements:
                for i in elements:
                    soup = bs(i, 'html.parser')
                    a_tag = soup.find('a') 
                    doc_url = a_tag['href']
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
                offset += 500
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
