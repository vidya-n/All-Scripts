# Doctor urls with load more - all doctors

import requests
from bs4 import BeautifulSoup

# URL from the AJAX request when clicking "Load More"
url = "https://doctors.summithealthcare.net/find_a_doctor/locations/show_low/"

# These headers and params are just examples, you need to get them from the actual request
headers = {"User-Agent": "Mozilla/5.0"}
#params = {"page": 3}  # This might be how the website keeps track of pagination


response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")
#print(soup.prettify())

doctor_urls = []
page_count = 6
sum = 20
load_more_a = soup.find('a', {'class': 'drts-view-nav-item-name-load_more'})
load_more = load_more_a['href']
for i in range(1, page_count+1):
    modified_href = load_more.replace("page=2", f"page={i}")
    #print(modified_href)
    response = requests.get(modified_href, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    doctors = soup.find_all('div', {'data-name': 'entity_field_post_title'})
    for doctor in doctors:
        for link in doctor.find_all('a', href=True):
            doctor_urls.append(link['href'])


print(len(doctor_urls))
for i in doctor_urls:
    print(i)
