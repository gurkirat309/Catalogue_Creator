import pandas as pd

DATA_PATH = "data/master_products.xlsx"

df = pd.read_excel(DATA_PATH)

def default_dimensions(category, sub_category):
    category = str(category).lower()
    sub_category = str(sub_category).lower()

    # Furniture
    if category == "furniture":
        if "chair" in sub_category:
            return "Approx. 110–130 cm (H) × 55–65 cm (W) × 85–95 cm (D)"
        if "bed" in sub_category:
            return "Approx. 180–190 cm (L) × 60–70 cm (W) × 65–75 cm (H)"
        if "stool" in sub_category:
            return "Approx. 45–60 cm (H) × 35–40 cm (Dia)"
        return "Approx. standard furniture dimensions"

    # Machines
    if category == "machine":
        return "Approx. 30–45 cm (H) × 25–40 cm (W) × 25–40 cm (D)"

    # Tools
    if category == "tool":
        return "Approx. 15–25 cm (L)"

    # Accessories
    if category == "accessory":
        return "Approx. 10–20 cm (L)"

    # Consumables
    if category == "consumable":
        return "Standard commercial packaging size"

    return "Approx. standard industry dimensions"

# Fill missing dimensions only
filled_count = 0

for idx, row in df.iterrows():
    if pd.isna(row["Dimensions"]) or str(row["Dimensions"]).strip() == "":
        df.at[idx, "Dimensions"] = default_dimensions(
            row["Category"], row["Sub_Category"]
        )
        filled_count += 1

df.to_excel(DATA_PATH, index=False)

print(f"✅ Filled missing dimensions for {filled_count} products")
