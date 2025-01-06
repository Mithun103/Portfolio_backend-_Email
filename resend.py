import os
from dotenv import load_dotenv
import requests
import resend
load_dotenv()

RESEND_API_KEY = os.getenv('RESEND_API_KEY')
print(f"API Key found: {'Yes' if RESEND_API_KEY else 'No'}")

response = requests.post(
    'https://api.resend.com/emails',
    headers={
        'Authorization': f'Bearer {RESEND_API_KEY}',
        'Content-Type': 'application/json'
    },
    json={
        "from": "onboarding@resend.dev",
        "to": ["msmithunof@gmail.com"],  # Replace with your email
        "subject": "Test Email",
        "html": "<p>This is a test email to verify the Resend API is working.</p>"
    }
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")