import csv
import os

def save_analysis(react_name, outcome, recommendation, output_file):
    with open(output_file, mode="a", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["Project Name", "ReACT Name/Number", "Outcome", "Recommendation"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not os.path.isfile(output_file) or os.stat(output_file).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "Project Name": 'kvrocks',
            "ReACT Name/Number": react_name,
            "Outcome": outcome,
            "Recommendation": recommendation
        })
    
    print(f"Analysis for {react_name} saved to {output_file}")

# purva
def analyze_react_102(input_csv_file, output_file):
    with open(input_csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        faq_feature_found = False
        for row in reader:
            content = row.get("Content", "").lower()
            if "faq" in content:
                faq_feature_found = True
                break
        if faq_feature_found:
            outcome = "FAQ section feature found and integrated into the project."
            recommendation = "Enhance the live FAQ section with real-time updates and user interactions."
        else:
            outcome = "No live FAQ section feature found in the project."
            recommendation = "Add a live FAQ section with interactive capabilities to improve user engagement."
        
        save_analysis("ReACT-102", outcome, recommendation, output_file)

# purva
def analyze_react_100(input_csv_file, output_file):
    with open(input_csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        documentation_found = False
        for row in reader:
            content = row.get("Content", "").lower()
            if any(keyword in content for keyword in ["document", "process", "practice"]):
                documentation_found = True
                break
        if documentation_found:
            outcome = "Processes and practices are documented within the project."
            recommendation = "Ensure that the documentation is comprehensive and up-to-date, including any new practices or processes."
        else:
            outcome = "No documentation of processes and practices found in the project."
            recommendation = "Document the key processes and practices to enhance team collaboration and project transparency."
        
        save_analysis("ReACT-100", outcome, recommendation, output_file)

# purva
def analyze_react_93(input_csv_file, output_file):
    with open(input_csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        zulip_found = False
        mailing_list_found = False
        for row in reader:
            header = row.get("Header", "").strip().lower()
            content = row.get("Content", "").strip().lower()
            if "zulip" in header or "zulip" in content:
                zulip_found = True
            if "mailing list" in header or "mailing list" in content:
                mailing_list_found = True        
        if zulip_found and mailing_list_found:
            outcome = "Zulip chat and Mailing List are both available as communication channels."
            recommendation = "Leverage Zulip for real-time discussions and use the Mailing List for formal updates and long-form communication."
        elif zulip_found:
            outcome = "Zulip chat is available as a local communication channel."
            recommendation = "Promote the use of Zulip for community discussions and ensure visibility to newcomers."
        elif mailing_list_found:
            outcome = "A Mailing List is available for communication."
            recommendation = "Introduce real-time communication platforms, like Zulip, to complement the mailing list for faster and more interactive engagement."
        else:
            outcome = "No clear local communication channels (like Zulip or chat platforms) found."
            recommendation = "Create and promote real-time communication channels, such as Zulip or chat rooms, for better community engagement."
        
        save_analysis("ReACT-93", outcome, recommendation, output_file)

# purva
def analyze_react_95(input_csv_file, output_file):
    with open(input_csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        expectations_found = False
        contributing_found = False
        for row in reader:
            header = row.get("Header", "").strip().lower()
            content = row.get("Content", "").strip().lower()
            if "contributing" in header:
                contributing_found = True                
            if any(keyword in content for keyword in ["expectations", "technologies", "skills", "programming languages", "requirements", "difficulty"]):
                expectations_found = True
                break        
        if contributing_found and expectations_found:
            outcome = "Expectations and required skills/technologies are documented, and the project has a clear contributing guide."
            recommendation = "Ensure that the contributing guide clearly outlines the required skills, technologies, and level of expertise for newcomers."
        elif contributing_found:
            outcome = "Contributing section is present, but detailed expectations and skill requirements are unclear."
            recommendation = "Enhance the contributing section by providing explicit details about the skills, technologies, and expertise required for contributing to the project."
        else:
            outcome = "No clear information on expectations, required skills, or technologies for newcomers found in the project."
            recommendation = "Provide clear information on the skills, technologies, and level of expertise required for the project, and ensure it is easily accessible early in the documentation for newcomers."
        
        save_analysis("ReACT-95", outcome, recommendation, output_file)

# purva
def analyze_react_97(input_csv_file, output_file):
    with open(input_csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        tutorials_found = False
        for row in reader:
            content = row.get("Content", "").lower()
            if any(keyword in content for keyword in ["tutorial", "guide", "document", "video", "website"]):
                tutorials_found = True
                break        
        if tutorials_found:
            outcome = "Tutorials and documentation are present in the project."
            recommendation = "Ensure that the tutorials are linked properly and easily accessible for users to learn about the project."
        else:
            outcome = "No tutorials or instructional documents found in the project."
            recommendation = "Create and link different kinds of tutorials and documents, including video tutorials and guides to help newcomers understand the system."
        
        save_analysis("ReACT-97", outcome, recommendation, output_file)

# purva
def analyze_react_98(input_csv_file, output_file):
    with open(input_csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        setup_found = False        
        for row in reader:
            content = row.get("Content", "").lower()
            if any(keyword in content for keyword in ["build", "setup", "install"]):
                setup_found = True
                break        
        if setup_found:
            outcome = "The system setup process for newcomers is documented."
            recommendation = "Ensure that the setup instructions are simple, clear, and include all necessary dependencies to minimize friction."
        else:
            outcome = "No clear instructions for newcomers to build the system locally found."
            recommendation = "Provide easy-to-follow instructions for setting up the system locally, ensuring that all dependencies and tools are clearly defined."
        
        save_analysis("ReACT-98", outcome, recommendation, output_file)

# purva
def analyze_react_77(input_csv_file, output_file):
    with open(input_csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        mailing_list_found = False
        mailing_list_encouraged = False        
        for row in reader:
            header = row.get("Header", "").strip().lower()
            content = row.get("Content", "").strip().lower()
            if "mailing list" in header or "mailing list" in content:
                mailing_list_found = True            
            if "subscribe" in header or "subscribe" in content or "join the mailing list" in content:
                mailing_list_encouraged = True        
        if mailing_list_found and mailing_list_encouraged:
            outcome = "Mailing list is mentioned and encouraged."
            recommendation = "The README provides clear encouragement for contributors to use the mailing list for communication and involvement."
        elif mailing_list_found:
            outcome = "Mailing list is mentioned, but not encouraged."
            recommendation = "Add a call-to-action encouraging contributors to use the mailing list for discussions, feedback, and project-related questions."
        else:
            outcome = "Mailing list is not mentioned."
            recommendation = "Include a section that encourages contributors to join and use the mailing list for communication and development discussions."
        
        save_analysis("ReACT-77", outcome, recommendation, output_file)

# purva
def analyze_react_60(input_csv_file, output_file):
    with open(input_csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        stars_found = False
        social_media_links_found = False        
        for row in reader:
            content = row.get("Content", "").strip().lower()  
            if "github stars" in content:
                stars_found = True            
            if "twitter" in content or "medium" in content or "linkedin" in content:
                social_media_links_found = True        
        if stars_found and social_media_links_found:
            outcome = "GitHub stars and social media links are present."
            recommendation = "The README promotes visibility with both GitHub stars and social media links."
        elif stars_found:
            outcome = "GitHub stars are present, but social media links are missing."
            recommendation = "Include social media profile links (Twitter, LinkedIn, Medium) to increase the project's visibility."
        else:
            outcome = "GitHub stars are not present."
            recommendation = "Add the GitHub stars badge and include social media profile links (Twitter, LinkedIn, Medium) to promote the project."
        
        save_analysis("ReACT-60", outcome, recommendation, output_file)

# purva
def analyze_react_53(input_csv_file, output_file):
    with open(input_csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)        
        incubated_found = False        
        for row in reader:
            content = row.get("Content", "").strip().lower()            
            if "apache software foundation" in content or "apache kvrocks" in content:
                incubated_found = True        
        if incubated_found:
            outcome = "The project is incubated by the Apache Software Foundation."
            recommendation = "No action required. The project is already incubated by a large software foundation."
        else:
            outcome = "The project is not incubated by a large software foundation."
            recommendation = "Consider submitting the project to a large software foundation like Apache or Linux Foundation for incubation."
        
        save_analysis("ReACT-53", outcome, recommendation, output_file)

# purva
def analyze_react_20(input_csv_file, output_file):
    with open(input_csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)        
        communication_channels = []        
        for row in reader:
            content = row.get("Content", "").strip().lower()
            if "zulipchat" in content:
                communication_channels.append("Zulip")
            if "mailing list" in content or "dev@kvrocks.apache.org" in content:
                communication_channels.append("Mailing List")
            if "medium" in content:
                communication_channels.append("Medium")
            if "twitter" in content or "x" in content:
                communication_channels.append("Twitter")
            if "wechat" in content:
                communication_channels.append("WeChat")        
        communication_channels = list(set(communication_channels))        
        if len(communication_channels) >= 2:
            outcome = f"The project communicates through various channels: {', '.join(communication_channels)}."
            recommendation = "No action required. The project already communicates through various channels."
        else:
            outcome = "The project does not communicate through various channels."
            recommendation = "Consider utilizing additional communication channels to enhance engagement and reach a wider audience."
        
        save_analysis("ReACT-20", outcome, recommendation, output_file)

input_csv_file = 'github_api/kvrocks/README.csv'
output_file = 'final_react_analysis.csv'
analyze_react_93(input_csv_file, output_file)
analyze_react_95(input_csv_file, output_file)
analyze_react_97(input_csv_file, output_file)
analyze_react_98(input_csv_file, output_file)
analyze_react_102(input_csv_file, output_file)
analyze_react_100(input_csv_file, output_file)
analyze_react_77(input_csv_file, output_file)
analyze_react_60(input_csv_file, output_file)
analyze_react_20(input_csv_file, output_file)