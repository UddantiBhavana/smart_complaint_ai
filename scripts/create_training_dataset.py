import pandas as pd

input_file = "datasets/complaints/processed/nyc_filtered.csv"
output_file = "datasets/complaints/processed/complaints.csv"

mapping = {
    # Roads
    "Street Condition": "Roads",
    "Sidewalk Condition": "Roads",
    "Highway Condition": "Roads",

    # Water
    "Water System": "Water",
    "WATER LEAK": "Water",
    "Water Conservation": "Water",
    "Water Quality": "Water",
    "Drinking Water": "Water",

    # Electricity
    "Street Light Condition": "Electricity",
    "Traffic Signal Condition": "Electricity",
    "ELECTRIC": "Electricity",
    "Electrical": "Electricity",

    # Drainage
    "Sewer": "Drainage",
    "Root/Sewer/Sidewalk Condition": "Drainage",
    "Standing Water": "Drainage",
    "Indoor Sewage": "Drainage",

    # Sanitation
    "UNSANITARY CONDITION": "Sanitation",
    "Dirty Conditions": "Sanitation",
    "Missed Collection (All Materials)": "Sanitation",
    "Sanitation Condition": "Sanitation",
    "Recycling Enforcement": "Sanitation"
}

chunksize = 50000
first_chunk = True

for chunk in pd.read_csv(
    input_file,
    chunksize=chunksize,
    low_memory=False
):
    chunk = chunk[chunk["Complaint Type"].isin(mapping.keys())]

    chunk["category"] = chunk["Complaint Type"].map(mapping)

    chunk["complaint_text"] = (
        chunk["Descriptor"].fillna("")
    )

    final_df = chunk[["complaint_text", "category"]]

    final_df.to_csv(
        output_file,
        mode='w' if first_chunk else 'a',
        header=first_chunk,
        index=False
    )

    first_chunk = False

print("complaints.csv created successfully!")