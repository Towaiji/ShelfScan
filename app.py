import os
import re
from datetime import datetime, timedelta
from flask import Flask, render_template, request
from PIL import Image
import pytesseract
from dotenv import load_dotenv
import requests
from difflib import SequenceMatcher

# Load environment variables
load_dotenv()
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global grocery item list
items = []

# Default expiry estimates (in days)
default_expiry_days = {
    "milk": 7,
    "bread": 3,
    "eggs": 14,
    "cheese": 10,
    "pancakes": 5,
    "coffee": 30,
    "sausage": 7
}

@app.route("/", methods=["GET", "POST"])
def index():
    global items
    scanned_items = []

    if request.method == "POST":
        file = request.files.get("receipt")
        if file:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            try:
                image = Image.open(path)
                text = pytesseract.image_to_string(image).lower()

                print("🧾 OCR Output:\n" + "-"*40)
                print(text)
                print("-"*40)

                found = []
                for line in text.splitlines():
                    line = line.strip()
                    for keyword in default_expiry_days:
                        ratio = SequenceMatcher(None, keyword, line).ratio()
                        if ratio > 0.6 and keyword not in found:
                            expiry_date = datetime.now() + timedelta(days=default_expiry_days[keyword])
                            item_data = {"item": keyword, "expiry": expiry_date.date()}
                            scanned_items.append(item_data)
                            items.append(item_data)
                            found.append(keyword)

                print("📦 Final Items List:")
                for i in items:
                    print(f"- {i['item']} (expires {i['expiry']})")

            except Exception as e:
                return f"❌ Error processing receipt: {e}"

    return render_template("index.html", items=items, scanned=scanned_items)

@app.route("/add", methods=["POST"])
def add():
    global items
    item = request.form.get("item", "").strip().lower()
    expiry = request.form.get("expiry")

    if item:
        if not expiry:
            expiry_date = datetime.now() + timedelta(days=default_expiry_days.get(item, 7))
        else:
            try:
                expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
            except ValueError:
                expiry_date = datetime.now() + timedelta(days=7)

        items.append({"item": item, "expiry": expiry_date.date()})

    return render_template("index.html", items=items, scanned=[])

@app.route("/suggest", methods=["POST"])
def suggest():
    global items
    if not SPOONACULAR_API_KEY:
        return render_template("index.html", items=items, suggestions="⚠️ No API key found.", scanned=[])

    ingredient_list = ",".join([i["item"] for i in items])
    if not ingredient_list:
        return render_template("index.html", items=items, suggestions="No ingredients provided.", scanned=[])

    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredient_list}&number=3&ranking=2&ignorePantry=true&apiKey={SPOONACULAR_API_KEY}"

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        if not data:
            return render_template("index.html", items=items, suggestions="No recipe ideas found 😢", scanned=[])

        suggestions = ""
        for recipe in data:
            title = recipe.get("title")
            used = [i["name"] for i in recipe.get("usedIngredients", [])]
            missed = [i["name"] for i in recipe.get("missedIngredients", [])]
            suggestions += f"🍽️ {title}\nUses: {', '.join(used)}\nNeeds: {', '.join(missed)}\n\n"

        return render_template("index.html", items=items, suggestions=suggestions.strip(), scanned=[])

    except Exception as e:
        return render_template("index.html", items=items, suggestions=f"❌ Error fetching recipes: {e}", scanned=[])

if __name__ == "__main__":
    app.run(debug=True)
