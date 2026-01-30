📦 AI-Assisted Product Catalogue Generator

This project automates the creation of a professional, print-ready product catalogue PDF from a simple Excel file.
It is designed for large product inventories (300+ items) where manual catalogue creation is time-consuming and error-prone.

The pipeline combines data structuring, image management, rule-based content generation, and HTML-to-PDF rendering to produce a consistent, client-ready catalogue.

✨ Key Features

📊 Excel-driven workflow – single source of truth

🖼️ Automatic + manual image support

Uses images from a local folder

Gracefully handles missing images with blank placeholders

📝 Automated product descriptions & features

Rule-based (stable, consistent, no hallucinations)

📐 Standardized industry dimensions

📄 High-quality PDF output

Exactly 2 products per page

Clean layout

Print-friendly (A4)

🔁 Re-runnable & editable

Replace images → regenerate PDF

Update Excel → regenerate PDF

🏗️ Project Structure
catalogue_project/
│
├── data/
│   └── master_products.xlsx        # Final structured product data
│
├── images/                          # Product images (manual or auto-added)
│   └── P001_product_name.jpg
│
├── templates/
│   └── catalogue.html               # wkhtmltopdf-safe HTML template
│
├── generate_pdf.py                  # Generates final PDF
├── fix_missing_descriptions.py      # Fills missing descriptions & features
├── fix_missing_dimensions.py        # Fills missing dimensions
│
└── catalogue.pdf                    # Final output

📥 Input Requirements
1️⃣ Excel File (master_products.xlsx)

Required columns:

Product_ID

Product_Name

Category

Sub_Category

Description

Features

Dimensions

Image_Path (optional)

The Excel file is auto-generated and enriched during earlier steps of the pipeline.

2️⃣ Images Folder (images/)

Image filenames must match the Image_Path or Product_ID

Example:

P051_all_in_one_eyelash_brushcomb.jpg


If an image is missing:

A blank image placeholder is shown

Layout remains intact

🛠️ Tech Stack

Python

Pandas – data handling

Jinja2 – HTML templating

wkhtmltopdf – HTML → PDF rendering

pdfkit – Python wrapper for wkhtmltopdf

wkhtmltopdf is used instead of WeasyPrint for maximum stability on Windows.

⚙️ Setup Instructions
1️⃣ Install wkhtmltopdf (Windows)

Download and install:
👉 https://wkhtmltopdf.org/downloads.html

Verify installation:

wkhtmltopdf --version

2️⃣ Install Python dependencies
pip install pandas jinja2 pdfkit openpyxl

3️⃣ (Optional) Fix missing data

If descriptions or dimensions are missing:

python fix_missing_descriptions.py
python fix_missing_dimensions.py

📄 Generate the Catalogue PDF
python generate_pdf.py


Output:

catalogue.pdf

🧠 How to Update the Catalogue
✔ Add or replace images

Drop new images into images/

Keep filenames unchanged

Re-run generate_pdf.py

✔ Update text or dimensions

Edit master_products.xlsx

Re-run generate_pdf.py

No manual PDF editing required.

✅ Design Decisions (Why this works)

Rule-based content instead of AI at scale

Avoids API limits and partial outputs

HTML tables instead of CSS grid

Required for reliable wkhtmltopdf rendering

Image placeholders

Prevent layout breakage

Repeatable pipeline

Same input → same output, every time

📌 Limitations

PDF layout is optimized for A4

Images must be provided manually for best quality

AI-based text generation is intentionally avoided in the final stage for stability

🚀 Use Cases

Salon & beauty equipment catalogues

Industrial product listings

Vendor or BOQ-based catalogues

Internal procurement documents

Client-facing product brochures

📜 License

This project is intended for internal, educational, or commercial catalogue generation.
Modify and extend as needed for your use case.