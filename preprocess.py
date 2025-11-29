import pandas as pd

ALL_BRANDS = ["Mercedes-Benz","BMW","Audi","Volkswagen","Porsche","Mini","Toyota","Lexus","Nissan","Mitsubishi","Suzuki","Mazda","Hyundai","Kia","Genesis","Peugeot","Renault","Citroën","DS","Dacia","Fiat","Alfa Romeo","Jeep","Abarth","Ford","Chevrolet","Land Rover","Range Rover","Jaguar","Volvo","Skoda","Seat","Opel","Chery","Haval","Great Wall","Changan","JAC","Geely","BYD","MG","DFSK","FAW","BAIC","HAVAL","Isuzu","Mahindra","Tata","SsangYong","Ram"]
LUXURY_BRANDS = ["Mercedes-Benz", "BMW", "Audi", "Porsche", "Lexus", "Land Rover", "Range Rover", "Jaguar"]

def load():
    df = pd.read_excel("cars_cleaned_full.xlsx")
    
    if "Model_raw" in df.columns:
        df = df.drop(columns=["Model_raw"])
    
    cols = ["Brand", "Model", "Year", "HP", "Engine_size", "Transmission", "Mileage in KM", "price in DT"]
    df = df[cols].copy()
    
    print("Missing values before cleaning:")
    print(df.isnull().sum())
    
    df["Brand"] = df["Brand"].str.strip().str.title()
    df = df[df["Brand"].isin(ALL_BRANDS)].copy()

    df["Model"] = df["Model"].astype(str).apply(lambda x: " ".join(x.split()[:2]))
    
    df["Transmission"] = df["Transmission"].str.lower().str.strip()
    df["Transmission"] = df["Transmission"].map({
        "auto": "auto", "automatique": "auto", "automatic": "auto",
        "manuelle": "manual", "manual": "manual"
    }).fillna("manual")
    
    df["Engine_size"] = pd.to_numeric(df["Engine_size"], errors='coerce')
    df["Mileage in KM"] = pd.to_numeric(df["Mileage in KM"], errors='coerce')
    df["price in DT"] = pd.to_numeric(df["price in DT"], errors='coerce')
    df["Year"] = pd.to_numeric(df["Year"], errors='coerce')
    df["Age"] = 2025 - df["Year"]
    
    df = df.drop(columns=["HP"])
    df["Engine_size"] = df["Engine_size"].fillna(df["Engine_size"].median())
    df = df.dropna().reset_index(drop=True)
    print(df.isnull().sum())


    df["Is_Luxury"] = df["Brand"].isin(LUXURY_BRANDS).astype(int)
    
    final_cols = ["Brand", "Model", "Age", "Engine_size", "Transmission", "Mileage in KM", "Is_Luxury", "price in DT"]
    df = df[final_cols]
    
    return df



df = load()
print(f"\nClean dataset ready: {len(df)} cars")
print(f"Unique Brands : {df['Brand'].nunique()}")
print(f"Unique Models : {df['Model'].nunique()}")
print("\nFirst 10 rows:")
print(df.head(10))
print("\nStats:")
print(df.describe())