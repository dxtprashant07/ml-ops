FROM python:3.9-slim

WORKDIR /app

COPY . .

# Install dependencies including openpyxl
RUN pip install --no-cache-dir PyMuPDF pandas openpyxl

CMD ["python", "invoice.py"]
