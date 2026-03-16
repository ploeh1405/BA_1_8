from openpyxl import Workbook
from datetime import datetime
import json
import os

OUTPUT_DIR = "/data/output"

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"ergebnisse_{timestamp}.xlsx"
filepath = os.path.join(OUTPUT_DIR, filename)

wb = Workbook()

# erstes Sheet: Summary
ws_berichte = wb.active
ws_berichte.title = "Berichte"

# Header für Berichte
ws_berichte.append([
    "Dateiname",
    "Firma",
    "Art des Jobs",
    "Mitgebrachte Kenntnisse und Lehrveranstaltungen",
    "Fehlende Kenntnisse und Lehrveranstaltungen"
])

# zweites Sheet: Summary
ws_summary = wb.create_sheet(title="Summary")

# Platzhalter-Header (kannst du später erweitern)
ws_summary.append([
    "Metrik",
    "Wert"
])


wb.save(filepath)

print(json.dumps({
    "output_file": filepath
}))
