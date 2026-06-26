import pandas as pd

input_file = "datasets/complaints/processed/nyc_filtered.csv"

complaint_types = {}

chunksize = 50000

print("Finding unique complaint types...")

for chunk in pd.read_csv(
    input_file,
    usecols=["Complaint Type"],
    chunksize=chunksize,
    low_memory=False
):
    counts = chunk["Complaint Type"].value_counts()

    for complaint, count in counts.items():
        complaint_types[complaint] = complaint_types.get(complaint, 0) + count

print("\nTop Complaint Types:\n")

sorted_types = sorted(
    complaint_types.items(),
    key=lambda x: x[1],
    reverse=True
)

for complaint, count in sorted_types[:100]:
    print(f"{complaint}: {count}")