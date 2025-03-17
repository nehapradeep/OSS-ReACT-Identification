import csv
import re
import sys
import os

def parse_txt_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = file.read()
    
    # Split PR entries using the separator line
    pr_entries = data.strip().split("================================================================================")
    
    # Define regex patterns
    pr_pattern = re.compile(r'PR #(\d+): (.*?) \(State: (.*?)\)')
    url_pattern = re.compile(r'URL: (.*?)')
    created_pattern = re.compile(r'Created at: (.*?), Merged at: (.*?)$')
    
    csv_data = []
    
    for entry in pr_entries:
        entry = entry.strip()
        pr_match = pr_pattern.search(entry)
        url_match = url_pattern.search(entry)
        created_match = created_pattern.search(entry)
        
        if pr_match and url_match and created_match:
            pr_number = pr_match.group(1)
            title = pr_match.group(2)
            state = pr_match.group(3)
            url = url_match.group(1)
            created_at = created_match.group(1)
            merged_at = created_match.group(2)
            
            csv_data.append([pr_number, title, state, url, created_at, merged_at])
    
    # Write to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["PR Number", "Title", "State", "URL", "Created At", "Merged At"])
        writer.writerows(csv_data)
    
    print(f'CSV file "{output_file}" created successfully!')

# Example usage
def main(project_name):
    # Define paths dynamically based on the project name
    txt_path = os.path.join("github_api", project_name, "pr.txt")
    csv_path = os.path.join("github_api", project_name, "pr.csv")
    
    parse_txt_to_csv(txt_path, csv_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python github_api/txt_csv.py <project_name>")
        sys.exit(1)
    
    project_name = sys.argv[1]
    main(project_name)
