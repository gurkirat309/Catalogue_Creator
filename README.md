# 📦 Product Catalogue PDF Generator

A production-ready pipeline to generate a **clean, professional, print-ready product catalogue PDF** from an Excel file.

This project is built for **large inventories (300+ products)** where manual catalogue creation becomes impractical.  
It supports **partial images, standardized descriptions, stable layouts**, and **Windows-safe PDF generation**.

---

## ✨ Features

- 📊 Excel-driven catalogue generation  
- 🖼️ Automatic + manual image handling  
- 📝 Rule-based product descriptions & features  
- 📐 Standardized industry dimensions  
- 📄 Stable PDF output (A4, print-ready)  
- 📑 **Exactly 2 products per page**  
- 🧱 Blank image placeholders when photos are missing  
- 🔁 Fully re-generatable (no manual PDF edits)





```text
catalogue_project/
├── data/
│   └── master_products.xlsx
│
├── images/
│   └── P001_product_name.jpg
│
├── templates/
│   └── catalogue.html
│
├── generate_pdf.py
├── fix_missing_descriptions.py
├── fix_missing_dimensions.py
│
└── catalogue.pdf
```

---




---

### 1️⃣ Excel File (`master_products.xlsx`)

Required columns:

| Column Name | Description |
|------------|-------------|
| Product_ID | Unique product identifier |
| Product_Name | Product name |
| Category | Product category |
| Sub_Category | Product sub-category |
| Description | Product description |
| Features | Bullet-point features |
| Dimensions | Approximate dimensions |
| Image_Path | Local image path (optional) |

---

### 2️⃣ Images Folder (`images/`)

- Image filenames must match `Product_ID`
- Example:
P051_all_in_one_eyelash_brushcomb.jpg

- If an image is missing:
- Layout stays intact
- Blank placeholder is shown

---

## 🛠️ Tech Stack

- Python
- Pandas
- Jinja2
- wkhtmltopdf
- pdfkit

> `wkhtmltopdf` is used for **maximum stability on Windows**.

---

## ⚙️ Setup Instructions

### 1️⃣ Install wkhtmltopdf (Windows)

Download from:
https://wkhtmltopdf.org/downloads.html


Verify installation:
```bash
wkhtmltopdf --version
2️⃣ Install Python Dependencies
pip install pandas jinja2 pdfkit openpyxl
🧹 Fix Missing Content (Optional)
If descriptions or dimensions are missing:

python fix_missing_descriptions.py
python fix_missing_dimensions.py
These scripts:

Do NOT use AI

Ensure 100% consistency

Are safe to run multiple times

📄 Generate the PDF Catalogue
python generate_pdf.py
Output:

catalogue.pdf
🔁 Updating the Catalogue
✔ Replace or add images
Drop images into images/

Keep filenames unchanged

Re-run generate_pdf.py

✔ Update text or data
Edit master_products.xlsx

Re-run generate_pdf.py

No manual PDF editing required.

🧠 Design Decisions
Rule-based content instead of AI at scale

HTML tables instead of CSS Grid (wkhtmltopdf compatibility)

Fixed layout to prevent overlapping

Repeatable, deterministic output

This ensures client-safe, print-safe PDFs every time.
```


🚀 Use Cases
Product catalogues

Vendor / BOQ documentation

Salon & beauty equipment listings

Industrial product brochures

Procurement documentation

