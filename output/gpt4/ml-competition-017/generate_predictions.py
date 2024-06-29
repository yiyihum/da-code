import pandas as pd

# Assuming there is a pre-trained model available as 'EssayScoringModel'
from EssayScoringModel import predict_scores

def generate_submission(test_file, submission_file):
    # Load the test data
    test_data = pd.read_csv(test_file)
    
    # Generate predictions using the pre-trained model
    predictions = predict_scores(test_data['full_text'])
    
    # Create a DataFrame for the submission
    submission = pd.DataFrame({
        'essay_id': test_data['essay_id'],
        'score': predictions
    })
    
    # Save the submission file
    submission.to_csv(submission_file, index=False)

# Generate the submission file
generate_submission('test.csv', 'submission.csv')

print("Submission file generated successfully.")
