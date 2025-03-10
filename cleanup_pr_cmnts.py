import re

input_file = "./github_api/kvrocks/pr_comments.txt"
output_file = "./github_api/kvrocks/pr_comments_cleaned.txt"

# Read the input file
with open(input_file, "r", encoding="utf-8") as file:
    data = file.read()

# Find all occurrences of 'body': '<comment>'
matches = re.findall(r"'body':\s*'(.*?)'", data)

# Save the extracted comments to the output file
with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n\n".join(matches))

print(f"Extracted {len(matches)} comments and saved to: {output_file}")
