import pandas as pd
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict
import pdfkit
import os

DATA_PATH = "data/master_products.xlsx"
TEMPLATE_DIR = "templates"
OUTPUT_PDF = "catalogue3.pdf"

config = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
)

df = pd.read_excel(DATA_PATH)
df = df.fillna("")

products = defaultdict(list)
for _, row in df.iterrows():
    products[row["Category"]].append(row.to_dict())

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template("catalogue.html")

html_content = template.render(products=products)

temp_html = "temp_catalogue.html"
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_content)

options = {
    "page-size": "A4",
    "margin-top": "10mm",
    "margin-bottom": "10mm",
    "margin-left": "10mm",
    "margin-right": "10mm",
    "encoding": "UTF-8",
    "enable-local-file-access": ""
}

pdfkit.from_file(
    temp_html,
    OUTPUT_PDF,
    configuration=config,
    options=options
)

os.remove(temp_html)

print("Catalogue generated fil;e names as catalogue.pdf")
