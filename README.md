# 🛒 **ShelfScan**

**ShelfScan** is a receipt scanning and item tracking web application. It allows users to upload grocery receipts, automatically extract items using OCR (Optical Character Recognition), and keep track of item expiry dates. Users can also manually add items to their list and get recipe suggestions based on the items they already have.

## 🌟 **Features**

- 🧾 **OCR-powered Receipt Scanning**: Automatically scans uploaded receipts to detect grocery items and their expiry dates.
- ➕ **Manual Item Addition**: Allows users to manually add items with their expiry dates.
- 🍳 **Recipe Suggestions**: Get recipe ideas based on the ingredients you have on hand, using the Spoonacular API.
- 🌙 **Dark Mode Toggle**: Switch between light and dark modes for a personalized experience.
- 🎨 **Animated UI**: Items fade in smoothly when they are added or scanned.
- 🔄 **Loading Indicator**: Displays a "scanning..." animation while OCR is processing the receipt.
- 🎨 **TailwindCSS**: Clean and responsive design for all devices.

## 🛠️ **Technologies Used**

- 🐍 **Flask**: Web framework used to build the server and handle routing.
- 📸 **Tesseract OCR**: Open-source tool to extract text from images (used for receipt scanning).
- 🌈 **TailwindCSS**: Utility-first CSS framework for styling.
- 🍲 **Spoonacular API**: API to fetch recipe suggestions based on available ingredients.
- 🖼️ **Pillow**: Python Imaging Library used to handle images.

## ⚙️ **Installation**

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/Towaiji/ShelfScan.git
cd ShelfScan
2️⃣ Install Dependencies
Make sure you have pip installed and then run:

bash
Copy
pip install -r requirements.txt
3️⃣ Set up .env file
Create a .env file in the root directory of your project and add your Spoonacular API Key:

env
Copy
SPOONACULAR_API_KEY=your-api-key-here
You can get an API key by signing up on Spoonacular.

4️⃣ Run the Application
Run the Flask application:

bash
Copy
python3 app.py
By default, the app will run at http://127.0.0.1:5000/. Open this URL in your browser.

🖥️ Usage
1️⃣ Scan Receipt
📸 Upload a receipt image (JPEG, PNG, or any supported format).

🧾 The app will scan the receipt and extract items (e.g., eggs, milk).

🗃️ The extracted items will be added to your grocery list, along with their expiry dates.

2️⃣ Add Items Manually
✍️ Manually add items by specifying their name and expiry date.

🕒 If no expiry date is provided, the app will use a default expiry based on the item.

3️⃣ Get Recipe Suggestions
🍽️ Once items are added to your list, you can get recipe suggestions based on the available ingredients.

🔍 The suggestions are fetched using the Spoonacular API.

4️⃣ Dark Mode Toggle
🌙 You can toggle between dark and light modes by clicking the "Toggle Dark Mode" button.

📂 Directory Structure
bash
Copy
ShelfScan/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Required Python packages
├── .env                   # Environment variables (Spoonacular API Key)
├── uploads/               # Folder to store uploaded receipt images
└── templates/
    └── index.html         # Frontend template using TailwindCSS
