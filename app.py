from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

# In-memory list for now
grocery_items = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        expiry_date = datetime.strptime(request.form["expiry"], "%Y-%m-%d")
        days_left = (expiry_date - datetime.now()).days

        grocery_items.append({
            "name": name,
            "expiry": expiry_date.strftime("%Y-%m-%d"),
            "days_left": days_left
        })

        return redirect("/")

    # Update days_left dynamically
    for item in grocery_items:
        item["days_left"] = (datetime.strptime(item["expiry"], "%Y-%m-%d") - datetime.now()).days

    return render_template("index.html", items=grocery_items)


if __name__ == "__main__":
    app.run(debug=True)
