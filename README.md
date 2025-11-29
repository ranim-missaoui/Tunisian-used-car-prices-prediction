# Tunisia Used Car Price Predictor  

**open-source car pricing tool for the Tunisian market**  
Real local data • Web scraper • ML model • CLI  

**Current Best Accuracy**  
R² 0.75 → MAE 20.8k DT  


## Features

- Full **automobile.tn web scraper** (BeautifulSoup)  
- preprocessing & feature engineering 
- **Random Forest** trained on log prices : best real-world accuracy  
- **CLI predictor** with full input validation (accurate car brands and models) 
- Pre-trained model included 


## CLI example
Brand (Abarth, Alfa Romeo, Audi, Chery, Chevrolet, Citroën, Dacia, Fiat...): Fiat
Model for Fiat (500, 500 C, 500 Lounge, Ducato, Fiorino, Grande Punto...): Grande Punto
Year (e.g. 2019): 2011
Transmission (auto/manual): manual
Engine size (L, e.g. 1.6): 1
Mileage in KM (e.g. 120000): 200000

============================================================
   Fiat Grande Punto 2011
   1.0L • 200,000 km • MANUAL
   Age: 14 year(s) 
------------------------------------------------------------
   PREDICTED PRICE: 28,752 DT
============================================================
