import os
import time
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# =========================
# CONFIG
# =========================
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DATA_PATH = "data/master_products.xlsx"

# Free-tier safe settings
NORMAL_SLEEP = 2          # seconds between successful calls
QUOTA_SLEEP = 35          # seconds to wait when quota is hit

# =========================
# SETUP
# =========================
genai.configure(api_key=GEMINI_API_KEY)

# IMPORTANT: free-tier model
model = genai.GenerativeModel("models/gemini-2.5-flash-lite")

df = pd.read_excel(DATA_PATH)

# Ensure required columns exist
for col in ["Description", "Features", "Dimensions", "Description_Status"]:
    if col not in df.columns:
        df[col] = ""

# =========================
# PROMPT BUILDER
# =========================
def build_prompt(row):
    return f"""
You are writing content for a professional product catalogue.

Product Name: {row['Product_Name']}
Category: {row['Category']}
Sub Category: {row['Sub_Category']}

Tasks:
1. Write a neutral professional description (40–60 words).
2. Provide 3–5 concise bullet-point features.
3. Give approximate industry-standard dimensions based on category.

Rules:
- Do NOT mention brand names.
- Do NOT assume materials unless generic.
- Dimensions must be approximate.
- Use a clean, catalogue-ready tone.

Output STRICTLY in this format:

DESCRIPTION:
<text>

FEATURES:
• point 1
• point 2
• point 3

DIMENSIONS:
<dimensions>
"""

# =========================
# MAIN LOOP
# =========================
print("🚀 Starting Gemini free-tier description generation...")

for idx, row in tqdm(df.iterrows(), total=len(df)):

    # Skip already completed rows
    if str(row["Description_Status"]).lower() == "success":
        continue

    try:
        prompt = build_prompt(row)
        response = model.generate_content(prompt)

        text = response.text.strip()

        # Parse output safely
        desc = text.split("FEATURES:")[0].replace("DESCRIPTION:", "").strip()
        features = text.split("FEATURES:")[1].split("DIMENSIONS:")[0].strip()
        dimensions = text.split("DIMENSIONS:")[1].strip()

        df.at[idx, "Description"] = desc
        df.at[idx, "Features"] = features
        df.at[idx, "Dimensions"] = dimensions
        df.at[idx, "Description_Status"] = "success"

        time.sleep(NORMAL_SLEEP)

    except ResourceExhausted:
        # 🔴 QUOTA HIT — WAIT & RETRY SAME ITEM
        print("⏳ Quota hit. Waiting before retry...")
        time.sleep(QUOTA_SLEEP)
        continue

    except Exception as e:
        print(f"❌ Failed for {row['Product_Name']}: {e}")
        df.at[idx, "Description_Status"] = "failed"
        time.sleep(NORMAL_SLEEP)

# =========================
# SAVE
# =========================
df.to_excel(DATA_PATH, index=False)

print("✅ STEP 4 COMPLETE (or paused safely)")
