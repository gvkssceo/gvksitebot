import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from email_service import EmailService
from datetime import datetime

app = Flask(__name__)

# CORS: allow frontend at https://www.gvkss.com (and gvkss.com) to call this API
ALLOWED_ORIGINS = ["https://www.gvkss.com", "https://gvkss.com"]
CORS(
    app,
    resources={r"/api/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept"],
        "expose_headers": ["Content-Type"],
    }},
    supports_credentials=False,
)

try:
    email_service = EmailService()
    print("Email service initialized successfully")
except Exception as e:
    print(f"Warning: Email service initialization failed: {e}")
    print("Email functionality will be limited")
    email_service = None

def _get_request_data():
    """Get payload from either JSON body or form data (for CORS/frontend compatibility)."""
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form


@app.route('/api/send-email', methods=['POST', 'OPTIONS'])
def send_email():
    """
    API endpoint to send internship application emails with resume link.
    Accepts application/json or application/x-www-form-urlencoded.
    """
    if request.method == "OPTIONS":
        return "", 204

    try:
        data = _get_request_data()
        position = data.get('position')
        fullName = data.get('fullName')
        email = data.get('email')
        phone = data.get('phone')
        university = data.get('university')
        graduationYear = data.get('graduationYear')
        skills = data.get('skills')
        motivation = data.get('motivation')
        resume_link = data.get('resume')

        # Validate required fields
        required_fields = ['position', 'fullName', 'email', 'phone', 'university', 'graduationYear', 'skills', 'motivation', 'resume']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Validate resume link format
        if not resume_link or not str(resume_link).startswith(('http://', 'https://')):
            return jsonify({'error': 'Please provide a valid URL for your resume'}), 400
        
        # Prepare application data
        application_data = {
            'position': position,
            'fullName': fullName,
            'email': email,
            'phone': phone,
            'university': university,
            'graduationYear': graduationYear,
            'skills': skills,
            'motivation': motivation,
            'resume_link': resume_link,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Check if email service is available
        if email_service is None:
            return jsonify({
                'success': True,
                'message': 'Application received successfully (email service not available)',
                'application_id': f"APP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'email_sent': False,
                'confirmation_sent': False,
                'note': 'Email service is not configured. Set GMAIL_APP_PASSWORD in Render Dashboard (Environment) or .env.'
            }), 200
        
        # Send application email to GVKSS team
        success, message = email_service.send_internship_application(application_data)

        if not success:
            # When email is not configured (e.g. no GMAIL_APP_PASSWORD), return 200 so local/testing works
            if 'not configured' in message.lower():
                return jsonify({
                    'success': True,
                    'message': 'Application received (email not configured)',
                    'application_id': f"APP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    'email_sent': False,
                    'confirmation_sent': False,
                    'note': message
                }), 200
            return jsonify({'error': f'Failed to send application email: {message}'}), 500
        
        # Send confirmation email to applicant
        confirmation_success, confirmation_message = email_service.send_confirmation_email(application_data)
        
        if not confirmation_success:
            # Log warning but don't fail the request
            print(f"Warning: Failed to send confirmation email: {confirmation_message}")
        
        return jsonify({
            'success': True,
            'message': 'Application submitted successfully',
            'application_id': f"APP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'email_sent': True,
            'confirmation_sent': confirmation_success,
            'resume_link_provided': True
        }), 200
        
    except Exception as e:
        print(f"Error in send_email endpoint: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'service': 'GVKSS Internship Email Service',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint
    """
    return jsonify({
        'message': 'GVKSS Internship Email Service',
        'endpoints': {
            'send_email': '/api/send-email',
            'health': '/api/health'
        },
        'usage': 'POST to /api/send-email with application data to send internship application emails'
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
