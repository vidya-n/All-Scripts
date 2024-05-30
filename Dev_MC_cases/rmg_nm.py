from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import hashlib
import requests
import json


from custom_scripts.base_script import BaseScript


class Ochsner(BaseScript):
          
    def process_data(self):
        count = 1
        profiles = []
        print("hitting the url")
        #self.driver.get(url)    
        
        while count <= 43:
            print("test")
            page_count = count
            url = f'https://www.nm.org/nm-api/northwestern/physicians/GetPhysicians?latitude=41.8946401&longitude=-87.6211275&medicalgrouplist=nmg&medicalgrouplist=northwesternmedicineregionalmedicalgroup&sort=distance&page={page_count}&pageSize=96'
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cookie': 'ppms_privacy_4abb1e4c-f063-4207-8488-64f5e44dc7cf={%22visitorId%22:%2294e847a5-ac92-40bf-9825-05a3a2acfc7e%22%2C%22domain%22:{%22normalized%22:%22www.nm.org%22%2C%22isWildcard%22:false%2C%22pattern%22:%22www.nm.org%22}%2C%22consents%22:{%22analytics%22:{%22status%22:-1}}%2C%22staleCheckpoint%22:%222024-03-13T04:56:07.608Z%22}; ELOQUA=GUID=78639DCFE3FD4B63982CD62154F8D6DE; _hjSessionUser_1968954=eyJpZCI6Ijg0ODM3NjI1LWQ3Y2ItNTIwNS1iNTUxLTA3NThlN2E1MDY4NyIsImNyZWF0ZWQiOjE3MTAzMDU3NjY1NTEsImV4aXN0aW5nIjp0cnVlfQ==; _sg_b_v=2%3B792%3B1710307715; _hjDonePolls=997955%2C1006138; ppms_privacy_bar_4abb1e4c-f063-4207-8488-64f5e44dc7cf={%22status%22:true%2C%22domain%22:{%22normalized%22:%22www.nm.org%22%2C%22isWildcard%22:false%2C%22pattern%22:%22www.nm.org%22}}; _hjSession_1968954=eyJpZCI6ImU0ODRkM2IxLWRjYjktNGFlYy1iM2EzLWQzNDVmZTU2OWJkOSIsImMiOjE3MTU2Nzg2ODIwNzIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowfQ==; _pk_ses.4abb1e4c-f063-4207-8488-64f5e44dc7cf.e154=*; _pk_id.4abb1e4c-f063-4207-8488-64f5e44dc7cf.e154=f69c97a2f7f1d217.1715678683.1.1715679101.1715678683.; nmuid=0d63b004-d3d5-453e-a5ac-c8f2b13a885f',
                'Referer': f'https://www.nm.org/doctors/search-results?medicalgrouplist=nmg&medicalgrouplist=northwesternmedicineregionalmedicalgroup&sort=distance&page={page_count}&pagesize=96',
                'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
            }
            
            payload = {
                'latitude': '41.8946401',
                'longitude': '-87.6211275',
                'medicalgrouplist': 'nmg',
                'medicalgrouplist': 'northwesternmedicineregionalmedicalgroup',
                'sort': 'distance',
                'page': f'{page_count}',
                'pageSize': '96'
            }
            r = requests.get(url, headers=headers, data=payload, verify=False)
            #time.sleep(5)
            
            
            elements = r.json()['Physicians']
            if elements:
                for i in elements:
                    doc_url = i['DoctorProfileUrl']
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
                #time.sleep(5)
                print(f"Page {page_count} done")
                print(len(profiles))
                count = count + 1
            except Exception as e:
                #print("Pagination failed")
                print(e)
                break
            
            
            if self.check_repeated_pages(profiles):
                break
            # else:
            #     break
            # return profiles
        return self.profiles
