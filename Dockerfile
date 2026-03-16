FROM n8nio/n8n

USER root

# 1) Systempakete installieren
# - python3 + pip
# - ca-certificates (TLS)
# - build tools + libs für manche Python Wheels (PyMuPDF ist meist als wheel da, aber safe)
RUN apk add --no-cache \
    python3 \
    py3-pip \
    ca-certificates \
    build-base \
    libffi-dev \
    openssl-dev \
  && update-ca-certificates

# 2) Virtuelle Umgebung anlegen und Python-Libraries installieren
RUN python3 -m venv /opt/venv \
  && /opt/venv/bin/python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
  && /opt/venv/bin/python -m pip install --no-cache-dir \
       pdfminer.six \
       openpyxl \
       pymupdf

# 3) venv in PATH, damit "python3" / "pip" aus der venv genutzt werden
ENV PATH="/opt/venv/bin:$PATH"

USER node
