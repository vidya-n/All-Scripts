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
        offset = 0
        while page_count <= 1093:
            print("test")
            url = f'https://doctors.intermountainhealth.org/api/searchservice-v9/sclhealth/providers?filter=provider.direct_book_capable%3Atrue&facet=provider.id&categories=primary_care%2Cspecialties%2Cprovider_name%2Cnetwork_affiliation%2Clocation_name%2Cclinical_keywords&sort=networks%2Crelevance%2Cavailability_density_best%2Cdistance&search_alerts=false&shuffle_seed=179cc884-f3d3-4ef6-a90e-8de074f5711a&provider_fields=-clinical_keywords&page={page_count}&context=sclhealth_pmc&tracking_token=36d281e5-9329-4f62-8b83-4f1cedc967bb&search_token=4ec8160e-b4e6-4bbd-b5dd-8f025de57c94&user_id=dc69050b-62fd-5aba-abec-07626d2b19a8&user_token=96304517-adb7-4e56-878d-9a4bf2e886b1&per_page=50&exclude_from_analytics=true'
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': f'https://doctors.intermountainhealth.org/search?categories=primary_care%2Cspecialties%2Cprovider_name%2Cnetwork_affiliation%2Clocation_name%2Cclinical_keywords&sort=networks%2Crelevance%2Cavailability_density_best%2Cdistance&search_alerts=false&shuffle_seed=179cc884-f3d3-4ef6-a90e-8de074f5711a&provider_fields=-clinical_keywords&page={page}',
                'Cookie': 'consumer_user_token=96304517-adb7-4e56-878d-9a4bf2e886b1; visid_incap_2929202=Xo8tVbA+Spy/s3JvHMRmW6cHHGYAAAAAQUIPAAAAAABYNOrHlkv+MwO0+ZVNeMKM; _ga=GA1.2.257996919.1713113000; _ga_F212BGZP7G=GS1.1.1713113000.1.1.1713113305.0.0.0; _ga_P4V7FRH4LF=GS1.1.1713113000.1.1.1713113305.60.0.0; consumer_tracking_token=36d281e5-9329-4f62-8b83-4f1cedc967bb; search_shuffle_token=179cc884-f3d3-4ef6-a90e-8de074f5711a; nlbi_2929202=j/6PC4ZeIHwAySSkTpyrFwAAAAA91QzRwvFQiF2iD9gJHxCK; incap_ses_1438_2929202=hF+lRBqTTSDZJi83dM30E5o4cGYAAAAAYeFzRfQmqXrEK6p2Ncczuw==; incap_ses_385_2929202=2WMif+hR0BgH0BsajctXBS9GcGYAAAAAk1+r0aqXVheOCChLgNLbkA==; incap_ses_2103_2929202=t7cAFgxeYkyHtWhEblsvHW7icGYAAAAAnEO250dLE20uXiLLBrxzUg==; incap_ses_239_2929202=eJnNQFczHDa6xNrQUBlRA4AZcWYAAAAA+9izlRw3mJD+7A4HSFR47g==; reese84=3:A9fhHGZ/mHn2DxFPO5MGXQ==:8QVIaEdctvqDCYhYdBiVcRoSvZzifP+Op4zDnYpCmOgh0mj1N0SfRpmmOJYnhFhCfXqZHHH45iPjs4ekkrTgIANozDybF4853QH44sWZB+GTWEwrFV1cFep4TBiOAeLgTjT2Ca+OCXyxQl2uw1efuZfFKIv7FW/ZGyZPr7EVIuNqrNZxGBcdVNKbpDJb6uPzsdZ+Q+xI+mSED+MpQeWPqhU3wFBLR2TFE4F+GeXYiBZd1vOXj8BKp76ukRXebdh8E/xuYtMATZTITpHrEG5vCXJuuMACKX5bvxRNAWkAmMfWuzuksrlKsrqxMj94cOJsz+DsS0+a1G37sclqsTL5l/N5cO/J94C7uOlsEUYpN190aDPOQuTMLHqUoqUs/1xH0lX8c9j22c4hC3dO+SzWdCeT2pU6BR5p5k1EeW/oWT3nBY/dH+9xCGiB3RnSGtyPnEo/Q5T/hHfMlmDJUycOPEoHgIMOG05vSVt+npGXT/Q=:MjKc3mwIfH0FMLMnalOqHi/NXmhssLgzbfH+DpK3EEc=; nlbi_2929202_2147483392=gOZDSk+wg0vKx2dATpyrFwAAAAAwtcdBXJRmyvOhCF5j7jO1; utag_main=v_id:019026329e3e0022512e92938d380506f003806700978$_sn:2$_se:6$_ss:0$_st:1718689982546$dc_visit:2$ses_id:1718688135953%3Bexp-session$_pn:2%3Bexp-session$source:direct%3Bexp-session$medium:direct%3Bexp-session$dc_event:6%3Bexp-session$dc_region:us-west-2%3Bexp-session',
                'Sec-Cha-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'Sec-Cha-Ua-Mobile': '?0',
                'Sec-Cha-Ua-Platform': '"Windows"',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'X-Consumer-Groups': 'sclhealth',
                'X-Consumer-Username': 'pmc',
                'X-Csrf-Header': 'sclhealth',
                'X-Requested-With': 'XMLHttpRequest'
            }
            r = requests.get(url, headers=headers) # type: ignore
            elements = r.json()['_result']
            if elements:
                for i in elements:
                    p_url = i['provider']['pmc_url'] 
                    print(p_url)
                    if p_url is None:
                        pass
                    else:
                        doc_url = p_url.replace(' ', '%20')
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
