import csv
from pathlib import Path

folder = Path(r"C:\Users\NAHID\Desktop\brown")

source = folder / "significant_annotation_table_annotated.csv"
output = folder / "significant_final_review.csv"

if not source.exists():
    print("Could not find:", source)
else:
    with source.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    if "Confidence" not in fieldnames:
        fieldnames.append("Confidence")

    if "Notes" not in fieldnames:
        fieldnames.append("Notes")

    statistical_cases = {6, 11, 12, 13, 14, 15, 16}

    for i, row in enumerate(rows, start=1):
        row["Confidence"] = (
            "High" if i in {11, 13}
            else "Review"
        )

        if i in statistical_cases:
            row["Notes"] = (
                "Provisional statistical interpretation; "
                "check the full context."
            )
        else:
            row["Notes"] = (
                "Provisional general-meaning interpretation; "
                "check the context."
            )

    with output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Review file saved:", output)
    print("Rows:", len(rows))
5
