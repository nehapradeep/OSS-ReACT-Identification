import csv
import os
import pandas as pd

def analyze_react_metrics(csv_filename):
    project_metrics = {
        "ReACT-11 Keep the project small and simple.": True,  # Assume small and simple unless large LOC is detected
        "ReACT-26 Conduct unit tests.": False,  # Will be True if test files are found
        "ReACT-32 Promote code transparency. Keep the code as simple as possible": False,  # Will be evaluated based on comments
        "ReACT-82 Have and enforce a code of conduct": False   # Will be True if CODE_OF_CONDUCT.md exists
    }
    
    total_files = 0
    total_loc = 0
    total_comment_lines = 0
    test_files = 0
    
    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            total_files += 1
            total_loc += int(row["Total Lines Changed"])
            
            file_name = row["File Name"].lower()
            file_extension = row["File Extension"].lower()
            
            # Check for test files
            if "test" in file_name or file_name.startswith("test_"):
                test_files += 1
                
            # Check for code of conduct
            if file_name == "code_of_conduct.md":
                project_metrics["ReACT-82 Have and enforce a code of conduct (have file named CODE_OF_CONDUCT.md"] = True
                
            # Approximate comment ratio (assuming comments are 20% of deleted lines)
            total_comment_lines += int(row["Deleted Lines"]) * 0.2
    
    # Evaluate ReACT-11: Project simplicity (if LOC > 10,000, recommend keeping it simple) - Can be Vague
    if total_loc > 1000000:
        project_metrics["ReACT-11 Keep the project small and simple."] = False
    
    # Evaluate ReACT-26: If no test files exist, recommend unit tests
    if test_files > 0:
        project_metrics["ReACT-26 Conduct unit tests."] = True
    
    # Evaluate ReACT-32: If comments are less than 15% of total LOC, recommend more transparency
    if total_comment_lines / total_loc > 0.15:
        project_metrics["ReACT-32 Promote code transparency. Keep the code as simple as possible"] = True
    
    recommendations = [key for key, value in project_metrics.items() if not value]
    
    if recommendations:
        print("Recommendations:")
        for react in recommendations:
            print(f"- {react}")
    else:
        print("All ReACT guidelines are met! No recommendations needed.")


def analyze_file_extensions(file_path, react_number, project_name="Liminal Project", output_file="react_analysis_output.csv"):
    # Step 1: Read the project's CSV file
    df = pd.read_csv(file_path)
    
    # Step 2: Compute the percentage of each file extension
    extension_counts = df["File Extension"].value_counts()
    extension_percentage = (extension_counts / extension_counts.sum()) * 100
    
    # Step 3: Prepare the output CSV file
    file_exists = os.path.isfile(output_file)
    
    # Step 4: Store the results in a DataFrame
    outcome_str = "; ".join([f"{ext}: {perc:.2f}%" for ext, perc in extension_percentage.items()])
    
    output_data = pd.DataFrame({
        "OSS Project": [project_name],
        "ReACT number": [react_number],
        "Outcome": [outcome_str]  # Store all percentages in a single cell
    })
    
    # Step 5: Save or append to the CSV file
    output_data.to_csv(output_file, mode='a', index=False, header=not file_exists)
    
    print(f"Analysis saved to {output_file}")

def analyze_contributing_md(directory_path):
    project_metrics = {
        "ReACT-9 Grant newcomer access to the main repository": False,
        "ReACT-19 Flag newcomers to ensure a welcoming environment for them": False,
        "ReACT-33 Provide clear and detailed contribution guidelines": False,
        "ReACT-84 Provide onboarding support and help newcomers to make their first contribution": False
    }
    
    contributing_md_path = os.path.join(directory_path)
    if os.path.exists(contributing_md_path):
        with open(contributing_md_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
            
            if "how to request for access" in content:
                project_metrics["ReACT-9 Grant newcomer access to the main repository"] = True
            if "flag newcomers" in content:
                project_metrics["ReACT-19 Flag newcomers to ensure a welcoming environment for them"] = True
            if "contribution guidelines" in content:
                project_metrics["ReACT-33 Provide clear and detailed contribution guidelines"] = True
            if "onboarding support" in content or "first contribution" in content:
                project_metrics["ReACT-84 Provide onboarding support and help newcomers to make their first contribution"] = True
    
    recommendations = [key for key, value in project_metrics.items() if not value]
    
    if recommendations:
        print("Recommendations for CONTRIBUTING.md:")
        for react in recommendations:
            print(f"- {react}")
    else:
        print("All ReACT guidelines for CONTRIBUTING.md are met!")

# Example usage
file_path = "liminal_commit_data.csv"
react_number = "ReACT-3"
#analyze_file_extensions(file_path, react_number)

csv_filename = "liminal_commit_data.csv"
#analyze_react_metrics(csv_filename)
analyze_contributing_md(csv_filename)