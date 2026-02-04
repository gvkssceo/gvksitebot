# GVKSS Internship Email Service

This backend service handles sending internship application emails via SMTP using Gmail.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Gmail App Password

1. Go to your Google Account settings: https://myaccount.google.com/
2. Navigate to Security > 2-Step Verification
3. Scroll down and click on "App passwords"
4. Generate a new app password for "Mail"
5. Copy the 16-character password

### 3. Create Environment File
Create a `.env` file in the backend directory:
```bash
# Gmail App Password for SMTP
GMAIL_APP_PASSWORD=your_16_character_app_password_here

# Email Configuration
SENDER_EMAIL=dineshnampally393@gmail.com
RECIPIENT_EMAIL=gvkssceo@gvkss.com
```

### 4. Run the Service
```bash
python app.py
```

The service will run on `http://localhost:5001`

## API Endpoints

### POST /api/send-email
Sends internship application emails.

**Request Body:**
```json
{
  "position": "Full-Stack Web Development",
  "fullName": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "university": "Test University",
  "graduationYear": "2025",
  "skills": "React, Node.js, Python",
  "motivation": "I want to learn and grow in web development"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Application submitted successfully",
  "application_id": "APP_20240115_103000",
  "email_sent": true,
  "confirmation_sent": true
}
```

### GET /api/health
Health check endpoint.

### GET /
Service information and available endpoints.

## Email Features

- **Application Email**: Sent to GVKSS team (gvkssceo@gvkss.com)
- **Confirmation Email**: Sent to applicant with application details
- **HTML Formatting**: Professional email templates with styling
- **Error Handling**: Comprehensive error handling and logging

## Security Notes

- Use Gmail App Password, not your regular password
- Keep the .env file secure and never commit it to version control
- The service runs on localhost by default for security

## Troubleshooting

1. **SMTP Authentication Error**: Check your Gmail app password
2. **Port Already in Use**: Change the port in app.py
3. **CORS Issues**: Ensure the frontend URL is allowed in CORS settings
