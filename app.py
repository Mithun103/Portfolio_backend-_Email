from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get API key from .env
RESEND_API_KEY = os.getenv('RESEND_API_KEY')
if not RESEND_API_KEY:
    logger.error("Resend API key not found in environment variables.")
    exit(1)

@app.route('/')
def home():
    return jsonify({'message': 'Server is running'}), 200

@app.route('/api/contact', methods=['POST'])
def send_support_message():
    try:
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        print(data)
        if not all([name, email, message]):
            missing_fields = [field for field in ['name', 'email', 'message'] if not data.get(field)]
            return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400

        email_data = {
            "from": "Support System <onboarding@resend.dev>",
            "to": ["msmithunof@gmail.com"],
            "reply_to": email,
            "subject": f"New Support Message from {name}",
            "html": f"""
                <h2>MESSAGE FROM PORTFOLIO</h2>
                <p><strong>From:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Message:</strong></p>
                <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
                    {message}
                </div>
            """
        }

        response = requests.post(
            'https://api.resend.com/emails',
            headers={
                'Authorization': f'Bearer {RESEND_API_KEY}',
                'Content-Type': 'application/json'
            },
            json=email_data
        )

        if response.status_code == 200:
            confirmation_data = {
                "from": "Support System <onboarding@resend.dev>",
                "to": [email],
                "subject": "We received your message",
                "html": f"""
                    <h2>Thank you for contacting us!</h2>
                    <p>Dear {name},</p>
                    <p>We have received your message and will get back to you soon.</p>
                    <p>Best regards,<br>Support Team</p>
                """
            }

            requests.post(
                'https://api.resend.com/emails',
                headers={
                    'Authorization': f'Bearer {RESEND_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json=confirmation_data
            )

            return jsonify({'message': 'Message sent successfully'}), 200
        else:
            logger.error(f"Resend API error: {response.text}")
            return jsonify({
                'error': 'Failed to send message',
                'status_code': response.status_code,
                'response': response.text
            }), 500

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    app.run(debug=True)
