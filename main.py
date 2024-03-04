import pandas as pd
import requests
from threading import Thread
import time
import re
import os


from models import Apartment

class Scraping:
    def __init__(self, targetURL) -> None:
        self.targetURL = targetURL
        self.apartments = list()

    def get_advertisement(self):
        try:
            siteInfo = requests.get(self.targetURL, timeout=10)
            siteInfo.raise_for_status()
            return siteInfo
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def extraction_advertisement(self, htmlContent):
        title_pattern = re.compile(r'<h2 class="kt-post-card__title">([^<]+)<\/h2>')
        price_pattern = re.compile(r'<div class="kt-post-card__description">([^<]+)<\/div>')
        link_pattern = re.compile(r'<a class="" href="([^"]+)">')

        title_matches = title_pattern.finditer(htmlContent)
        price_mathces = price_pattern.finditer(htmlContent)
        link_matches = link_pattern.finditer(htmlContent)

        for title_match, price_match, link_match in zip(title_matches, price_mathces, link_matches):
           self.add_apartment(title_match.group(1), price_match.group(1),"https://divar.ir"+ link_match.group(1))


    def add_apartment(self, title, price, link):
        newApartment = Apartment(title, price, link)
        self.apartments.append(newApartment)

    def save_to_file(self, filePath):
        try:
            df = pd.DataFrame([(ad.title, ad.price, ad.link) for ad in self.apartments], columns=['Title', 'Price', 'Link'])
            df.to_excel(filePath, index=False)
            self.apartments = []
        except Exception as e:
            print(f"Error: {e}")

    def delete_file(self,filePath):
        if os.path.exists(filePath):
            os.remove(filePath)


def scrape_divar(targetURL, filePath):
    print("Starting Scrape Your Site")
    divar = Scraping(targetURL=targetURL)
    siteInfo = divar.get_advertisement()

    if siteInfo and siteInfo.status_code == 200:
        divar.extraction_advertisement(siteInfo.text)
        divar.save_to_file(filePath)
    else:
        print("Failed to retrieve HTML content.")

if __name__ == "__main__":
    targetURL = "https://divar.ir/s/tehran/buy-apartment/navvab?districts=1006%2C197%2C275%2C284%2C94&price=1800000000-2500000000"
    filePath = "ScrapDivar.xlsx"

    while True:
        ThreadReceiveNewAdvertisement = Thread(target=scrape_divar, args=(targetURL, filePath))
        ThreadReceiveNewAdvertisement.start()
        time.sleep(1800)
