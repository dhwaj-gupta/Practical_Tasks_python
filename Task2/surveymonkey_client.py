import requests

class SurveyMonkeyClient:
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        self.api_url = 'https://api.surveymonkey.com/v3'

    def create_new_blank_survey(self, title):
        endpoint = '/surveys'
        url = self.api_url + endpoint
        payload = {
            "title": title
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def create_survey_page_question(self, survey_id, page_id, **kwargs):
        endpoint = f'/surveys/{survey_id}/pages/{page_id}/questions'
        url = self.api_url + endpoint
        response = requests.post(url, json=kwargs, headers=self.headers)
        return response.json()

    def create_new_empty_survey_page(self, survey_id):
        url = f"https://api.surveymonkey.com/v3/surveys/{survey_id}/pages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "title": "New Page Title"  # Adjust the title as needed
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for any error status code
        return response.json()

