import os
import re
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

# =========================
# CONFIG
# =========================
load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

DATA_PATH = "data/master_products.xlsx"
IMAGE_DIR = "images"

REQUEST_TIMEOUT = 30
SLEEP_BETWEEN_REQUESTS = 1  # seconds (avoid rate limits)

# =========================
# SETUP
# =========================
os.makedirs(IMAGE_DIR, exist_ok=True)

df = pd.read_excel(DATA_PATH)

# Ensure Image_Path column exists
if "Image_Path" not in df.columns:
    df["Image_Path"] = ""

# =========================
# HELPERS
# =========================
def safe_filename(text: str) -> str:
    """
    Make filenames OS-safe (Windows/Linux/Mac).
    """
    text = text.lower()
    text = re.sub(r'[\/:*?"<>|]', '', text)   # remove illegal chars
    text = re.sub(r'\s+', '_', text)          # spaces -> underscore
    return text.strip("_")

def fetch_image_url(query: str) -> str | None:
    """
    Fetch best image URL from SerpAPI.
    """
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_images",
        "q": query,
        "api_key": SERP_API_KEY,
        "num": 5
    }

    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    data = response.json()
    images = data.get("images_results", [])

    for img in images:
        if "original" in img:
            return img["original"]

    return None

# =========================
# MAIN LOOP
# =========================
print("🚀 Starting image fetch...")

for idx, row in tqdm(df.iterrows(), total=len(df)):

    # Skip already completed rows
    if pd.notna(row["Image_Path"]) and str(row["Image_Path"]).strip() != "":
        continue

    product_id = row["Product_ID"]
    product_name = row["Product_Name"]
    query = row["Image_Query"]

    safe_name = safe_filename(product_name)
    image_filename = f"{product_id}_{safe_name}.jpg"
    image_path = os.path.join(IMAGE_DIR, image_filename)

    try:
        img_url = fetch_image_url(query)
        if not img_url:
            print(f"⚠️ No image found for: {product_name}")
            continue

        img_response = requests.get(img_url, timeout=REQUEST_TIMEOUT)
        img_response.raise_for_status()

        with open(image_path, "wb") as f:
            f.write(img_response.content)

        df.at[idx, "Image_Path"] = image_path

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    except Exception as e:
        print(f"❌ Failed for {product_name}: {e}")

# =========================
# SAVE RESULTS
# =========================
df.to_excel(DATA_PATH, index=False)

print("✅ Image fetching complete.")
print("📄 master_products.xlsx updated with Image_Path")
