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
# ReACT-99,
# ReACT-69,
# ReACT-70,
# ReACT-71,
# ReACT-72,
# ReACT-74,

import os
import time
import csv

from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY_2")
client = genai.Client(api_key=GEMINI_API_KEY)

#project_name = "kvrocks"
# project_name = "celeborn"
project_name = "ResDB"
base_path = "../github_api"

if GEMINI_API_KEY is None:
    print("Keys were not fetched!!\n")
else:
    print("Keys fetched!!\n")

def upload_file_in_chunks(file_path, chunk_size=1024*1024):
    with open(file_path, 'r', encoding='utf-8') as file:
        chunk = file.read(chunk_size)
        while chunk:
            yield chunk
            chunk = file.read(chunk_size)

def upload_file_in_n_chunks(file_path):
    """Splits a file into exactly 6 equal parts and adds leftover bytes to the last chunk."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()  # Read the entire file into memory

    chunk_size = len(content) // 8  # Base size for each chunk

    chunks = [content[i * chunk_size: (i + 1) * chunk_size] for i in range(7)]  # First 5 chunks
    chunks.append(content[7 * chunk_size:])  # Last chunk gets the remainder too

    return chunks  # Returns a list of 6 chunks

def stream_file_in_n_chunks(file_path, num_chunks=50):
    """Streams file contents in smaller chunks to avoid memory overload."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    chunk_size = len(content) // num_chunks  
    for i in range(num_chunks - 1):
        yield content[i * chunk_size: (i + 1) * chunk_size]
    yield content[(num_chunks - 1) * chunk_size:]  # Last chunk

def batch_chunks(chunks, batch_size=5):
    """Yields batches of chunks to reduce API calls."""
    batch = []
    for chunk in chunks:
        batch.append(chunk)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch  # Send remaining chunks

def save_analysis(react_name, outcome, recommendation, output_file):
    with open(output_file, mode="a", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["Project Name", "ReACT Name/Number", "Outcome", "Recommendation"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not os.path.isfile(output_file) or os.stat(output_file).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "Project Name": project_name,
            "ReACT Name/Number": react_name,
            "Outcome": outcome,
            "Recommendation": recommendation
        })
    
    print(f"Analysis for {react_name} saved to {output_file}")

def issue_comm_reacts():
    reacts = {
        "ReACT-17": "Encourage mentors to collaborate with mentees on addressing bugs or issues.",
        "ReACT-27": "As a newcomer, explain what you've tried when asking for help, and use the provided template. (Check for good-first-issue labels)",
        "ReACT-58": "Encourage senior developers to answer questions of newcomers",
        "ReACT-61": "Make the tasks technically interesting",
        "ReACT-67": "Clearly communicate unresolved issues to the developers",
        "ReACT-86": "Acknowledge all contributions of newcomers (comments)",
        "ReACT-95": "Set expectations and needs early: Show newcomers what is expected from them, where the difficulties lie, and what skills and level of expertise they need to have (what programming languages and technologies are used by the project, etc.). Place this information somewhere that newcomers access early in their journey (check issue comments under: Issue tag: “good first issue”)",
        "ReACT-103": "Keep the community informed about decisions."
    }

    my_file = list(upload_file_in_chunks(os.path.join(base_path, project_name, "issue_comments_cleaned.txt")))

    for chunk in my_file:
        issue_chunk_uploader = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Sharing the issue comments for the analysis in chunks, keep them in context for answering the following questions:",
                chunk
            ]
        )
        print("Chunk upload done!")
        time.sleep(65)  # Avoid rate limits
    for react in reacts:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Analyze all the issue comments chunks provided earlier of a GitHub project and tell me in one word either yes or no if the project follows this recommendation: " + reacts[react]
                + "\n Also, Provide a short, concise and to-the-point 3-4 lines max explanation on why do you think that the project does or does not follow this recommendation. "
                "Please give you answer in a paragraph style and not bullet points"
            ]
        )

        # Extract the first word (YES/NO) and the explanation
        response_text = response.text.strip()
        response_parts = response_text.split(" ", 1)  # Split at first space
        yes_no = response_parts[0] if response_parts else "UNKNOWN"
        explanation = response_parts[1] if len(response_parts) > 1 else "No explanation provided."

        # Remove commas from the explanation to keep CSV format intact
        explanation = explanation.replace(",", " ")

        react_combined = f"{react}: {reacts[react]}"  # Combine react ID and description

        # Append row to CSV
        save_analysis(react_combined, explanation, yes_no, "../final_react_analysis.csv")

        print(f"Saved: {project_name}, {react}, {yes_no}")


def PR_related_reacts():
    # Defining PR related ReACTS
    PR_reacts = {
        "ReACT-5": "Utilize a pull-based development approach (Check if multiple pull requests are being made by different contributors).",
        "ReACT-8": "Engage in code revision/Perform frequent code reviews.(Check for frequency of PRs)",
        "ReACT-10": "Offer job support to the newcomer.(Check for comments on PRs)",
        "ReACT-22": "Encourage newcomers to share their work for increased exposure. (Check for comments on PRs)"
    }

    # Providing all the PR related files to the Gemini API
    pr_comments_file = list(upload_file_in_chunks(os.path.join(base_path, project_name, "pr_comments.txt")))
    pr_file = list(upload_file_in_chunks(os.path.join(base_path, project_name, "pr.txt")))

    # # Reopening Output file
    for pr_chunk, pr_comments_chunk in zip(pr_file, pr_comments_file):
        pr_chunk_uploader = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Sharing the Pull Requests and Comments on it for the analysis in chunks, keep them in context for answering the following questions:",
                pr_comments_chunk,
                pr_chunk
            ]
        )
        print("PR chunk upload done!")
        time.sleep(65)  # Avoid rate limits
    for react in PR_reacts:
        # Storing a quick explanation from Gemini too
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Based on all the previously shared PR chunks, analyze whether the GitHub project follows this recommendation:"
                + PR_reacts[react] + "Give your answer in either Yes or No." + "\n Also, Provide a short, "
                "concise and to-the-point 3-4 lines max explanation on why do you think that the project does "
                "or does not follow this recommendation. Please give you answer in a paragraph style and not "
                "bullet points",
            ]
        )
        response_text = response.text.strip()
        response_parts = response_text.split(" ", 1)  # Split at first space
        yes_no = response_parts[0] if response_parts else "UNKNOWN"
        explanation = response_parts[1] if len(response_parts) > 1 else "No explanation provided."

        # Remove commas from the explanation to keep CSV format intact
        explanation = explanation.replace(",", " ")

        react_combined = f"{react}: {PR_reacts[react]}"  # Combine react ID and description

        # Append row to CSV
        save_analysis(react_combined, explanation, yes_no, "../final_react_analysis.csv")

        print(f"Saved: {project_name}, {react}, {yes_no}")

    print("Hurray! done! PR ReACT analysis saved!")

def issue_labels_related_reacts():
    # #pranav
    Issue_labels_reacts = {
        "ReACT-21": "Assign newcomers small and interesting tasks.(From Issue tags : find tags related to good first issue)",
        "ReACT-23": "Tag tasks based on their complexity level.(From Issue tags : find tags related to complexity level)",
        "ReACT-99": "Keep the issue list clean and triaged.(From Issue tags : check if significant tags are present)"
    }

    issue_comments_file = list(upload_file_in_chunks(os.path.join(base_path, project_name, "issue_comments_cleaned.txt")))

    # #pranav
        # for batch in batch_chunks(stream_file_in_n_chunks("../github_api/kvrocks/issue_comments.txt")):
        #     response = client.models.generate_content(
        #         model="gemini-2.0-flash",
        #         contents=["Processing multiple chunks in one request. Keep them in context:"] + batch
        #     )
        #     print("Batch upload done!")
        #     time.sleep(65)  # Avoid rate limits
        
    for chunk in issue_comments_file:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Sharing the issue labels for the analysis in chunks, keep them in context for answering the following questions:",
                chunk
            ]
        )
        print("Chunk upload done!")
        time.sleep(65)  # Avoid rate limits

    for react in Issue_labels_reacts:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Based on all the previously shared issue comments, analyze whether the GitHub project follows this recommendation: '"
                + Issue_labels_reacts[react] + "'.\n\n"
                "Respond with 'Yes' or 'No' based on your analysis.\n"
                "Then, provide a short and concise 3-4 line explanation justifying your answer.\n"
                "Ensure the response is in paragraph format, not bullet points."
            ]
        )
        # print(react, Issue_labels_reacts[react], response.text)
        # f.write(react + "," + Issue_labels_reacts[react] + "," + response.text + "," + "\n")
        response_text = response.text.strip()
        response_parts = response_text.split(" ", 1)  # Split at first space
        yes_no = response_parts[0] if response_parts else "UNKNOWN"
        explanation = response_parts[1] if len(response_parts) > 1 else "No explanation provided."

        # Remove commas from the explanation to keep CSV format intact
        explanation = explanation.replace(",", " ")

        react_combined = f"{react}: {Issue_labels_reacts[react]}"  # Combine react ID and description

        # Append row to CSV
        save_analysis(react_combined, explanation, yes_no, "../final_react_analysis.csv")
        print(f"Saved: {project_name}, {react}, {yes_no}")
        time.sleep(65)

    print("Labels ReACTs analysis completed and saved!")

#pranav
#Source code ReACTS
def analyze_source_code_reacts():
    source_code_reacts = {
        "ReACT-69": "Improve Inheritance in the source code (Remove implicit polymorphism, introduce generalization, Facilitate Subclassing, Use override over inheritance, Improve interface compliance)",
        "ReACT-70": "Improve encapsulation in the source code (Minimize public interface, remove unnecessary public variables)",
        "ReACT-71": "Improve exception handling in the source code",
        "ReACT-72": "Improve naming in the source code",
        "ReACT-74": "Improve Modularization (Modularize API, Improve organization of test directory, Remove unneeded packages)"
    }

    source_code_dir = os.path.join(base_path, project_name, "top_files")
    source_files = [os.path.join(source_code_dir, file) for file in os.listdir(source_code_dir)]

    for react in source_code_reacts:
        for file_path in source_files:
            file_chunks = list(upload_file_in_chunks(file_path))

            # for chunk in file_chunks:
            #     response = client.models.generate_content(
            #         model="gemini-2.0-flash",
            #         contents=[
            #             f"Analyze the following source code files and tell me in one word either yes or no if the project follows this recommendation: {source_code_reacts[react]}",
            #             chunk
            #         ]
            #     )
            src_files_upload = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    f"Sharing the source code files for the analysis, keep them in context for answering the following questions:",
                    file_chunks
                ]
            )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                f"Analyze the following source code files and tell me in one word either yes or no if the project follows this recommendation: {source_code_reacts[react]}",
                file_chunks 
            ]
        )

        time.sleep(65)  # Avoid rate limits

        explanation_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                f"Provide a short, concise, and to-the-point 3-4 lines max explanation on why do you think that the project does or does not follow this recommendation: {source_code_reacts[react]} Directly start the output with explanation. Please give your answer in a paragraph style and not bullet points.",
                file_chunks
            ]
        )

        response_text = response.text.strip()
        response_parts = response_text.split(" ", 1)  # Split at first space
        yes_no = response_parts[0] if response_parts else "UNKNOWN"

        # Remove commas from the explanation to keep CSV format intact
        explanation_text = explanation_response.text.strip().replace(",", " ")

        react_combined = f"{react}: {source_code_reacts[react]}"  # Combine react ID and description

        # Append row to CSV
        save_analysis(react_combined, explanation_text, yes_no, "../final_react_analysis.csv")
        
        print(f"Saved: {project_name}, {react}, {yes_no}")

        time.sleep(65)  # Avoid rate limits

    
    print("Source code ReACT analysis completed and saved!")

if __name__ == "__main__":
    issue_comm_reacts()
    PR_related_reacts()
    issue_labels_related_reacts()
    analyze_source_code_reacts()



