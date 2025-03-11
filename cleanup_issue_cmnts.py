import re

repos = [
    # {'owner': 'Kanaries', 'repo': 'pygwalker'},
    {'owner': 'apache', 'repo': 'ResDB'},
    #{'owner': 'apache', 'repo': 'kvrocks'},
    # {'owner': 'apache', 'repo': 'doris'},
    # {'owner': 'apache', 'repo': 'incubator-liminal'},
    # {'owner': 'apache', 'repo': 'celeborn'}
]

repo = repos[0] 

input_file = f'./github_api/{repo['repo']}/issue_comments.txt'  # Update if needed
output_file = f'./github_api/{repo['repo']}/issue_comments_cleaned.txt'

# Read the input file
with open(input_file, "r", encoding="utf-8") as file:
    data = file.readlines()

extracted_lines = []
current_issue = None  # Store the current issue being processed

for line in data:
    # Match lines like "Issue #1234: Labels: bug, enhancement"
    issue_match = re.search(r"(Issue #\d+: Labels: .*)", line)
    
    if issue_match:
        current_issue = issue_match.group(1)  # Capture the issue line
        extracted_lines.append(current_issue)  # Store the issue line

    # Match 'body': '<comment>' on the same or next line
    body_match = re.search(r"'body':\s*'(.*?)'", line)
    
    if body_match and current_issue:
        extracted_lines.append(body_match.group(1))  # Store the corresponding comment

# Save extracted data
with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(extracted_lines))

print(f"Extracted {len(extracted_lines)} entries and saved to: {output_file}")
