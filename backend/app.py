from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)
CORS(app)

# =========================
# LOAD MODEL
# =========================

model = joblib.load("extratrees_resale_model.pkl")
model_columns = joblib.load("model_columns.pkl")

# =========================
# PREDICT
# =========================

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    screen_size = float(data["screen_size"])
    rear_camera_mp = float(data["rear_camera_mp"])
    front_camera_mp = float(data["front_camera_mp"])
    internal_memory = float(data["internal_memory"])
    ram = float(data["ram"])
    battery = float(data["battery"])
    weight = float(data["weight"])
    release_year = int(data["release_year"])
    days_used = float(data["days_used"])

    new_price = float(data["normalized_new_price"])

    fourg = int(data["fourg"])
    fiveg = int(data["fiveg"])

    brand = data["brand"]
    os_name = data["os"]

    normalized_new_price = np.log(new_price)

    current_year = 2026

    device_age = current_year - release_year

    usage_ratio = (
        days_used /
        (device_age * 365 + 1)
    )

    camera_total = (
        rear_camera_mp +
        front_camera_mp
    )

    battery_per_weight = (
        battery /
        weight
    )

    ram_storage_ratio = (
        ram /
        (internal_memory + 1)
    )

    storage_ram_product = (
        internal_memory *
        ram
    )

    camera_per_storage = (
        camera_total /
        (internal_memory + 1)
    )

    battery_age_ratio = (
        battery /
        (device_age + 1)
    )

    days_used_per_year = (
        days_used /
        (device_age + 0.1)
    )

    price_per_storage = (
        normalized_new_price /
        (internal_memory + 1)
    )

    price_per_ram = (
        normalized_new_price /
        (ram + 1)
    )

    battery_screen_ratio = (
        battery /
        screen_size
    )

    camera_ram_product = (
        camera_total *
        ram
    )

    storage_per_age = (
        internal_memory /
        (device_age + 1)
    )

    battery_ram_product = (
        battery *
        ram
    )

    row = {}

    for col in model_columns:
        row[col] = 0

    row["screen_size"] = screen_size
    row["4g"] = fourg
    row["5g"] = fiveg
    row["rear_camera_mp"] = rear_camera_mp
    row["front_camera_mp"] = front_camera_mp
    row["internal_memory"] = internal_memory
    row["ram"] = ram
    row["battery"] = battery
    row["weight"] = weight
    row["release_year"] = release_year
    row["days_used"] = days_used
    row["normalized_new_price"] = normalized_new_price

    row["device_age"] = device_age
    row["usage_ratio"] = usage_ratio
    row["camera_total"] = camera_total
    row["battery_per_weight"] = battery_per_weight
    row["ram_storage_ratio"] = ram_storage_ratio
    row["storage_ram_product"] = storage_ram_product
    row["camera_per_storage"] = camera_per_storage
    row["battery_age_ratio"] = battery_age_ratio
    row["days_used_per_year"] = days_used_per_year
    row["price_per_storage"] = price_per_storage
    row["price_per_ram"] = price_per_ram
    row["battery_screen_ratio"] = battery_screen_ratio
    row["camera_ram_product"] = camera_ram_product
    row["storage_per_age"] = storage_per_age
    row["battery_ram_product"] = battery_ram_product

    brand_col = "device_brand_" + brand

    if brand_col in row:
        row[brand_col] = 1

    if os_name == "iOS":
        if "os_iOS" in row:
            row["os_iOS"] = 1

    elif os_name == "Windows":
        if "os_Windows" in row:
            row["os_Windows"] = 1

    else:
        if "os_Others" in row:
            row["os_Others"] = 1

    X = pd.DataFrame([row])

    pred_log = model.predict(X)[0]

    resale_value = round(
        np.exp(pred_log) * 86,
        2
    )

    gold = 0.034
    silver = 0.35
    copper = 15
    lithium = 3

    recycling_value = round(
        gold * 9000 +
        silver * 100 +
        copper * 0.8 +
        lithium * 40,
        2
    )

    if resale_value > recycling_value * 3:
        recommendation = "Resell Recommended"
    else:
        recommendation = "Recycle Recommended"

    return jsonify({

        "resale_value": resale_value,
        "recycling_value": recycling_value,
        "recommendation": recommendation,

        "gold": gold,
        "silver": silver,
        "copper": copper,
        "lithium": lithium

    })


if __name__ == "__main__":
    app.run(debug=True)