from PIL import Image, UnidentifiedImageError
import pytesseract
import re

# Path to your test image
image_path = "images/1185-receipt.jpg"

try:
    image = Image.open(image_path)
    image.verify()  # Check if it's a valid image
    image = Image.open(image_path).convert("L")  # Reopen + convert to grayscale

    text = pytesseract.image_to_string(image)
    print("🧾 OCR Output:\n" + "-"*40)
    print(text)
    print("-" * 40)

    # Keywords for this specific receipt
    keywords = ["coffee", "eggs", "pancakes", "sausage"]

    # Check and print found items
    found = []
    for keyword in keywords:
        if re.search(rf'\b{keyword}\b', text.lower()):
            found.append(keyword)

    print(f"✅ Detected items: {found}")

except UnidentifiedImageError:
    print(f"❌ Error: '{image_path}' is not a valid image file.")
except Exception as e:
    print(f"❌ Error processing image: {e}")
