import requests
from surveymonkey_client import SurveyMonkeyClient
API_URL = "https://api.surveymonkey.com/v3"
access_token=""
# Initialize your SurveyMonkey client
client = SurveyMonkeyClient(access_token)

def create_survey():
    # Step 1: Create a new blank survey
    survey_response = client.create_new_blank_survey(title="Survey on Productivity")

    # Extract the survey ID from the response
    survey_id = survey_response["id"]

    # Step 2: Create a new empty page for the survey
    page_response = client.create_new_empty_survey_page(survey_id)

    # Extract the page ID from the response
    page_id = page_response["id"]

    # Step 3: Create questions for the page
    questions = [
        {
            "title": "What is your age?",
            "headings": [{"heading": ""}],
            "position": 1,
            "family": "single_choice",
            "subtype": "vertical",
            "answers": [
                {"text": "Under 18"},
                {"text": "18-30"},
                {"text": "31-45"},
                {"text": "46-60"},
                {"text": "Over 60"}
            ]
        },
        {
            "title": "What do you do on your leisure time?",
            "headings": [{"heading": ""}],
            "position": 2,
            "family": "single_choice",
            "subtype": "vertical",
            "answers": [
                {"text": "Read"},
                {"text": "Watch TV"},
                {"text": "Exercise"},
                {"text": "Socialize"},
                {"text": "Other"}
            ]
        },
        {
            "title": "Are you satisfied with how you spend your free time?",
            "headings": [{"heading": ""}],
            "position": 3,
            "family": "single_choice",
            "subtype": "vertical",
            "answers": [
                {"text": "Yes"},
                {"text": "No"}
            ]
        }
    ]

    for question in questions:
        question_response = client.create_survey_page_question(survey_id, page_id, **question)
        # Optional: Extract question ID from the response if needed

    return survey_id

def send_invitations_to_survey(survey_id, recipients):
    # Define the endpoint for sending invitations
    endpoint = f"/surveys/{survey_id}/collectors/email/messages"

    # Construct the URL
    url = API_URL + endpoint

    # Define the message to be sent
    message = {
        "subject": "Invitation to participate in our survey",
        "body_text": "We kindly invite you to participate in our survey on productivity.",
        "sender_email": "dgupta@griddynamics.com",
        "reply_email": "dgupta@griddynamics.com",
        "recipients": recipients  # List of recipient email addresses
    }

    # Make a POST request to send invitations
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=message)

    # Check if the request was successful
    if response.status_code == 200:
        print("Invitations sent successfully!")
    else:
        print("Failed to send invitations. Status code:", response.status_code)

# Call the function to create a survey and get the survey ID
survey_id = create_survey()

# Define the recipients for the email invitations
recipients = ["dgupta@griddynamics.com", "rgeorge@griddynamics.com","oali@griddynamics.com"]

# Call the function to send email invitations
send_invitations_to_survey(survey_id, recipients)

