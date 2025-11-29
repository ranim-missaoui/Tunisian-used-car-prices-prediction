import joblib
import pandas as pd
import numpy as np
import os

MODEL_PATH = "model/best_rf_model.pkl"
LUXURY_BRANDS = ["Mercedes-Benz", "BMW", "Audi", "Porsche", "Lexus", "Land Rover", "Range Rover", "Jaguar"]

if not os.path.exists(MODEL_PATH):
    print(f"Model not found: {MODEL_PATH}")
    exit(1)
model = joblib.load(MODEL_PATH)


from preprocess import load
df = load()
brand_to_models = df.groupby("Brand")["Model"].apply(lambda x: sorted(set(x.str.title()))).to_dict()
all_brands = sorted(brand_to_models.keys())
print("data loaded")


print("\nTunisian Used Car Price Predictor")
print("=" * 60)

while True:
    brand = input(f"\nBrand ({', '.join(all_brands[:8])}...): ").strip().title()
    if not all_brands or brand in all_brands:
        break
    print(f"Invalid or rare brand: '{brand}'. Try one of the known brands above.")

if brand in brand_to_models and brand_to_models[brand]:
    valid_models = brand_to_models[brand]
    while True:
        model_name = input(f"Model for {brand} ({', '.join(valid_models[:6])}...): ").strip().title()
        if model_name in valid_models:
            break
        print(f"No {brand} {model_name} found. Known models: {', '.join(valid_models[:10])}...")
else:
    model_name = input(f"Model for {brand}: ").strip().title()  

year = int(input("Year (e.g. 2019): "))
while not (1990 <= year <= 2025):
    year = int(input("Year must be 1990–2025: "))

transmission = input("Transmission (auto/manual): ").strip().lower()
transmission = "auto" if transmission.startswith("a") else "manual"

engine = float(input("Engine size (L, e.g. 1.6): "))
while not (0.8 <= engine <= 6.5):
    engine = float(input("Engine size between 0.8 and 6.5: "))

mileage = int(input("Mileage in KM (e.g. 120000): "))
while mileage < 0 or mileage > 900000:
    mileage = int(input("Mileage 0–900,000 KM: "))

age = 2025 - year
is_luxury = 1 if brand in LUXURY_BRANDS else 0
is_very_new = 1 if age <= 2 else 0
is_old = 1 if age >= 15 else 0
luxury_x_new = is_luxury * is_very_new



input_df = pd.DataFrame([{
    "Brand": brand,
    "Model": model_name,
    "Transmission": transmission,
    "Age": age,
    "Engine_size": engine,
    "Is_Luxury": is_luxury,
    "Is_Very_New": is_very_new,
    "Is_Old": is_old,
    "Luxury_x_New": luxury_x_new
}])

pred_log = model.predict(input_df)[0]
price = np.expm1(pred_log)

print("\n" + "=" * 60)
print(f"   {brand} {model_name} {year}")
print(f"   {engine}L • {mileage:,} km • {transmission.upper()}")
print(f"   Age: {age} year(s) • {'LUXURY' if is_luxury else 'Standard'}")
print("-" * 60)
print(f"   PREDICTED PRICE: {price:,.0f} DT")
print(f"   (error ~20k DT)")
print("=" * 60)