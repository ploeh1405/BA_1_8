import sys
import json
import base64
from openpyxl import load_workbook

def main():
    if len(sys.argv) < 2:
        raise RuntimeError("Fehlendes Argument: payload_b64")

    payload_b64 = sys.argv[1]
    raw = base64.b64decode(payload_b64).decode("utf-8", errors="replace")
    data = json.loads(raw)

    output_file = data["output_file"]
    sheet_name = data["sheet"]
    row = data["row"]

    wb = load_workbook(output_file)
    ws = wb[sheet_name]
    
    fixed_row = []
    for cell in row:
        if isinstance(cell, list):
            fixed_row.append("; ".join(str(x) for x in cell))
        elif isinstance(cell, dict):
            fixed_row.append(json.dumps(cell, ensure_ascii=False))
        elif cell is None:
            fixed_row.append("")   # optional: None -> leer
        else:
            fixed_row.append(cell)

    ws.append(fixed_row)

    wb.save(output_file)

    print("OK: 1 row appended")

if __name__ == "__main__":
    main()
