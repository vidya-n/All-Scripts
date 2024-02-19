# Getting all the doctor urls from the website

import requests
from bs4 import BeautifulSoup

domain  = "https://www.adventhealth.com"
doctor_urls = []

for i in range(1, 27):
    search = "https://www.adventhealth.com/hospital/adventhealth-wesley-chapel/find-doctors"

    response = requests.get(search)
    soup = BeautifulSoup(response.content, "html.parser")
    #print(soup.prettify())

    doctors = soup.find_all('div', {'class': 'physician-block__cta'})
    #print(len(doctors))
    

    for doctor in doctors:
        for link in doctor.find_all('a', href=True):
            doctor_urls.append(domain + link['href'])
    #print(f"Page {i} done")
print(len(doctor_urls))
print(doctor_urls)
