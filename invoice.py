import os
import fitz  # PyMuPDF
import pandas as pd
import re
"""“This code is currently tailored for Amazon India invoices.
 With slight adjustments to regex patterns, it can be extended for
   Flipkart invoices as well.”"""
# Directories
input_folder = "Input"
output_folder = "Output"
os.makedirs(output_folder, exist_ok=True)

# Helper for safe regex search
def find(pattern, text, field_name, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL):
    match = re.search(pattern, text, flags)
    if match:
        return match.group(1).strip()
    print(f"⚠️ Field '{field_name}' not found.")
    return ""

# Extract text
def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        return "\n".join(page.get_text() for page in doc)

# Main extraction logic
def extract_invoice_data(text, filename):
    # Flexible seller name detection
    seller_name = find(r"For\s+(.+?):\s*Authorized Signatory", text, "Seller Name")
    if not seller_name:
        seller_name = find(r"Sold\s*By\s*:\s*\n?(.+)", text, "Seller Name (alt)")

    # Tax rate & type from product line
    tax_rate = find(r"₹[\d,.]+\s+\d+\s+₹[\d,.]+\s+([\d]+%)\s+[A-Z]+", text, "Tax Rate")
    tax_type = find(r"₹[\d,.]+\s+\d+\s+₹[\d,.]+\s+[\d]+%\s+([A-Z]+)", text, "Tax Type")

    # Improved buyer name extraction - stops at newline or common address patterns
    buyer_name = find(r"Billing\s*Address\s*:\s*([^,\n]+?)(?:\n|,|\s+\d+|\s+[A-Z]{2,}\s+\d+)", text, "Buyer Name")
    if not buyer_name:
        # Alternative pattern for different invoice formats
        buyer_name = find(r"Bill\s*To\s*:\s*([^,\n]+?)(?:\n|,)", text, "Buyer Name (alt)")

    # Billing address (name + full block)
    billing_address = find(
        r"Billing\s*Address\s*:\s*(.*?)\n(?:State/UT Code|Shipping Address)",
        text, "Billing Address", flags=re.DOTALL
    ).replace('\n', ', ').strip()

    # Shipping address block
    shipping_address = find(
        r"Shipping\s*Address\s*:\s*(.*?)\n(?:State/UT Code|Place of supply)",
        text, "Shipping Address", flags=re.DOTALL
    ).replace('\n', ', ').strip()

    return {
        "File Name": filename,
        "Invoice Number": find(r"Invoice\s*Number\s*[:\-]?\s*\n?\s*([A-Z0-9\-]+)", text, "Invoice Number"),
        "Order Number": find(r"Order\s*Number\s*[:\-]?\s*\n?\s*([\d\-]+)", text, "Order Number"),
        "Order Date": find(r"Order\s*Date\s*[:\-]?\s*\n?\s*([\d./]+)", text, "Order Date"),
        "Invoice Date": find(r"Invoice\s*Date\s*[:\-]?\s*\n?\s*([\d./]+)", text, "Invoice Date"),
        "Seller Name": seller_name,
        "Seller GSTIN": find(r"GST\s*Registration\s*No\s*[:\-]?\s*([0-9A-Z]+)", text, "GSTIN"),
        "Buyer Name": buyer_name,
        "Billing Address": billing_address,
        "Shipping Address": shipping_address,
        "Place of Supply": find(r"Place\s*of\s*supply\s*[:\-]?\s*([A-Z ]+)", text, "Place of Supply"),
        "Product Name": find(r"\d\s+(.*?)\|", text, "Product Name"),
        "HSN": find(r"HSN[:\s]+(\d+)", text, "HSN"),
        "Unit Price": find(r"₹([\d,.]+)\s+\d+\s+₹[\d,.]+", text, "Unit Price"),
        "Quantity": "1",
        "Net Amount": find(r"1\s+.+?\s+₹[\d,.]+\s+\d+\s+₹([\d,.]+)", text, "Net Amount"),
        "Tax Rate": tax_rate,
        "Tax Type": tax_type,
        "Tax Amount": find(r"(?:IGST|CGST|SGST)\s+₹([\d,.]+)", text, "Tax Amount"),
        "Shipping Charges": find(r"Shipping Charges\s+₹([\d,.]+)", text, "Shipping Charges") or find(r"Shipping\s*Fee\s*[:\-]?\s*₹?([\d,.]+)", text, "Shipping Charges (alt)") or "0",
        "Shipping Tax Amount": (
    find(r"Shipping Charges.*?(?:IGST|CGST|SGST)\s+₹([\d,.]+)", text, "Shipping Tax (IGST block)")
    or find(r"Shipping.*?(?:Tax|GST).*?₹([\d,.]+)", text, "Shipping Tax (generic fallback)")
    or "0"
),

        "Total Amount": find(r"TOTAL:\s+₹[\d,.]+\s+₹([\d,.]+)", text, "Total Amount"),
        "Amount in Words": find(r"Amount in Words\s*[:\-]?\s*(.+?)\n", text, "Amount in Words"),
        "Payment Modes": ", ".join(re.findall(r"Mode\s*of\s*Payment\s*[:\-]?\s*(\w+)", text)) or "Not Mentioned"
    }

# Process all files
data_list = []
for filename in os.listdir(input_folder):
    if filename.endswith(".pdf") and filename != "5.pdf":
        path = os.path.join(input_folder, filename)
        try:
            text = extract_text_from_pdf(path)
            data = extract_invoice_data(text, filename)
            data_list.append(data)
        except Exception as e:
            print(f"❌ Error in {filename}: {e}")

# Export to Excel
df = pd.DataFrame(data_list)
output_path = os.path.join(output_folder, "extracted_invoice_data.xlsx")
df.to_excel(output_path, index=False)

print(f"\n✅ Done! Data saved to: {output_path}")