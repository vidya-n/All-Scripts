import requests
import json
import time
import hashlib
import urllib.parse

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Intermountainhealth(BaseScript):
    
    def process_data(self):
        profiles = []
        print("hitting the url")
        page_count = 1
        base_url = 'https://doctors.christianacare.org/provider/'
        #offset = 0
        while page_count <= 50:
            print("test")
            url = f'https://doctors.christianacare.org/api/searchservice-v9/christiana/providers?filter=provider.direct_book_capable%3Atrue&facet=provider.id&sort=relevance%2Cavailability_density_best&search_alerts=false&shuffle_seed=ff268518-d948-40a6-bd1f-124c64dea5c7&provider_fields=-clinical_keywords&page={page_count}&context=christiana_pmc&tracking_token=a718c873-e309-4727-aa79-62ab1be65cac&search_token=8fc2e044-47c3-4b91-84d5-1ee3dcda76a0&user_id=d20dd5ae-a3ce-5009-81d1-3d38aa25d3e2&user_token=da96baca-4acd-42e9-8a9b-4bbc91d82378&per_page=50&components=administrative_area%3ADE&exclude_from_analytics=true'
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': f'https://doctors.christianacare.org/search?sort=relevance%2Cavailability_density_best&search_alerts=false&shuffle_seed=ff268518-d948-40a6-bd1f-124c64dea5c7&provider_fields=-clinical_keywords&page={page_count}',
                'Cookie': 'consumer_user_token=da96baca-4acd-42e9-8a9b-4bbc91d82378; visid_incap_2775688=jvPXIrhrTfGiuASR7g/tWUqDVmYAAAAAQUIPAAAAAADBkvBDYGoALsRiIPzNHCJG; consumer_tracking_token=a718c873-e309-4727-aa79-62ab1be65cac; search_shuffle_token=ff268518-d948-40a6-bd1f-124c64dea5c7; nlbi_2775688=bUzaXVmfJUT6/lqjON60KQAAAABiuIGTndivR8v/nvSlRteT; incap_ses_2102_2775688=xzpFIc/9iwO/lcSt780rHRbdc2YAAAAAe+1TaHL+Hjj4vcJ+2w+I5Q==; reese84=3:DdlfJTKoS4EHu31c0aAtag==:1N67QJEUABWYEwhPrUvqdErgtgAqXwR5wjujilNtL1Qp6tRwS5/J+WkNYm/pte7+g/N+LMTF5jXq97NNtluftSE5k4xDGjasjtkiIRJfCL2AiiPoGji/1GxQqI5QqegJ0HWQ6uggeu0crFokD3xy2SHlB+FQ+jeSVYsSiUuTDF8HDKWJScBq0W4qZx6jhKKRZIFoJwZsDwtjnWffw846u810cXSichBABxYX/0JRCT63qgVIHK8/x9FFAgO6y53mybSaL1+olSgcpeLhyPwfpQ7xQrOW54yBl/TvySruRo2emtaLdzAWt6DaPW+c+2AkAuYAUhHkWi5O2IXQC07P+QnsVPFT/ZxgH5CikloKSoR50WlGQOn+wcO6i7XX9PagGuwn/5b5qfFdURyC51SUTdUDWKhVpwQ00ZKQtDHN4S7yE008OXdAY75lxxuPnfKhYHOjVBOAm+jx+4tQTKdYYg==:VIpQ/EQumwVAzN132fTg4kZKlmsMr3Q13f5N8btizGE=; nlbi_2775688_2147483392=EcpmETjO8CStQKEKON60KQAAAABq6ZCvraitEI30LgcsktLM; utag_main=v_id:018fc1f10701001c05591b680e910506f005406700978$_sn:5$_se:6$_ss:0$_st:1718871118146$dc_visit:4$ses_id:1718869276955%3Bexp-session$_pn:2%3Bexp-session$dc_event:6%3Bexp-session$dc_region:us-west-2%3Bexp-session',
                'Sec-Cha-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'Sec-Cha-Ua-Mobile': '?0',
                'Sec-Cha-Ua-Platform': '"Windows"',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'X-Consumer-Groups': 'christiana',
                'X-Consumer-Username': 'pmc',
                'X-Csrf-Header': 'christiana',
                'X-Requested-With': 'XMLHttpRequest'
            }
            r = requests.get(url, headers=headers) # type: ignore
            elements = r.json()['_result']
            if elements:
                for i in elements:
                    name = i['provider']['name']['full']
                    name = name.replace(' ', '%20')
                    id = i['provider']['id']
                    doc_url = base_url + name + '/' + str(id)
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
