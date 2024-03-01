import smtplib
import json
import ssl
import http.client
from string import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
my_address = config["EMAIL"]
password = config["PASSWORD"].strip()
client_id = config["client_id"]
client_secret = config["client_secret"]
survey_web_link = ""

def get_template(filename):
    template_file = open(filename, mode="r", encoding="utf-8")
    template_file_content = template_file.read()
    return Template(template_file_content)

def get_usercontacts(filename):
    names = []
    emails = []
    user_list = open(filename, mode="r", encoding="utf-8")
    for user in user_list:
        names.append(user.split()[0])
        emails.append(user.split()[1])
    return names, emails
names, emails = get_usercontacts("email_addresses.txt")
message_template = get_template("template.txt")

def login(sender_email, password):
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, password)
        return server
    except Exception as e:
        print(f"Failed to login. Error: {e}")
        return None

def send_email(server, sender_email, name, invitee_email, survey_link):
    if server:
        message_body = message_template.substitute(PERSON_NAME=name, LINK=survey_link)
        # message_body = message_template.substitute(LINK={survey_link})
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = invitee_email
        message["Subject"] = "Survey Invitation"
        message.attach(MIMEText(message_body, "plain"))
        try:
            server.sendmail(sender_email, invitee_email, message.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email. Error: {e}")

def get_access_token(client_id, client_secret):
    token_url = "https://api.surveymonkey.com/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    return access_token

def survey_creation_function(access_token, title):
    conn = http.client.HTTPSConnection("api.surveymonkey.com")
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Accept': "application/json",
        "Content-Type": "application/json"
    }
    payload = {
    }
    json_payload = json.dumps(payload)
    conn.request("POST", "/v3/surveys", json_payload, headers)
    res = conn.getresponse()
    data = res.read()
    survey_data1 = json.loads(data)
    survey_id = survey_data1["id"]
    return survey_id

def insert_questions(access_token, survey_id):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    with open('survey_questions.json', 'r') as f:
        survey_questions = json.load(f)
    for page in survey_questions['pages']:
        page_payload = {
            'title': page['title']
        }
        response = requests.post(f'https://api.surveymonkey.com/v3/surveys/{survey_id}/pages', 
                                 json=page_payload, headers=headers)
        if response.status_code == 201:
            page_id = response.json()['id']
            for question in page['questions']:
                question_payload = {
                    'headings': [{'heading': question['title']}],
                    'family': 'single_choice',
                    'subtype': 'vertical',
                    'answers': {'choices': [{'text': answer} for answer in question['answers']]}
                }
                response = requests.post(f'https://api.surveymonkey.com/v3/surveys/{survey_id}/pages/{page_id}/questions',
                                         json=question_payload, headers=headers)
                if response.status_code == 201:
                    print(f"Added question '{question['title']}' to the survey page '{page['title']}'")
                else:
                    print(f"Failed to add question '{question['title']}' to the survey page '{page['title']}'")
        else:
            print(f"Failed to create page '{page['title']}' for the survey")

def create_web_link_collector(survey_id):
    conn = http.client.HTTPSConnection("api.surveymonkey.com")
    payload = {
        "type": "weblink",
        "name": "web_link_collector",
        "thank_you_page": {
            "is_enabled": True,
            "message": "Thank you for completing the survey!"
        },
        "thank_you_message": "Thank you!",
        "display_survey_results": True,
        "allow_multiple_responses": True
    }
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    json_payload = json.dumps(payload)
    conn.request("POST", f"/v3/surveys/{survey_id}/collectors", json_payload, headers)
    res = conn.getresponse()
    collector_data = json.loads(res.read().decode("utf-8"))
    print(collector_data)
    return collector_data.get("url", None)

def send_survey_invitations(survey_link, emails, names):
    sender_email = my_address
    server = login(sender_email, password)
    if server:
        for name,email in zip(names,emails):
            send_email(server, sender_email, name, email, survey_link)
        server.quit()

if __name__ == "__main__":
    access_token = get_access_token(client_id, client_secret)
    with open("survey_questions.json", "r") as f:
        survey_questions = json.load(f)
    survey_name = "Survey on Productivity"
    survey_id = survey_creation_function(access_token,survey_name)
    insert_questions(access_token, survey_id)
    survey_web_link = create_web_link_collector(survey_id)
    send_survey_invitations(survey_web_link, emails, names)
