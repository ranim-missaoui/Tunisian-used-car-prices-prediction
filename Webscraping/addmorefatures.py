from bs4 import BeautifulSoup
import requests
import re
import pandas as pd



headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

df = pd.read_excel("cars_raw_full.xlsx")

links = df["URL"]
horsepowers = []
i=0
for link in links:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    spec_names = soup.select(".spec-name")
    spec_values = soup.select(".spec-value")

    HorsePower = None
    for name, value in zip(spec_names, spec_values):
        clean_name = name.get_text(strip=True).lower()
        if "puissance fiscale" in clean_name:
            digits = re.findall(r'\d+', value.get_text(strip=True))
            if digits:
                HorsePower = int(digits[0])
                break           
    horsepowers.append(HorsePower)
    i=i+1
    print(f"{i} : {HorsePower}")
df['HP'] = horsepowers



df.to_excel("cars_with_hp_and.xlsx", index=False)
