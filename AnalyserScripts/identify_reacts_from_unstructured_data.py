# Reacts: ReACT-17, 
# ReACT-27, 
# ReACT-58, 
# ReACT-61, 
# ReACT-67, 
# ReACT-86, 
# ReACT-95, 
# ReACT-103
# ReACT-5,
# ReACT-8,
# ReACT-10,
# ReACT-22
# ReACT-21,
# ReACT-23,
# ReACT-99

import os

from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

if GEMINI_API_KEY is None:
    print("Keys were not fetched!!\n")
else:
    print("Keys fetched!!\n")

reacts = {
    "ReACT-17": "Encourage mentors to collaborate with mentees on addressing bugs or issues.",
    "ReACT-27": "As a newcomer, explain what you've tried when asking for help, and use the provided template. (good-first-issue)",
    "ReACT-58": "Encourage senior developers to answer questions of newcomers",
    "ReACT-61": "Make the tasks technically interesting",
    "ReACT-67": "Clearly communicate unresolved issues to the developers",
    "ReACT-86": "Acknowledge all contributions of newcomers (comments)",
    "ReACT-95": "Set expectations and needs early: Show newcomers what is expected from them, where the difficulties lie, and what skills and level of expertise they need to have (what programming languages and technologies are used by the project, etc.). Place this information somewhere that newcomers access early in their journey (check issue comments under: Issue tag: “good first issue”)",
    "ReACT-103": "Keep the community informed about decisions."
}

def upload_file_in_chunks(file_path, chunk_size=1024*1024):
    with open(file_path, 'r', encoding='utf-8') as file:
        chunk = file.read(chunk_size)
        while chunk:
            yield chunk
            chunk = file.read(chunk_size)

my_file = list(upload_file_in_chunks('../github_api/kvrocks/issue_comments.txt'))

with open("react_analysis_2.csv", "w", encoding='utf-8') as f:
    for react in reacts:
        for chunk in my_file:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    "Analyze the issue comments of a GitHub project and tell me in one word either yes or no if the project follows this recommendation: " + reacts[react],
                    chunk
                ]
            )
        print(react, reacts[react], response.text)
        f.write(react + "," + reacts[react] + "," + response.text + "\n")

# Defining PR related ReACTS
PR_reacts = {
    "ReACT-5": "Utilize a pull-based development approach",
    "ReACT-8": "Engage in code revision/Perform frequent code reviews.",
    "ReACT-10": "Offer job support to the newcomer.",
    "ReACT-22": "Encourage newcomers to share their work for increased exposure."
}

# Providing all the PR related files to the Gemini API
pr_comments_file = list(upload_file_in_chunks("../github_api/kvrocks/pr_comments.txt"))
pr_file = list(upload_file_in_chunks("../github_api/kvrocks/pr.txt"))

# Reopening Output file
with open("react_analysis_2.csv", "w", encoding='utf-8') as f:
    for react in PR_reacts:
        for pr_chunk, pr_comments_chunk in zip(pr_file, pr_comments_file):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    "Analyze the pull request comments and related PR descriptions of a GitHub project and tell me in one word either yes or no if the project follows this recommendation: " + PR_reacts[react],
                    pr_comments_chunk,
                    pr_chunk
                ]
            )

            # Storing a quick explanation from Gemini too
            explanation = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    "Provide a short, concise and to-the-point 3-4 lines max explanation on why do you think that the project does or does not follow this recommendation: " + PR_reacts[react] + " Directly start the output with explanation. Please give you answer in a paragraph style and not bullet points",
                    pr_comments_chunk,
                    pr_chunk
                ]
            )
            print(react, PR_reacts[react], response.text, explanation.text)
            f.write(react + "," + PR_reacts[react] + "," + response.text + "," + explanation.text + "\n")

print("Hurray! done! PR ReACT analysis saved!")

#pranav
Issue_labels_reacts = {
    "ReACT-21": "Assign newcomers small and interesting tasks.(From Issue tags : find tags related to good first issue)",
    "ReACT-23": "Tag tasks based on their complexity level.(From Issue tags : find tags related to complexity level)",
    "ReACT-99": "Keep the issue list clean and triaged.(From Issue tags : check if significant tags are present)"
}

issue_comments_file = list(upload_file_in_chunks("../github_api/kvrocks/issue_comments.txt"))

#pranav
with open("react_analysis_2.csv", "a", encoding='utf-8') as f:
    for react in Issue_labels_reacts:
        for chunk in issue_comments_file:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    "Analyze the issue labels of a GitHub project and tell me in one word either yes or no if the project follows this recommendation: " + Issue_labels_reacts[react],
                    chunk
                ]
            )

            # Store a short explanation
            explanation = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    "Provide a short, concise, and to-the-point 3-4 lines max explanation on why do you think that the project does or does not follow this recommendation: " + Issue_labels_reacts[react] + " Directly start the output with explanation. Please give you answer in a paragraph style and not bullet points",
                    chunk
                ]
            )

            print(react, Issue_labels_reacts[react], response.text, explanation.text)
            f.write(react + "," + Issue_labels_reacts[react] + "," + response.text + "," + explanation.text + "\n")

print("Labels ReACT analysis completed and saved!")



