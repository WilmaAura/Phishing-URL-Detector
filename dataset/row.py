import csv
from pathlib import Path

csv_path = Path(__file__).with_name("top-1m.csv")
with csv_path.open(newline="", encoding="utf-8") as csv_file:
    row_count = sum(1 for _ in csv.reader(csv_file))

print(row_count)