
import csv
from pathlib import Path

DATA_DIR = Path("data")

files = [
    "tulu_titles.csv",
    "kannada_titles.csv",
    "english_titles.csv"
]

for filename in files:
    file_path = DATA_DIR / filename

    print(f"\nChecking: {filename}")

    if not file_path.exists():
        print("ERROR: File not found!")
        continue

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        print("Columns:", reader.fieldnames)

        for i, row in enumerate(reader):
            if i == 2:
                break
            print(f"Sample {i + 1}:", row.get("title_nfc"))

    print("File exists and can be read.")
