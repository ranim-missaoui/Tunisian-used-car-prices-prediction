import pandas as pd 
import re
pd.set_option("display.max_colwidth", None)



#print(df.head())
#print(df['Model_raw'].head())

#print(df['Model_raw'].head(300))

def extract_brand(text):
    text = str(text)
    brands = ["Mercedes-Benz", "BMW", "Audi", "Volkswagen", "Porsche", "Mini", "Toyota", "Lexus", "Nissan", "Mitsubishi", "Suzuki", "Mazda",
        "Hyundai", "Kia", "Genesis", "Peugeot", "Renault", "Citroën", "DS", "Dacia", "Fiat", "Alfa Romeo", "Jeep", "Abarth",
        "Ford", "Chevrolet", "Land Rover", "Range Rover", "Jaguar", "Volvo", "Skoda", "Seat", "Opel",
        "Chery", "Haval", "Great Wall", "Changan", "JAC", "Geely", "BYD", "MG", "DFSK", "FAW", "BAIC", "HAVAL", "Isuzu", "Mahindra", "Tata",
        "SsangYong", "Ram"]
    for b in brands:
        if text.startswith(b):
            return b
    return text.split()[0]


def extract_engine_size(text):
    if pd.isna(text):
        return None
    text = str(text)
    m = re.search(r"(\d[\.,]\d)", text)
    return m.group(1).replace(",",".") if m else None



def extract_transmission(text):
    text = str(text)
    if "auto" in text.lower():
        return "auto"
    return "man"


def extract_model(text,brand):
    text = str(text)
    t=text.replace(brand,"").strip()
    t = re.split(r"\d[\.,]\d|\d+ch", t)[0]
    t = re.sub(r"automatique|manuelle", "",t, flags=re.IGNORECASE)
    return t.strip()

def clean_model_name(text):
    if pd.isna(text):
        return None

    text = str(text)

    text = text.split("\n")[0]

    text = re.sub(r"\s{2,}", " ", text).strip()

    return text


df = pd.read_excel("cars_scraped_raw.xlsx")
df["Brand"] = df["Model_raw"].apply(extract_brand)
df["Engine_size"] = df["Model_raw"].apply(extract_engine_size)
df["Transmission"] = df["Model_raw"].apply(extract_transmission)
df["Model"] = df.apply(lambda row: extract_model(row["Model_raw"], row["Brand"]), axis=1).apply(clean_model_name)




df.to_excel('cars_cleaned.xlsx' , index=False)



    

