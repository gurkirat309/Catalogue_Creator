import pandas as pd

INPUT_FILE = "BOQ PRODUCT LIST.xlsx"
OUTPUT_FILE = "data/master_products.xlsx"

# Load Excel WITHOUT headers
df = pd.read_excel(INPUT_FILE, header=None)

print("📌 Raw shape:", df.shape)

# Assume BOQ format:
# Column 0 → SR NO (or junk)
# Column 1 → Product Name
# Column 2 → Quantity

df = df.rename(columns={
    1: "product_name",
    2: "quantity"
})

# Drop rows where product name is missing
df = df.dropna(subset=["product_name"])

# Clean product names
df["product_name"] = df["product_name"].astype(str).str.strip().str.title()

# Quantity cleanup
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1).astype(int)

# Category logic
def assign_category(name):
    name = name.lower()
    if any(x in name for x in ["bed", "chair", "stool", "table"]):
        return "Furniture"
    if any(x in name for x in ["machine", "steamer", "remover", "heater", "unit"]):
        return "Machine"
    if any(x in name for x in ["brush", "roller"]):
        return "Accessory"
    if any(x in name for x in ["cream", "gel", "wax"]):
        return "Consumable"
    return "Tool"

def assign_subcategory(name):
    name = name.lower()
    if "bed" in name:
        return "Bed"
    if "chair" in name:
        return "Chair"
    if "brush" in name:
        return "Brush"
    if "remover" in name:
        return "Handheld Device"
    return ""

df["Category"] = df["product_name"].apply(assign_category)
df["Sub_Category"] = df["product_name"].apply(assign_subcategory)

# Product IDs
df.insert(0, "Product_ID", [f"P{str(i+1).zfill(3)}" for i in range(len(df))])

# Image queries
df["Image_Query"] = df["product_name"].apply(
    lambda x: f"{x.lower()} product white background"
)

df["Notes"] = ""

# Final output
df_final = df[
    ["Product_ID", "product_name", "Category", "Sub_Category", "quantity", "Image_Query", "Notes"]
]

df_final.columns = [
    "Product_ID",
    "Product_Name",
    "Category",
    "Sub_Category",
    "Quantity",
    "Image_Query",
    "Notes"
]

df_final.to_excel(OUTPUT_FILE, index=False)

print("✅ STEP 1 COMPLETE")
print("📄 Output file created → data/master_products.xlsx")
print(f"📦 Total products processed: {len(df_final)}")
