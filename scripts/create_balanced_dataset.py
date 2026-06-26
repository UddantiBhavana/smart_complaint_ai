import pandas as pd

input_file = "datasets/complaints/processed/complaints.csv"
output_file = "datasets/complaints/processed/complaints_balanced.csv"

samples_per_class = 50000

categories = [
    "Roads",
    "Water",
    "Electricity",
    "Drainage",
    "Sanitation"
]

balanced_parts = []

print("Reading dataset...")

for category in categories:

    print(f"Processing {category}...")

    sampled_chunks = []
    collected = 0

    for chunk in pd.read_csv(
        input_file,
        chunksize=50000,
        low_memory=False
    ):

        subset = chunk[chunk["category"] == category]

        if len(subset) > 0:

            sampled_chunks.append(subset)

            collected += len(subset)

            if collected >= samples_per_class:
                break

    category_df = pd.concat(sampled_chunks)

    category_df = category_df.sample(
        n=samples_per_class,
        random_state=42
    )

    balanced_parts.append(category_df)

balanced_df = pd.concat(balanced_parts)

balanced_df = balanced_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

balanced_df.to_csv(
    output_file,
    index=False
)

print("\nBalanced dataset created successfully!")
print("\nCategory Counts:")
print(balanced_df["category"].value_counts())
print("\nShape:")
print(balanced_df.shape)