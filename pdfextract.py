#!/usr/bin/env python3


import json
# os: um zu prüfen ob die Datei existiert
import os
# sys: um Argumente (PDF Pfad) aus sys.argv zu lesen
import sys
from pdfminer.high_level import extract_text


# CHUNKING CONFIG

CHUNK_SIZE = 20000
OVERLAP_PERCENTAGE = 0.05
OVERLAP = int(CHUNK_SIZE * OVERLAP_PERCENTAGE)
MIN_LAST_CHUNK = 200


# WORD CUTOFF

def find_cut_index_at_word_boundary(text, cut_index):
    
    # index later than end of text
    if cut_index >= len(text):
        return len(text)

    # if index on space - return index
    if text[cut_index].isspace():
        return cut_index

    # go back to last space
    i = cut_index
    while i > 0 and not text[i].isspace():
        i -= 1

    # return index if no spaces
    if i == 0:
        return cut_index

    return i


# CHUNKING

def chunk_text(text, chunk_size, overlap):
    chunks = []

    # check if text exists
    if not text:
        return chunks

    # check chunking config
    if chunk_size < 200:
        raise ValueError("CHUNK_SIZE ist kleiner als 200.")

    if overlap < 0:
        raise ValueError("OVERLAP ist kleiner als 0.")

    if overlap >= chunk_size:
        raise ValueError("OVERLAP ist groesser als CHUNK_SIZE.")

    
    start = 0
    n = len(text)

    while start < n:
        rough_end = start + chunk_size

        if rough_end > n:
            rough_end = n

        end = find_cut_index_at_word_boundary(text, rough_end)

        if end <= start + 50 and rough_end < n:
            end = rough_end

        chunk = text[start:end]
        chunk = chunk.strip()

        if chunk:
            chunks.append(chunk)

        if end >= n:
            break

        start = max(0, end - overlap)

    # if last chunk to short, add to prev
    if len(chunks) >= 2 and len(chunks[-1]) < MIN_LAST_CHUNK:
        chunks[-2] = (chunks[-2] + "\n\n" + chunks[-1]).strip()
        chunks.pop()

    return chunks


# MAIN

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 textExtract2.py <pdf_path>", file=sys.stderr)
        sys.exit(2)

    pdf_path = sys.argv[1]

    # path leads to pdf
    if not pdf_path.lower().endswith(".pdf"):
        print(f"Error: input is not a PDF: {pdf_path}", file=sys.stderr)
        sys.exit(3)

    if not os.path.isfile(pdf_path):
        print(f"Error: file not found: {pdf_path}", file=sys.stderr)
        sys.exit(4)

    try:
        raw_text = extract_text(pdf_path)

        if raw_text is None:
            raw_text = ""

        chunks = chunk_text(raw_text, CHUNK_SIZE, OVERLAP)

        output = {
            "pdf_path": pdf_path,
            "chunk_size": CHUNK_SIZE,
            "overlap": OVERLAP,
            "num_chars": len(raw_text),
            "num_chunks": len(chunks),
            "chunks": [{"chunk_index": i, "text": c} for i, c in enumerate(chunks)],
        }

        print(json.dumps(output, ensure_ascii=False))

    except Exception as e:
        print(f"Extraction/chunking failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
