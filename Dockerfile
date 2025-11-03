# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy local files to container
COPY . .

# Install dependencies directly
RUN pip install --no-cache-dir PyMuPDF pandas

# Run your script
CMD ["python", "invoice.py"]
