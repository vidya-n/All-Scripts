import requests
from bs4 import BeautifulSoup as bs
import time
import hashlib

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Nchdoctors(BaseScript):
          
    def process_data(self):
        count = 1
        profiles = []
        print("hitting the url")
              
        
        while True:
            print("test")
            page_count = count
            url = f'https://www.dulyhealthandcare.com/physicians?page={page_count}&per-page=10'
            headers = {
                'Accept': 'text/html',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'max-age=0',
                'Cookie': '374d18ba1470ddd026eed29f136fd8=583ugnpe2q45kkt502h1q2j7mq; 7cbf40c6d657754517c6905b0b65fd1e=d14b482c1178045acd4f8beba172576bd0bee91c4b9959c5cb244119b90845c7a%3A2%3A%7Bi%3A0%3Bs%3A32%3A%227cbf40c6d657754517c6905b0b65fd1e%22%3Bi%3A1%3Bs%3A40%3A%22VXywCqp6lLhynEVca3LAu15mohH_DkkBuqXLr3ZG%22%3B%7D; _gcl_au=1.1.572383291.1718263188; _evga_7ee7={%22uuid%22:%2244748a3936c391ce%22}; _sfid_7159={%22anonymousId%22:%2244748a3936c391ce%22%2C%22consents%22:[]}; _ga=GA1.1.435291506.1718263191; _ga_XW0KZBCGRH=GS1.1.1718284941.2.1.1718284948.0.0.0',
                'Referer': f'https://www.dulyhealthandcare.com/physicians?page={page_count}&per-page=10',
                'Sec-Cha-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'Sec-Cha-Ua-Mobile': '?0',
                'Sec-Cha-Ua-Platform': '"Windows"',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'X-Isajax': 'true'
            }
            r = requests.get(url, headers=headers)
            soup = bs(r.text, "html.parser")
            elements = soup.find_all('a', string='Schedule Online')
            if elements:
                for i in elements:
                    doc_url = i['href']
                    #print(doc_url)
                    hash_object = hashlib.sha256(str(doc_url).encode('utf-8'))
                    profile_id = hash_object.hexdigest()
                    obj1 = str(self.client_id) + profile_id + self.runs
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
                print(f"Page {page_count} done")
                print(len(profiles))
                count = count + 1
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
