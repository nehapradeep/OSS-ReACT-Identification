import pandas as pd
import os

# Step 1: Open and read the project's CSV file
file_path = "liminal_commit_data2.csv"  # Update this path if needed
df = pd.read_csv(file_path)

# Step 2: Compute the percentage of each file extension
extension_counts = df["File Extension"].value_counts()
extension_percentage = (extension_counts / extension_counts.sum()) * 100

# Step 3: Define a variable for ReACT number (modifiable)
react_number = "ReACT-3"  # Change this value as needed

# Step 4: Prepare the output CSV file
output_file = "react_analysis_output.csv"
file_exists = os.path.isfile(output_file)

# Step 5: Store the results in a DataFrame
outcome_str = "; ".join([f"{ext}: {perc:.2f}%" for ext, perc in extension_percentage.items()])

output_data = pd.DataFrame({
    "OSS Project": ["Liminal Project"],
    "ReACT number": [react_number],
    "Outcome": [outcome_str]  # Store all percentages in a single cell
})

# Step 6: Save or append to the CSV file
output_data.to_csv(output_file, mode='a', index=False, header=not file_exists)

print(f"Analysis saved to {output_file}")
