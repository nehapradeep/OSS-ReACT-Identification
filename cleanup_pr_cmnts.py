import re

repos = [
    # {'owner': 'Kanaries', 'repo': 'pygwalker'},
    #{'owner': 'apache', 'repo': 'ResDB'},
    #{'owner': 'apache', 'repo': 'kvrocks'},
    # {'owner': 'apache', 'repo': 'doris'},
    # {'owner': 'apache', 'repo': 'incubator-liminal'},
    {'owner': 'apache', 'repo': 'celeborn'}
]

repo = repos[0]

input_file = f'./github_api/{repo['repo']}/pr_comments.txt'
output_file = f'./github_api/{repo['repo']}/pr_comments_cleaned.txt'

# Read the input file
with open(input_file, "r", encoding="utf-8") as file:
    data = file.read()

# Find all occurrences of 'body': '<comment>'
matches = re.findall(r"'body':\s*'(.*?)'", data)

# Save the extracted comments to the output file
with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n\n".join(matches))

print(f"Extracted {len(matches)} comments and saved to: {output_file}")
