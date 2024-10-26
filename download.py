import csv
import requests
import os
from bs4 import BeautifulSoup

def fetch_images_from_url(url, path):
    if not os.path.exists(path):
        os.makedirs(path)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    count = 1
    for div in soup.find_all("div", {"class": "mta-gallery-image"}):
        image_url = div['style'].replace('background-image: url(', '').replace(')', '')
        response = requests.get(image_url.strip())
        with open(os.path.join(path, str(count) + ".jpg"), "wb") as file:
            file.write(response.content)
            count += 1
    for img in soup.find_all("img", {"class": "img-responsive"}):
        image_url = img['src']
        response = requests.get(image_url)
        with open(os.path.join(path, str(count) + ".jpg"), "wb") as file:
            file.write(response.content)
            count += 1

with open('mta.csv', 'r') as csv_file:
    csv_data = csv.DictReader(csv_file)
    for row in csv_data:
        if row['Art Image Link']:
            fetch_images_from_url(row['Art Image Link'], row['Unique ID'])

