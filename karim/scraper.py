import requests
from bs4 import BeautifulSoup

URL = "https://www.cs.ucsb.edu/"
page = requests.get(URL).text

soup = BeautifulSoup(page, "lxml")

cs_intro = soup.findAll('p')

for pg in cs_intro:
    print(pg.text)
