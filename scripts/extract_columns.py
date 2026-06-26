import pandas as pd

input_file = "datasets/complaints/raw/NYC_311_Service_Requests.csv"
output_file = "datasets/complaints/processed/nyc_filtered.csv"

required_columns = [
    "Complaint Type",
    "Descriptor",
    "Agency",
    "Resolution Description",
    "Status",
    "Created Date",
    "Closed Date"
]

chunksize = 50000

first_chunk = True

print("Processing dataset in chunks...")

for chunk in pd.read_csv(
    input_file,
    usecols=required_columns,
    chunksize=chunksize,
    low_memory=False
):
    chunk.to_csv(
        output_file,
        mode='w' if first_chunk else 'a',
        header=first_chunk,
        index=False
    )

    first_chunk = False

    print(f"Processed {len(chunk)} rows")

print("Finished!")
print(f"Saved to: {output_file}")