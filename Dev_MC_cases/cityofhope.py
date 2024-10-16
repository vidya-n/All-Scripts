import requests
import json
import time
import hashlib
from bs4 import BeautifulSoup as bs

from custom_scripts.base_script import BaseScript
from selenium.webdriver.common.by import By

class Cityofhope(BaseScript):
    
    def process_data(self):
        profiles = []
        page_count = 0
        base = 'https://www.cityofhope.org'
        print("hitting the url")
        while page_count <= 153:
            url = f'https://www.cityofhope.org/patients/find-a-doctor?page={page_count}'
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'max-age=0',
                'Cookie': '__cf_bm=qSaOckWks0nbovDEavEXxUXnIWmr_9bTXl3teVerj3o-1727263909-1.0.1.1-.Fv_TlmvmBBiN435OaBrGO7QhFhggsjuIShek_feP3tmfvww9H3W3aHPi9rKK_cvpkqgEPyh54DFOEIQt7x21w; _gcl_au=1.1.239578492.1727263910; _ga=GA1.1.2072042580.1727263911; cf_clearance=RKQwREI8f6EXA6mLizmnj02zMfCqgU4PIV9n7DoeKxU-1727263912-1.2.1.1-W3ukPoL1_g2B0xSTQsaDaJOZbEsn71x4wjqTeuGuO3.MSx_jwDZWcrvsCvFr.UckXu_uaCO3JAjcc5HIqNlv4O_fi9UokO4u81kWHnyjy1UrzYi0Yo7um7xDx4B7Z7RILSBKQ48BfNH6qJTeKg908ElI1tOTNQEPoshYtuhy02CUvjFJ2qu6ChMc5aZOtZOKBojTvX.O29w_PdOd2jM1Bat3dtB0LkkzmP3awIPFyTz9v4E_95BM3S6cjwmuqFjW9RPRivSqSoihzEbAu2cyPpBgjFq8gI0QJBOKHMhe1TwF_jcAw7mvxlFf4UPuA8qK_Tl8CKwSU1nltubdr2C8lgiDALsOkWXRYbaKMG8SgAS8kAB1pmcUDoO9_RnZpTkz; _ga_K625FN3PRT=GS1.1.1727263911.1.0.1727263911.0.0.0; invoca_session=%7B%22ttl%22%3A%222024-09-26T11%3A33%3A50.917Z%22%2C%22session%22%3A%7B%22abtasty_vid%22%3A%22na%22%2C%22campaign%22%3A%22unknown%22%2C%22content%22%3A%22non_branded%22%2C%22current_page%22%3A%22https%3A%2F%2Fwww.cityofhope.org%2Fpatients%2Ffind-a-doctor%22%2C%22current_path%22%3A%22%2Fpatients%2Ffind-a-doctor%22%2C%22dc_id%22%3A%22na%22%2C%22entry_page%22%3A%22https%3A%2F%2Fwww.cityofhope.org%2Fpatients%2Ffind-a-doctor%22%2C%22gclid%22%3A%22na%22%2C%22host%22%3A%22www.cityofhope.org%22%2C%22medium%22%3A%22organic%22%2C%22referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22referring_domain%22%3A%22www.google.com%22%2C%22session_campaign%22%3A%7B%22sourcecode%22%3A%22non_branded_natural_search_google%22%2C%22invsrc%22%3A%22na%22%2C%22utm_source%22%3A%22na%22%2C%22utm_medium%22%3A%22na%22%2C%22utm_campaign%22%3A%22na%22%2C%22utm_content%22%3A%22na%22%2C%22utm_term%22%3A%22na%22%2C%22t_pur%22%3A%22na%22%2C%22t_si%22%3A%22na%22%2C%22t_plc%22%3A%22na%22%2C%22t_sz%22%3A%22na%22%2C%22t_con%22%3A%22na%22%2C%22t_ctv%22%3A%22na%22%2C%22t_src%22%3A%22na%22%2C%22t_cam%22%3A%22na%22%2C%22t_adg%22%3A%22na%22%2C%22t_trm%22%3A%22na%22%2C%22t_mtp%22%3A%22na%22%2C%22t_pos%22%3A%22na%22%2C%22t_mdm%22%3A%22na%22%2C%22t_crt%22%3A%22na%22%7D%2C%22site_activities%22%3A%7B%22session_counter%22%3A1%2C%22session_pages_seen%22%3A1%2C%22total_pages_seen%22%3A1%2C%22first_session_start_time%22%3A%222024-09-25T11%3A31%3A50.474Z%22%2C%22session_start_time%22%3A%222024-09-25T11%3A31%3A50.474Z%22%2C%22visitor_type%22%3A%22new%22%2C%22session_current_time%22%3A%222024-09-25T11%3A31%3A50.474Z%22%2C%22session_duration%22%3A0%2C%22recency%22%3A0%2C%22contact_freq%22%3A%220%22%2C%22contact_freq_type%22%3A%22na%22%2C%22last_session_start_time%22%3A%22na%22%7D%2C%22site_interests%22%3A%7B%22cancer%22%3A%22na%22%2C%22hospital%22%3A%22na%22%2C%22survivor%22%3A%22no%22%2C%22become_patient%22%3A%22no%22%2C%22insurance%22%3A%22no%22%7D%2C%22source%22%3A%22google%22%2C%22source_code%22%3A%22non_branded_natural_search_google%22%2C%22t_pos%22%3A%22na%22%2C%22ua%22%3A%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F128.0.0.0%20Safari%2F537.36%22%2C%22ga_measurement_id%22%3A%22G-K625FN3PRT%22%2C%22utm_medium%22%3A%22organic%22%2C%22utm_source%22%3A%22google.com%22%2C%22invoca_id%22%3A%22i-65721652-d6ae-4ddd-eafd-97c9c73295db%22%2C%22ga_session_id%22%3A%221727263911%22%2C%22g_cid%22%3A%222072042580.1727263911%22%7D%2C%22config%22%3A%7B%22ce%22%3Atrue%2C%22fv%22%3Afalse%2C%22rn%22%3Afalse%7D%7D',
                'Sec-Cha-Ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                'Sec-Cha-Ua-Mobile': '?0',
                'Sec-Cha-Ua-Platform': "Windows",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
            }
            #print("Hitting URL: ", url)
            r = requests.get(url, headers=headers)
            
            """if r.status_code != 200:
                print(f"Failed to retrieve page {page}. Status code: {r.status_code}")
                break"""
            
            soup = bs(r.content, 'html.parser')
            elements = soup.find_all('a', class_='field--name-title')
            
            for i in elements:
                doc_url = base + i.get('href')
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
