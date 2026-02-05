# GVKSS Internship Chatbot - Ginie 🤖

A modern, responsive chatbot application for GVKSS internship applications with SMTP email integration. Meet **Ginie**, your intelligent internship assistant!

## ✨ Features

- **🤖 Intelligent Chatbot (Ginie)**: Interactive conversation flow for internship inquiries
- **📝 Application Forms**: Complete internship application forms with validation
- **📧 SMTP Email Integration**: Automatic email sending to both GVKSS team and applicants
- **📱 Responsive Design**: Mobile-first design that works on all devices
- **🎨 Professional UI**: Beautiful green and white theme with modern chat interface
- **🔧 Rasa Backend**: AI-powered conversation management
- **⚡ Real-time Updates**: Live chat with typing indicators
- **👤 Professional Avatar**: Ginie with professional appearance and role
- **🔔 Notification Badge**: Visual indicator for new messages
- **📎 Enhanced Input**: Multiple input options (thumbs up, attachments, emojis)

## 🚀 Quick Start

### Option 1: Run Everything (Recommended for Development)
```bash
# Terminal 1: Start Rasa backend
rasa run --enable-api --cors "*" --port 5005

# Terminal 2: Start action server (required for applications to be taken)
rasa run actions

# Terminal 3: Start email backend service
cd backend
python app.py   # On Windows if "Python not found", use: py -3 app.py  or  run-backend.bat

# Terminal 4: Start React frontend
cd frontendx
npm start
```

### Option 2: Run Components Individually
```bash
# Start only Rasa
rasa run --enable-api --cors "*" --port 5005

# Start only email service
cd backend && python app.py   # Windows: use  py -3 app.py  or  run-backend.bat  from repo root

# Start only frontend
cd frontend && npm start
```

## 📋 Prerequisites

- **Python 3.8+** (for Rasa and email service)
- **Node.js 16+** (for React frontend)
- **Gmail Account** with App Password for SMTP
- **Git** for version control

### Windows: if `python` is not found

Use the **Python launcher** or the project **venv**:

```cmd
REM From repo root (gvksitebot-main) - option 1: batch file
run-backend.bat

REM Option 2: Python launcher
py -3 app.py

REM Option 3: venv (after creating .venv and installing deps)
.venv\Scripts\python.exe app.py
```

Default port is 5001 (or set `PORT=5001`). The API will be at `http://127.0.0.1:5001`.

## 🛠️ Installation & Setup

### Backend Setup (Rasa + Email Service)

1. **Clone and navigate to project**
   ```bash
   cd bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Rasa dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install email service dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

5. **Configure Gmail App Password**
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Navigate to Security > 2-Step Verification
   - Click "App passwords" and generate one for "Mail"
   - Copy the 16-character password

6. **Create environment file**
   ```bash
   # In backend/ directory
   echo "GMAIL_APP_PASSWORD=your_16_character_app_password_here" > .env
   ```

7. **Train the bot**
   ```bash
   cd ..  # Back to bot/ directory
   rasa train
   ```

### Frontend Setup (React)

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

## 🚀 Running the System

### 1. Start Rasa Backend
```bash
# Terminal 1
rasa run --enable-api --cors "*" --port 5005
```
- Runs on: `http://localhost:5005`
- Handles: Chatbot conversations and actions

### 2. Start Action Server
```bash
# Terminal 2
rasa run actions
```
- Runs on: `http://localhost:5055`
- Handles: Custom actions and responses

### 3. Start Email Service
```bash
# Terminal 3
cd backend
python app.py
```
- Runs on: `http://localhost:5001`
- Handles: SMTP email sending for applications

### 4. Start React Frontend
```bash
# Terminal 4
cd frontend
npm start
```
- Runs on: `http://localhost:3000`
- Handles: User interface and chat widget

## 🧪 Testing the Complete System

1. **Open browser** and navigate to `http://localhost:3000`
2. **Click the chat button** (bottom-right corner)
3. **Test conversation flow**:
   - Ask about internships
   - Learn about GVKSS
   - Start an application
4. **Fill out application form** and submit
5. **Check emails**:
   - Application sent to `gvkssceo@gvkss.com`
   - Confirmation sent to applicant's email

## 📁 Project Structure

```
bot/
├── actions/                 # Rasa custom actions
├── data/                   # Training data (NLU, stories, rules)
├── models/                 # Trained Rasa models
├── backend/                # Email service backend
│   ├── app.py             # Flask API server
│   ├── email_service.py   # SMTP email functionality
│   ├── requirements.txt   # Python dependencies
│   └── README.md          # Backend setup guide
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   │   └── ChatWidget.js  # Main chat interface
│   │   ├── App.js         # Root component
│   │   └── App.css        # Global styles
│   ├── package.json       # Node.js dependencies
│   └── README.md          # Frontend setup guide
├── config.yml              # Rasa configuration
├── domain.yml              # Rasa domain
├── endpoints.yml           # Rasa endpoints
└── requirements.txt        # Rasa dependencies
```

## 🔧 Configuration Files

### Rasa Configuration
- **`config.yml`**: Pipeline and policies for NLU and dialogue
- **`domain.yml`**: Intents, entities, actions, and responses
- **`endpoints.yml`**: API endpoints and action server URLs

### Email Service Configuration
- **`backend/.env`**: Gmail app password and email settings
- **`backend/app.py`**: Flask server configuration and API endpoints

### Frontend Configuration
- **`frontend/package.json`**: React dependencies and scripts
- **`frontend/src/components/ChatWidget.js`**: Chat interface styling and logic

## 📧 Email Integration

### SMTP Configuration
- **Provider**: Gmail SMTP
- **Server**: `smtp.gmail.com:587`
- **Authentication**: App Password (not regular password)
- **From**: `dineshnampally393@gmail.com`
- **To**: `gvkssceo@gvkss.com`

### Email Types
1. **Application Email**: Sent to GVKSS team with complete application details
2. **Confirmation Email**: Sent to applicant with application confirmation and next steps

### Email Features
- HTML formatting with professional styling
- Application details in organized tables
- Contact information and next steps
- Error handling and logging

## 📱 Responsiveness Features

### Mobile-First Design
- Responsive chat widget positioning
- Adaptive sizing for different screen sizes
- Touch-friendly interface elements
- Landscape and portrait orientation support

### Breakpoint Support
- **Desktop**: 1024px+ (full-size interface)
- **Tablet**: 768px-1024px (medium interface)
- **Mobile**: 480px-768px (compact interface)
- **Small Mobile**: <480px (minimal interface)

## 🔍 API Integration

### Frontend → Backend Communication
- **Rasa API**: `http://localhost:5005/webhooks/rest/webhook`
- **Email API**: `http://localhost:5001/api/send-email`

### API Endpoints
- **`POST /api/send-email`**: Submit internship applications
- **`GET /api/health`**: Health check for email service
- **`GET /`**: Service information and documentation

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Change ports in respective config files
   # Rasa: config.yml or command line
   # Email: backend/app.py
   # React: package.json scripts
   ```

2. **SMTP Authentication Error**
   - Verify Gmail app password is correct
   - Ensure 2-factor authentication is enabled
   - Check `.env` file exists in backend directory

3. **CORS Issues**
   - Verify Rasa CORS settings: `--cors "*"`
   - Check frontend API endpoint URLs
   - Ensure all services are running

4. **Module Not Found Errors**
   - Activate virtual environment
   - Install missing dependencies
   - Check Python/Node.js versions

### Debug Commands

```bash
# Test Rasa
rasa shell

# Test email service
cd backend && python email_service.py

# Check React build
cd frontend && npm run build

# View logs
rasa run --enable-api --cors "*" --port 5005 --debug
```

## 🚀 Deployment

### Production Considerations
- Use environment variables for sensitive data
- Set up proper CORS policies
- Configure production SMTP service
- Use HTTPS for all communications
- Set up monitoring and logging

### Docker Deployment (Optional)
```dockerfile
# Example Dockerfile for email service
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "app.py"]
```

## 🧪 Testing

### Manual Testing
- Test all conversation flows
- Verify form submissions
- Check email delivery
- Test responsive design on different devices

### Test email API from Command Prompt (cmd)

Use `curl` (Windows 10+). Start the backend first (e.g. `python app.py` on port 5001).

```cmd
REM Health check
curl -s http://127.0.0.1:5001/api/health

REM POST send-email (one line)
curl -s -X POST http://127.0.0.1:5001/api/send-email -H "Content-Type: application/json" -d "{\"position\":\"Test\",\"fullName\":\"Test User\",\"email\":\"test@example.com\",\"phone\":\"+1\",\"university\":\"U\",\"graduationYear\":\"2025\",\"skills\":\"X\",\"motivation\":\"Y\",\"resume\":\"https://example.com/r.pdf\"}"
```

In **PowerShell** use `Invoke-WebRequest`; in **cmd** use `curl` as above.

### Automated Testing
```bash
# Rasa testing
rasa test

# Frontend testing
cd frontend && npm test

# Email service testing
cd backend && python -m pytest
```

## 📚 Additional Resources

- [Rasa Documentation](https://rasa.com/docs/)
- [React Documentation](https://reactjs.org/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is proprietary to GVKSS. All rights reserved.

---

**Need Help?** Contact the development team or refer to the troubleshooting section above.
