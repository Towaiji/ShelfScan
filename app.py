from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
import os
from PIL import Image
import pytesseract

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# In-memory storage
grocery_items = []

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Expiry prediction rules
expiry_prediction = {
    "milk": 7,
    "bread": 5,
    "eggs": 14,
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
        print(f"Opening image: {image_path}")  # Debug log
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Error reading image: {e}")
        return []

    detected_items = []
    for keyword in expiry_prediction:
        if keyword in text.lower():
            days = predict_expiry(keyword)
            expiry_date = datetime.now() + timedelta(days=days)
            detected_items.append({
                "name": keyword,
                "expiry": expiry_date.strftime("%Y-%m-%d"),
                "days_left": days
            })

    return detected_items

@app.route("/", methods=["GET", "POST"])
def index():
    global grocery_items

    if request.method == "POST":
        # Manual input
        if "name" in request.form and "expiry" in request.form:
            name = request.form["name"]
            expiry_date = datetime.strptime(request.form["expiry"], "%Y-%m-%d")
            days_left = (expiry_date - datetime.now()).days

            grocery_items.append({
                "name": name,
                "expiry": expiry_date.strftime("%Y-%m-%d"),
                "days_left": days_left
            })

        # Receipt upload
        elif "receipt" in request.files:
            file = request.files["receipt"]
            if file and allowed_file(file.filename):
                path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(path)

                scanned_items = process_receipt(path)
                grocery_items.extend(scanned_items)
            else:
                return "Unsupported file type. Please upload a PNG, JPG, or JPEG.", 400

        return redirect("/")

    # Update days left
    for item in grocery_items:
        item["days_left"] = (datetime.strptime(item["expiry"], "%Y-%m-%d") - datetime.now()).days

    grocery_items.sort(key=lambda x: x["days_left"])

    return render_template("index.html", items=grocery_items)

if __name__ == "__main__":
    app.run(debug=True)
