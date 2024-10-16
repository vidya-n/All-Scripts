import requests
import json
import time
import hashlib
from bs4 import BeautifulSoup as bs

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Hartfordhealthcare(BaseScript):
    
    def process_data(self):
        profiles = []
        page_count = 1
        base = 'https://hartfordhealthcare.org'
        print("hitting the url")
        while page_count <= 153:
            url = f'https://hartfordhealthcare.org/find-a-doctor/physician-results?Keywords=&Location=&Distance=10&Page={page_count}&Sort=Rating+DESC'
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cookie': '_gcl_au=1.1.1368616668.1722859110; nmstat=1bffc3a0-7d45-a961-a848-a18ed2501626; _ga=GA1.1.1310274550.1722859111; iappsvisitor=e834f07b-e055-4eeb-9211-b1c300836def; FPID=FPID2.2.ZJD7hnd6ZL1nOGNfhstLJllVoC3Swqoha%2FUDx9BJSZA%3D.1722859111; .ASPXANONYMOUS=-n3cT7E-2wEkAAAAYTdhMDExODItNzRiZC00Y2YzLWEwNjAtNWZhYWM0MjgzMmMyw68RGz1dPRxNitCHaw0TvT8xczDbjm3cFL86asdWuXvn8-eYdlveoLQ3xkMcgxh94l4fxcR2_twd_1kjjkY2dA2; ASP.NET_SessionId=syginl1nufubnfi43ixtbygz; __AntiXsrfToken=cd3a26c057df47aaa527cc26b383f906; FPLC=cP2iBUR3dIIRJ6YXuTAy4sX1cHqzsFur5UBY%2BblQwaO4xgLFq42VusKSoNyAnCxydJDgrdDh8F5%2FqPvwFMS0kzHkvNgt8JdPpvoAU0ARHLkPrV9tl1KxIVjTwBplog%3D%3D; _ga_N73846W54H=GS1.1.1728282184.6.1.1728283005.0.0.956649668; _ga_4604MZZMMD=GS1.1.1728282185.6.1.1728283005.0.0.2000709368',
                'Referer': 'https://hartfordhealthcare.org/find-a-doctor/physician-results?Keywords=&Location=&Distance=10&Page=1',
                'Sec-Cha-Ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'Sec-Cha-Ua-Mobile': '?0',
                'Sec-Cha-Ua-Platform': '"Windows"',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/000000000 Safari/537.36'
            }
            print("Hitting URL: ", url)
            r = requests.get(url, headers=headers)
            
            """if r.status_code != 200:
                print(f"Failed to retrieve page {page}. Status code: {r.status_code}")
                break"""
            
            soup = bs(r.content, 'html.parser')
            docs = soup.find_all('h3')
            for doc in docs:
                elements = doc.find_all('a', href=True)
                if elements and elements['href'].strip():
                    doc_url = elements['href'].strip()
                    print(doc_url)
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
