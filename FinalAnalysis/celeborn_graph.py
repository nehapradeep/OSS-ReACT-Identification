import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, f1_score
import numpy as np

code_analysis = [
    "Yes", "Yes", "Yes", "No", "No", "Yes", "Yes", "No", "No", "No", "Yes", "Yes", 
    "Yes", "Yes", "No", "No", "Yes", "Yes", "No", "No", "Yes", "No", "No", "No", 
    "Yes", "Yes", "No", "No", "Yes", "No", "No", "Yes", "Yes", "No", "No", "Yes", 
    "Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "No", "No", "No", "No", "Yes", 
    "No", "Yes", "No", "No", "Yes", "Yes", "No", "No", "Yes", "No", "No", "No", 
    "Yes", "No", "Yes", "No"
]

manual_analysis = [
    "Yes", "Yes", "Yes", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "No", "Yes", "Yes", 
    "Yes", "Yes", "No", "No", "Yes", "Yes", "Yes", "No", "Yes", "Yes", "No", "No", 
    "Yes", "No", "No", "Yes", "Yes", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "Yes", 
    "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No", "Yes", 
    "Yes", "Yes", "No", "Yes", "Yes", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "No"
]

def map_labels(data):
    return [1 if label == "Yes" else 0 if label == "No" else None for label in data]

# Convert the string labels to numerical labels
true_labels = map_labels(manual_analysis)
predicted_labels = map_labels(code_analysis)

# Remove entries where either true_labels or predicted_labels is None (N/A or <>) 
filtered_true_labels = [true for true, pred in zip(true_labels, predicted_labels) if true is not None and pred is not None]
filtered_predicted_labels = [pred for true, pred in zip(true_labels, predicted_labels) if true is not None and pred is not None]

# Calculate confusion matrix
cm = confusion_matrix(filtered_true_labels, filtered_predicted_labels)

# Calculate F1 score
f1 = f1_score(filtered_true_labels, filtered_predicted_labels)

# Plot the confusion matrix using seaborn heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, 
            xticklabels=['Predicted No', 'Predicted Yes'], 
            yticklabels=['Actual No', 'Actual Yes'],
            linewidths=1, linecolor='white')

plt.title('Celeborn')
plt.xlabel('Predicted Labels')
plt.ylabel('Actual Labels')

plt.subplots_adjust(bottom=0.06)

# Display the F1 score below the plot
plt.figtext(0.5, -0.12, f'F1 Score: {f1:.2f}', ha='center', va='center', fontsize=14, color='crimson', weight='bold')

# Save the plot as a PNG file
plt.savefig('celeborn_graph_result.png', bbox_inches='tight')

# Close the plot to avoid issues in non-interactive environments
plt.close()