import csv
from pathlib import Path
from collections import Counter, defaultdict

# Use the folder containing this Python script
BASE_DIR = Path(__file__).resolve().parent

input_file = BASE_DIR / "significant_annotation_table.csv"
annotated_file = BASE_DIR / "significant_annotation_table_annotated.csv"

# 1. Print the context of each occurrence
print("CONTEXTS")

with open(input_file, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for i, row in enumerate(reader, start=1):
        print(f"\n--- Case {i} | Genre: {row['Genre']} ---")
        print(row["Context"])

# 2. Count semantic categories by genre
counts = defaultdict(Counter)

with open(annotated_file, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        genre = row["Genre"].strip()
        category = row["Semantic_Category"].strip()
        counts[genre][category] += 1

print("\nFREQUENCY AND PERCENTAGE TABLE")

for genre in sorted(counts):
    total = sum(counts[genre].values())
    print(f"\n{genre} (n={total})")

    for category in sorted(counts[genre]):
        number = counts[genre][category]
        percentage = number / total * 100 if total else 0
        print(f"  {category}: {number} ({percentage:.1f}%)")

# 3. Save the frequency table
output_file = BASE_DIR / "significant_semantic_frequencies.csv"

with open(output_file, "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Genre", "Semantic_Category", "Frequency", "Percentage"])

    for genre in sorted(counts):
        total = sum(counts[genre].values())

        for category in sorted(counts[genre]):
            number = counts[genre][category]
            percentage = number / total * 100 if total else 0
            writer.writerow([genre, category, number, round(percentage, 1)])

print(f"\nFrequency table saved: {output_file}")

# 4. Create and save the semantic-category chart
import matplotlib.pyplot as plt

genres = sorted(counts)
categories = sorted({
    category
    for genre_counts in counts.values()
    for category in genre_counts
})

x_positions = list(range(len(genres)))
bar_width = 0.8 / max(len(categories), 1)

fig, ax = plt.subplots(figsize=(9, 5))

for i, category in enumerate(categories):
    values = [counts[genre][category] for genre in genres]
    positions = [
        x + (i - (len(categories) - 1) / 2) * bar_width
        for x in x_positions
    ]
    ax.bar(positions, values, bar_width, label=category)

ax.set_xticks(x_positions)
ax.set_xticklabels(genres)
ax.set_xlabel("Genre")
ax.set_ylabel("Number of Occurrences")
ax.set_title("Semantic Categories of 'Significant' Across Genres")
ax.legend(title="Semantic Category")
fig.tight_layout()

chart_file = BASE_DIR / "significant_semantic_categories.png"
fig.savefig(chart_file, dpi=300, bbox_inches="tight")
plt.show()

print(f"Chart saved: {chart_file}")
