import csv
import pandas as pd
import os
from datetime import datetime, timedelta
from textblob import TextBlob

#project_name = 'kvrocks'
project_name = 'pygwalker'

# purva
def analyze_in_person_interactions(discussions, output_file="final_react_analysis.csv"):
    meetup_keywords = ['meetup', 'event', 'in-person', 'gathering', 'conference', 'announced']
    timestamps = []
    announcements = []
    total_discussions = 0

    for discussion in discussions:
        total_discussions += 1
        category_name = discussion['category_name'].lower() if discussion['category_name'] else ''
        body = discussion['discussion_body'].lower() if discussion['discussion_body'] else ''
        created_at = discussion['discussion_created_at']

        if 'announcements' in category_name or any(keyword in body for keyword in meetup_keywords):
            timestamps.append(created_at)
            announcements.append(discussion['discussion_body'].strip() if discussion['discussion_body'] else '')

    meetup_count = len(timestamps)
    percentage_meetups = (meetup_count / total_discussions) * 100 if total_discussions > 0 else 0

    print("\nMeetup Analysis Results:")
    print(f"Total number of discussions analyzed: {total_discussions}")
    print(f"Number of meetup/announcement discussions: {meetup_count}")
    print(f"Percentage of meetups/announcements: {percentage_meetups:.2f}%")

    meetup_details = pd.DataFrame({
        'Timestamp': timestamps,
        'Announcement': announcements
    })
    
    outcome_react85 = f"Total number of discussions analyzed: {total_discussions}. " \
                      f"Number of discussions involving in-person meetup announcements: {meetup_count}. " \
                      f"Percentage of meetups/announcements: {percentage_meetups:.2f}%."

    save_analysis("ReACT-85", outcome_react85, "Yes" if meetup_count > 0 else "No", output_file)

    return meetup_count, percentage_meetups, meetup_details

# purva
def analyze_newcomer_freedom(discussions, output_file="final_react_analysis.csv"):
    freedom_keywords = ['welcome', 'newcomer', 'new contributor', 'opinion', 'suggest', 'propose', 'idea', 'viewpoint', 'perspective']
    encouragement_phrases = ['feel free to', 'don\'t hesitate to', 'we encourage', 'your input is valuable', 'we welcome']
    
    freedom_count = 0
    total_discussions = 0
    freedom_examples = []

    for discussion in discussions:
        total_discussions += 1
        body = discussion['discussion_body'].lower() if discussion['discussion_body'] else ''
        
        if any(keyword in body for keyword in freedom_keywords) and any(phrase in body for phrase in encouragement_phrases):
            freedom_count += 1
            freedom_examples.append(body[:100] + "...")

    percentage_freedom = (freedom_count / total_discussions) * 100 if total_discussions > 0 else 0

    print("\nNewcomer Freedom Analysis Results:")
    print(f"Total number of discussions analyzed: {total_discussions}")
    print(f"Discussions encouraging newcomer freedom: {freedom_count}")
    print(f"Percentage of discussions encouraging freedom: {percentage_freedom:.2f}%")

    outcome_react89 = f"Total discussions: {total_discussions}. " \
                      f"Discussions encouraging newcomer freedom: {freedom_count}. " \
                      f"Percentage: {percentage_freedom:.2f}%. "

    recommendation = "Yes" if freedom_count > 0 and percentage_freedom > 5 else "No"
    save_analysis("ReACT-89", outcome_react89, recommendation, output_file)

    return freedom_count, percentage_freedom

# purva
def analyze_newcomer_response_time(discussions, response_threshold_hours=24):
    total_discussions = 0
    quick_responses = 0
    response_times = []

    for discussion in discussions:
        created_at = discussion.get('discussion_created_at')
        updated_at = discussion.get('discussion_updated_at')
        comments_count = discussion.get('discussion_comments', '0')

        if created_at and updated_at and comments_count:
            total_discussions += 1
            try:
                discussion_created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
                discussion_updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%SZ')
                if int(comments_count) > 0:
                    response_time = discussion_updated_at - discussion_created_at
                    response_times.append(response_time)
                    
                    if response_time <= timedelta(hours=response_threshold_hours):
                        quick_responses += 1
            except ValueError:
                continue
    
    if total_discussions > 0:
        percentage_quick_responses = (quick_responses / total_discussions) * 100
        avg_response_time = sum(response_times, timedelta()) / len(response_times) if response_times else timedelta()
        
        outcome = f"Total discussions: {total_discussions}. "
        outcome += f"Discussions with responses: {len(response_times)}. "
        outcome += f"Quick responses (within {response_threshold_hours} hours): {quick_responses}. "
        outcome += f"Percentage of quick responses: {percentage_quick_responses:.2f}%. "
        outcome += f"Average response time: {avg_response_time}"
        
        recommendation = "Yes" if percentage_quick_responses >= 80 else "No"
    else:
        outcome = "No valid discussions found in the given time period."
        recommendation = "N/A"
    
    return outcome, recommendation

# purva
def analyze_sentiment_and_save(discussions, output_file):
    total_discussions = 0
    positive_sentiments = 0
    negative_sentiments = 0
    neutral_sentiments = 0
    sentiment_scores = []

    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        if file.tell() == 0:
            writer.writerow(['Repository', 'ReACT_ID', 'Outcome', 'Recommendation'])
        
        for discussion in discussions:
            body = discussion.get('discussion_body', '')

            if body:
                total_discussions += 1
                try:
                    blob = TextBlob(body)
                    sentiment_score = blob.sentiment.polarity
                    sentiment_scores.append(sentiment_score)
                    if sentiment_score > 0:
                        positive_sentiments += 1
                    elif sentiment_score < 0:
                        negative_sentiments += 1
                    else:
                        neutral_sentiments += 1
                except Exception as e:
                    continue

        if total_discussions > 0:
            positive_percentage = (positive_sentiments / total_discussions) * 100
            negative_percentage = (negative_sentiments / total_discussions) * 100
            neutral_percentage = (neutral_sentiments / total_discussions) * 100
            avg_sentiment_score = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
            outcome = f"Total discussions: {total_discussions}. " \
                      f"Positive sentiments: {positive_sentiments}. " \
                      f"Negative sentiments: {negative_sentiments}. " \
                      f"Neutral sentiments: {neutral_sentiments}. " \
                      f"Positive %: {positive_percentage:.2f}%. " \
                      f"Negative %: {negative_percentage:.2f}%. " \
                      f"Neutral %: {neutral_percentage:.2f}%. " \
                      f"Average sentiment score: {avg_sentiment_score:.2f}"
            recommendation = "Yes" if positive_percentage >= 50 else "No"
        else:
            outcome = "No valid discussions found in the given time period."
            recommendation = "N/A"
        
        writer.writerow([
            project_name,
            'ReACT-92',
            outcome,
            recommendation
        ])


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

csv_file = 'github_api/celeborn/discussions.csv'
output_file = 'final_react_analysis.csv'

try:
    discussions = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            discussions.append(row)
except FileNotFoundError:
    print(f"Error: CSV file not found at {csv_file}")
    discussions = []

meetup_count, percentage_meetups, meetup_details = analyze_in_person_interactions(discussions, output_file)
freedom_count, percentage_freedom = analyze_newcomer_freedom(discussions, output_file)

react91_outcome, react91_recommendation = analyze_newcomer_response_time(discussions)
save_analysis("ReACT-91", react91_outcome, react91_recommendation, output_file)

analyze_sentiment_and_save(discussions, output_file)

if meetup_count > 0 or freedom_count > 0:
    print(f"Analysis complete. Results saved to {output_file}")
else:
    print("No relevant discussions found in the CSV file.")
