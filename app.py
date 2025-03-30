from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
import os
import re
from PIL import Image, UnidentifiedImageError
import pytesseract

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# In-memory store
grocery_items = []

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Updated expiry rules including receipt items
expiry_prediction = {
    "coffee": 180,
    "eggs": 14,
    "pancakes": 2,
    "sausage": 7,
    "milk": 7,
    "bread": 5,
    "cheese": 10,
    "chicken": 3,
    "lettuce": 4,
    "tomato": 5,
    "apple": 10,
    "banana": 4,
    "yogurt": 10
}

def predict_expiry(item_name):
    item_name = item_name.lower().strip()
    return expiry_prediction.get(item_name, 7)

def process_receipt(image_path):
    try:
        image = Image.open(image_path).convert("L")
        text = pytesseract.image_to_string(image)
        print("🧾 OCR Output:\n" + "-"*40)
        print(text)
        print("-" * 40)
    except UnidentifiedImageError:
        print(f"❌ Cannot read image: {image_path}")
        return []
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return []

    detected_items = []
    text_lower = text.lower()

    for keyword in expiry_prediction:
        if re.search(rf'\b{keyword}\b', text_lower):
            days = predict_expiry(keyword)
            expiry_date = datetime.now() + timedelta(days=days)
            detected_items.append({
                "name": keyword,
                "expiry": expiry_date.strftime("%Y-%m-%d"),
                "days_left": days
            })

    print(f"✅ Detected: {[item['name'] for item in detected_items]}")
    return detected_items

@app.route("/", methods=["GET", "POST"])
def index():
    global grocery_items

    if request.method == "POST":
        # Manual item
        if "name" in request.form:
            name = request.form["name"]
            expiry_input = request.form.get("expiry")

            if expiry_input:
                expiry_date = datetime.strptime(expiry_input, "%Y-%m-%d")
            else:
                days = predict_expiry(name)
                expiry_date = datetime.now() + timedelta(days=days)

            grocery_items.append({
                "name": name,
                "expiry": expiry_date.strftime("%Y-%m-%d"),
                "days_left": (expiry_date - datetime.now()).days
            })

        # Receipt upload
        elif "receipt" in request.files:
            file = request.files["receipt"]
            if file and allowed_file(file.filename):
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(path)
                scanned = process_receipt(path)
                grocery_items.extend(scanned)
            else:
                return "Unsupported file type", 400

        return redirect("/")

    # Update days left
    for item in grocery_items:
        item["days_left"] = (datetime.strptime(item["expiry"], "%Y-%m-%d") - datetime.now()).days

    grocery_items.sort(key=lambda x: x["days_left"])
    return render_template("index.html", items=grocery_items)

if __name__ == "__main__":
    app.run(debug=True)
