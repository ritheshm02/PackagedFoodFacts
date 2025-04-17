from flask import Flask, request, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

df = pd.read_csv("data/cleaned_data5.csv", low_memory=False)

nutrition_columns = [
    "energy-kcal_value",
    "fat_value",
    "saturated-fat_value",
    "carbohydrates_value",
    "sugars_value",
    "fiber_value",
    "proteins_value",
    "salt_value",
    "sodium_value",
    "trans-fat_value",
    "cholesterol_value",
    "vitamin-a_value",
    "vitamin-c_value",
    "vitamin-d_value",
    "calcium_value",
    "iron_value",
    "potassium_value",
    "omega-3-fat_value",
    "omega-6-fat_value",
]

for col in nutrition_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)


def evaluate_food(row):
    score = 0
    reasons = []

    # Energy (kcal)
    energy = row["energy-kcal_value"]
    if energy > 0:
        if 0 < energy <= 400:
            score += 1
            reasons.append("Moderate calorie content")
        elif energy > 400:
            score -= 1
            reasons.append("High calorie content")

    # Fat
    fat = row["fat_value"]
    if fat > 0:
        if 0 < fat <= 10:
            score += 1
            reasons.append("Moderate fat content")
        elif fat > 20:
            score -= 1
            reasons.append("High fat content")

    # Saturated Fat
    saturated_fat = row["saturated-fat_value"]
    if saturated_fat > 0:
        if 0 < saturated_fat <= 4:
            score += 1
            reasons.append("Low saturated fat")
        elif saturated_fat > 5:
            score -= 1
            reasons.append("High saturated fat")

    # Carbohydrates
    carbohydrates = row["carbohydrates_value"]
    if carbohydrates > 0:
        if 0 < carbohydrates <= 50:
            score += 1
            reasons.append("Moderate carbohydrate content")
        elif carbohydrates > 70:
            score -= 1
            reasons.append("High carbohydrate content")

    # Sugars
    sugars = row["sugars_value"]
    if sugars > 0:
        if 0 < sugars <= 10:
            score += 1
            reasons.append("Low sugar content")
        elif sugars > 15:
            score -= 1
            reasons.append("High sugar content")

    # Fiber
    fiber = row["fiber_value"]
    if fiber > 0:
        if fiber > 3:
            score += 1
            reasons.append("Good source of fiber")
        elif 0 < fiber <= 2:
            score -= 1
            reasons.append("Low fiber content")

    # Protein
    protein = row["proteins_value"]
    if protein > 0:
        if protein > 10:
            score += 1
            reasons.append("Good source of protein")
        elif 0 < protein <= 5:
            score -= 1
            reasons.append("Low protein content")

    # Salt
    salt = row["salt_value"]
    if salt > 0:
        if 0 < salt <= 1.5:
            score += 1
            reasons.append("Low salt content")
        elif salt > 2:
            score -= 1
            reasons.append("High salt content")

    # Trans fat
    trans_fat = row["trans-fat_value"]
    if trans_fat >= 0:
        if trans_fat == 0:
            score += 1
            reasons.append("No trans fat")
        elif trans_fat > 0:
            score -= 2
            reasons.append("Contains trans fat")

    # Cholesterol
    cholesterol = row["cholesterol_value"]
    if cholesterol > 0:
        if 0 < cholesterol <= 20:
            score += 1
            reasons.append("Low cholesterol")
        elif cholesterol > 60:
            score -= 1
            reasons.append("High cholesterol")

    # Omega-3 Fatty Acids
    omega_3_fat = row["omega-3-fat_value"]
    if omega_3_fat > 0:
        if omega_3_fat >= 1:
            score += 1
            reasons.append("Good source of omega-3 fatty acids")
        elif omega_3_fat < 0.1:
            score -= 1
            reasons.append("Low omega-3 fatty acids")

    # Omega-6 Fatty Acids
    omega_6_fat = row["omega-6-fat_value"]
    if omega_6_fat > 0:
        if omega_6_fat >= 1:
            score += 1
            reasons.append("Good source of omega-6 fatty acids")
        elif omega_6_fat < 0.1:
            score -= 1
            reasons.append("Low omega-6 fatty acids")

    # Vitamins and Minerals
    nutrients = [
        "vitamin-a_value",
        "vitamin-c_value",
        "vitamin-d_value",
        "calcium_value",
        "iron_value",
        "potassium_value",
    ]
    nutrient_names = [
        "Vitamin A",
        "Vitamin C",
        "Vitamin D",
        "Calcium",
        "Iron",
        "Potassium",
    ]

    for nutrient, name in zip(nutrients, nutrient_names):
        value = row[nutrient]
        if value > 0:
            score += 0.5
            reasons.append(f"Contains {name}")

    # Categorize based on score
    if score > 5:
        category = "Excellent"
    elif score > 2:
        category = "Good"
    elif score > -2:
        category = "Moderate"
    else:
        category = "Poor"

    return pd.Series([category, score, ", ".join(reasons)])


def get_recommendations(food):
    recommendations = []

    if food["Category"] == "Poor":
        recommendations.append(
            "This product has a poor nutritional profile. Consider limiting its consumption."
        )
    elif food["Category"] == "Moderate":
        recommendations.append(
            "This product has a moderate nutritional profile. It can be consumed in moderation as part of a balanced diet."
        )
    elif food["Category"] == "Good":
        recommendations.append(
            "This product has a good nutritional profile. It can be a healthy part of your diet."
        )
    else:
        recommendations.append(
            "This product has an excellent nutritional profile. It's a great choice for a healthy diet."
        )

    # Add specific recommendations
    if food["fat_value"] > 20:
        recommendations.append(
            "This product is high in fat. Consider alternatives with less fat or consume in moderation."
        )
    if food["sugars_value"] > 15:
        recommendations.append(
            "This product is high in sugar. Look for options with less added sugar or limit consumption."
        )
    if food["salt_value"] > 2:
        recommendations.append(
            "This product is high in salt. Try to limit your intake to maintain healthy blood pressure."
        )
    if food["fiber_value"] < 2:
        recommendations.append(
            "This product is low in fiber. Consider adding high-fiber foods to your diet for digestive health."
        )
    if food["trans-fat_value"] > 0:
        recommendations.append(
            "This product contains trans fat. It's recommended to avoid or minimize consumption of trans fats."
        )
    if food["cholesterol_value"] > 60:
        recommendations.append(
            "This product is high in cholesterol. If you have concerns about cholesterol, consult with a healthcare professional."
        )

    return "\n".join(recommendations)


def get_food_info(query):
    # Search by barcode or product name
    food = df[df["code"] == query]
    if food.empty:
        food = df[df["product_name_en"].str.contains(query, case=False, na=False)]
        if food.empty:
            return None

    food = food.iloc[0]
    evaluation = evaluate_food(food)
    food["Category"], food["Score"], food["Reasons"] = evaluation

    # Handle NaN values
    food = food.fillna("N/A")

    recommendations = get_recommendations(food)
    return {
        "product_name": (
            food["product_name_en"] if food["product_name_en"] != "N/A" else "N/A"
        ),
        "brand": food["brands"] if food["brands"] != "N/A" else "N/A",
        "category": food["Category"],
        "score": food["Score"],
        "reasons": food["Reasons"],
        "nutritional_info": {
            "Energy": f"{food['energy-kcal_value']} kcal",
            "Fat": f"{food['fat_value']}g",
            "Saturated Fat": f"{food['saturated-fat_value']}g",
            "Carbohydrates": f"{food['carbohydrates_value']}g",
            "Sugars": f"{food['sugars_value']}g",
            "Fiber": f"{food['fiber_value']}g",
            "Protein": f"{food['proteins_value']}g",
            "Salt": f"{food['salt_value']}g",
            "Trans Fat": f"{food['trans-fat_value']}g",
            "Cholesterol": f"{food['cholesterol_value']}mg",
            "Vitamin A": f"{food['vitamin-a_value']}µg",
            "Vitamin C": f"{food['vitamin-c_value']}mg",
            "Vitamin D": f"{food['vitamin-d_value']}µg",
            "Calcium": f"{food['calcium_value']}mg",
            "Iron": f"{food['iron_value']}mg",
            "Potassium": f"{food['potassium_value']}mg",
        },
        "recommendations": recommendations,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]
        food_info = get_food_info(query)
        return render_template("index.html", food_info=food_info)
    return render_template("index.html", food_info=None)


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        # query = request.form["query"]
        # food_info = get_food_info(query)
        return render_template("feedback.html")
    return render_template("feedback.html")


if __name__ == "__main__":
    app.run(debug=True)
