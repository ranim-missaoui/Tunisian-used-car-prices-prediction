from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import re


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
cars = []
page = 1 
while page <= 100:
    print(f"Scraping page {page}...")
    url = f"https://www.automobile.tn/fr/occasion/{page}"
    r = requests.get(url , headers = headers)
    soup = BeautifulSoup(r.text, "html.parser")
    links = [f"https://www.automobile.tn" + a["href"] for a in soup.select("a.occasion-link-overlay")]

    for link in links:
        r2 = requests.get(link, headers = headers)
        soup2 = BeautifulSoup(r2.text, "html.parser")

        model_elem = soup2.select_one("h1.occasion-title")
        price_elem = soup2.select_one("div.price")

        spec_names = soup2.select(".spec-name")
        spec_values = soup2.select(".spec-value")

        specs = {}
        for name, value in zip(spec_names, spec_values):
            clean_name = name.text.strip().replace("\n", "")
            clean_value = value.text.strip().replace("\n", "")
            specs[clean_name] = clean_value


        
        year = None
        mileage = None

        for name, value in zip(spec_names, spec_values):
            clean_name = name.get_text(strip=True).lower().replace("\n", "")
            clean_value = value.get_text(strip=True).replace("\n", "")

            if "mise en circulation" in clean_name:
                match = re.search(r"(\d{4})$", clean_value)  #grabs last 4 digits, format in site is mm.yyyy
                if match:
                    year = int(match.group(1))

            if "kilométrage" in clean_name or "kilometrage" in clean_name:
                digits = re.sub(r"[^\d]", "", clean_value)
                if digits:
                    mileage = int(digits)




        model = model_elem.text.strip() if model_elem else "N/A"


        price_text = price_elem.text.strip() if price_elem else "N/A"
        price = re.sub(r"[^\d]", "", price_text)
        print("stripped all elts")


        cars.append({
            "URL" : link, #LINK IS IMPORTANT TO APPLY CHANGES TO DATASET
            "Model_raw": model,
            "price in DT": price,
            "Mileage in KM": mileage,
            "Year": year
            })
        
        print("appended!")

        time.sleep(0.1)

    print(f"page {page} completed!")
    page += 1





df = pd.DataFrame(cars)
print(df.head())

df.to_excel('cars_raw_full.xlsx' , index=False)
    



