import pandas as pd

DATA_PATH = "data/master_products.xlsx"

df = pd.read_excel(DATA_PATH)

def generate_description(name, category, sub_category):
    category = str(category).lower()
    sub_category = str(sub_category).lower()

    if category == "furniture":
        return f"{name} is designed for professional salon and spa environments, offering stable construction, ergonomic support, and suitability for regular commercial use."

    if category == "machine":
        return f"{name} is a professional-use device intended for salon and beauty applications, providing reliable performance and ease of operation."

    if category == "tool":
        return f"{name} is a practical salon tool designed for routine beauty and grooming tasks, suitable for daily professional use."

    if category == "accessory":
        return f"{name} is a salon accessory intended to support beauty procedures and improve workflow efficiency."

    if category == "consumable":
        return f"{name} is a consumable salon item designed for regular professional usage."

    return f"{name} is designed for general professional salon use."

def generate_features(category, sub_category):
    category = str(category).lower()
    sub_category = str(sub_category).lower()

    if category == "furniture":
        return "• Professional-grade design\n• Stable construction\n• Suitable for salon use\n• Easy to maintain"

    if category == "machine":
        return "• Professional performance\n• Easy operation\n• Suitable for salon use\n• Reliable build quality"

    if category == "tool":
        return "• Easy to use\n• Suitable for daily use\n• Lightweight and practical"

    if category == "accessory":
        return "• Supports salon procedures\n• Easy handling\n• Suitable for professional use"

    if category == "consumable":
        return "• Suitable for professional use\n• Standard commercial quality"

    return "• Suitable for professional use"

filled_desc = 0
filled_feat = 0

for idx, row in df.iterrows():

    if pd.isna(row.get("Description")) or str(row["Description"]).strip() == "":
        df.at[idx, "Description"] = generate_description(
            row["Product_Name"], row["Category"], row["Sub_Category"]
        )
        filled_desc += 1

    if pd.isna(row.get("Features")) or str(row["Features"]).strip() == "":
        df.at[idx, "Features"] = generate_features(
            row["Category"], row["Sub_Category"]
        )
        filled_feat += 1

df.to_excel(DATA_PATH, index=False)

print(f"✅ Descriptions filled: {filled_desc}")
print(f"✅ Features filled: {filled_feat}")
