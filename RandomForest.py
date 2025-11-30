from preprocess import load
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np
import pandas as pd
import joblib
import os

df = load()
print(df.head())
df["Is_Very_New"]       = (df["Age"] <= 2).astype(int)
df["Is_Old"]            = (df["Age"] >= 15).astype(int)
df["Luxury_x_New"]      = df["Is_Luxury"] * df["Is_Very_New"]
categorical_cols = ["Brand", "Model", "Transmission"]
numerical_cols = [
    "Age", "Engine_size", "HP",
    "Is_Luxury", "Is_Very_New", "Is_Old", "Luxury_x_New"
] #removed data leakage

X = df[numerical_cols+categorical_cols]
y = df["price in DT"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)



preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols),
        ('num', 'passthrough', numerical_cols)
    ],
)

rf_pipeline = Pipeline([
    ('prep', preprocessor),
    ('model', RandomForestRegressor(
        n_estimators=2800,
        max_depth=35,
        min_samples_leaf=1,
        min_samples_split=2,
        max_features=0.45,
        random_state=42,
        n_jobs=-1,
        bootstrap=True,
        ccp_alpha=0.00005

    ))
])

y_train_log = np.log1p(y_train)
rf_pipeline.fit(X_train, y_train_log)

pred_log = rf_pipeline.predict(X_test)
pred_rf = np.expm1(pred_log)

print("\nRandom Forest Results (on original price scale):")
print("MAE:", mean_absolute_error(y_test, pred_rf))
print("R²:", r2_score(y_test, pred_rf))

print("\nFirst 10 Predictions vs Actual:")
comparison = pd.DataFrame({
    "Predicted": pred_rf[:10].round(0).astype(int),
    "Actual": y_test[:10].values
})
print(comparison)


os.makedirs("model", exist_ok=True)
joblib.dump(rf_pipeline, "model/best_rf_model.pkl")