import os
import json
import smtplib
import urllib.request
import urllib.error
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    print(f"Note: dotenv not loaded ({e}). Using environment variables only (e.g. Render env vars).")

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.environ.get("SENDER_EMAIL", "").strip()
        self.sender_password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
        self.resend_api_key = os.environ.get("RESEND_API_KEY", "").strip()
        # EmailJS: service ID, template IDs, user ID (public key), private key (for server)
        self.emailjs_service_id = os.environ.get("EMAILJS_SERVICE_ID", "").strip()
        self.emailjs_template_application = os.environ.get("EMAILJS_TEMPLATE_APPLICATION", "").strip()
        self.emailjs_template_confirmation = os.environ.get("EMAILJS_TEMPLATE_CONFIRMATION", "").strip()
        self.emailjs_user_id = os.environ.get("EMAILJS_USER_ID", "").strip()
        self.emailjs_private_key = os.environ.get("EMAILJS_PRIVATE_KEY", "").strip()

        self._use_emailjs = all((
            self.emailjs_service_id,
            self.emailjs_template_application,
            self.emailjs_template_confirmation,
            self.emailjs_user_id,
        ))

        if self._use_emailjs:
            print("Email service: Using EmailJS (service + templates + keys).")
        elif self.resend_api_key and self.sender_email:
            print("Email service: Using Resend API (works on Render when SMTP is blocked).")
        elif self.sender_password and self.sender_email:
            print("Email service: Using Gmail SMTP.")
        else:
            if not self.sender_email and not self._use_emailjs:
                print("Warning: SENDER_EMAIL not set.")
            if not self._use_emailjs and not self.resend_api_key and not self.sender_password:
                print("Warning: Set EmailJS vars, RESEND_API_KEY, or GMAIL_APP_PASSWORD. See .env.example.")

    def is_configured(self):
        """True if we can send (EmailJS, Resend, or Gmail configured)."""
        if self._use_emailjs:
            return True
        return bool(self.sender_email and (self.resend_api_key or self.sender_password))

    def _template_params(self, application_data):
        """Build template params for EmailJS (use {{name}} in your EmailJS templates)."""
        return {
            "fullName": application_data.get("fullName", ""),
            "email": application_data.get("email", ""),
            "phone": application_data.get("phone", ""),
            "position": application_data.get("position", ""),
            "university": application_data.get("university", ""),
            "graduationYear": application_data.get("graduationYear", ""),
            "skills": application_data.get("skills", ""),
            "motivation": application_data.get("motivation", ""),
            "resume": application_data.get("resume_link", application_data.get("resume", "")),
            "timestamp": application_data.get("timestamp", ""),
        }

    def _send_via_emailjs(self, template_id, template_params, to_email=None):
        """Send email via EmailJS REST API (works on Render, no SMTP)."""
        params = dict(template_params)
        if to_email is not None:
            params["to_email"] = to_email
        payload = {
            "service_id": self.emailjs_service_id,
            "template_id": template_id,
            "user_id": self.emailjs_user_id,
            "template_params": params,
        }
        if self.emailjs_private_key:
            payload["accessToken"] = self.emailjs_private_key
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        req = urllib.request.Request(
            "https://api.emailjs.com/api/v1.0/email/send",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return True, "Email sent successfully"
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace") if e.fp else ""
            msg = f"EmailJS API {e.code}: {body or e.reason}"
            if e.code == 403 and "1010" in body:
                msg += " Add EMAILJS_PRIVATE_KEY to .env (Dashboard → Account → Security). If it still fails, Cloudflare may block server IPs; use Resend instead for backend."
            return False, msg

    def _send_via_resend(self, to_email, subject, html):
        """Send one email via Resend HTTP API (works when SMTP is blocked, e.g. on Render)."""
        req = urllib.request.Request(
            "https://api.resend.com/emails",
            data=json.dumps({
                "from": self.sender_email,
                "to": [to_email],
                "subject": subject,
                "html": html,
            }).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.resend_api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return True, "Email sent successfully"
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace") if e.fp else ""
            return False, f"Resend API {e.code}: {body or e.reason}"

    def send_internship_application(self, application_data):
        """
        Send internship application email to GVKSS.
        Uses EmailJS, Resend, or Gmail SMTP depending on env config.
        """
        if self._use_emailjs:
            return self._send_via_emailjs(
                self.emailjs_template_application,
                self._template_params(application_data),
                to_email="gvkssceo@gvkss.com",
            )

        if not self.sender_email:
            return False, "SENDER_EMAIL not set."
        if not self.resend_api_key and not self.sender_password:
            return False, "Set EmailJS, RESEND_API_KEY, or GMAIL_APP_PASSWORD."

        html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #22c55e; border-bottom: 2px solid #22c55e; padding-bottom: 10px;">
                        🎯 New Internship Application Received
                    </h2>
                    
                    <h3 style="color: #166534;">Position: {application_data['position']}</h3>
                    
                    <table style="width: 100%; border-collapse: collapse; margin: 20px 0; border: 1px solid #ddd;">
                        <tr style="background-color: #f8f9fa;">
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold; width: 30%;">Full Name</td>
                            <td style="padding: 12px; border: 1px solid #ddd;">{application_data['fullName']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Email</td>
                            <td style="padding: 12px; border: 1px solid #ddd;">{application_data['email']}</td>
                        </tr>
                        <tr style="background-color: #f8f9fa;">
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Phone</td>
                            <td style="padding: 12px; border: 1px solid #ddd;">{application_data['phone']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">University</td>
                            <td style="padding: 12px; border: 1px solid #ddd;">{application_data['university']}</td>
                        </tr>
                        <tr style="background-color: #f8f9fa;">
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Graduation Year</td>
                            <td style="padding: 12px; border: 1px solid #ddd;">{application_data['graduationYear']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Skills</td>
                            <td style="padding: 12px; border: 1px solid #ddd;">{application_data['skills']}</td>
                        </tr>
                        <tr style="background-color: #f8f9fa;">
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Motivation</td>
                            <td style="padding: 12px; border: 1px solid #ddd;">{application_data['motivation']}</td>
                        </tr>
                    </table>
                    
                    <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 15px; margin: 20px 0;">
                        <p style="margin: 0; color: #166534;">
                            <strong>Application submitted on:</strong> {application_data.get('timestamp', 'N/A')}
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <p style="color: #666; font-size: 14px;">
                            This is an automated message from the GVKSS Internship Bot.
                            Please review the application and respond to the candidate directly.
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """

        if self.resend_api_key:
            try:
                return self._send_via_resend("gvkssceo@gvkss.com", f"New Internship Application - {application_data['position']}", html_content)
            except Exception as e:
                return False, str(e)

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"New Internship Application - {application_data['position']}"
            msg['From'] = self.sender_email
            msg['To'] = "gvkssceo@gvkss.com"
            msg.attach(MIMEText(html_content, 'html'))
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=12) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            return True, "Email sent successfully"
        except Exception as e:
            return False, str(e)

    def send_confirmation_email(self, application_data):
        """
        Send confirmation email to applicant.
        Uses EmailJS, Resend, or Gmail SMTP depending on env config.
        """
        if self._use_emailjs:
            return self._send_via_emailjs(
                self.emailjs_template_confirmation,
                self._template_params(application_data),
                to_email=application_data.get("email", ""),
            )

        if not self.sender_email:
            return False, "SENDER_EMAIL not set."
        if not self.resend_api_key and not self.sender_password:
            return False, "Set EmailJS, RESEND_API_KEY, or GMAIL_APP_PASSWORD."

        html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #22c55e; border-bottom: 2px solid #22c55e; padding-bottom: 10px;">
                        🎉 Application Received Successfully!
                    </h2>
                    
                    <p>Dear <strong>{application_data['fullName']}</strong>,</p>
                    
                    <p>Thank you for your interest in the <strong>{application_data['position']}</strong> internship position at GVKSS.</p>
                    
                    <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 15px; margin: 20px 0;">
                        <h3 style="color: #166534; margin-top: 0;">Application Details</h3>
                        <p><strong>Position:</strong> {application_data['position']}</p>
                        <p><strong>University:</strong> {application_data['university']}</p>
                        <p><strong>Expected Graduation:</strong> {application_data['graduationYear']}</p>
                    </div>
                    
                    <h3 style="color: #166534;">Next Steps</h3>
                    <ul>
                        <li>Our team will review your application within 3-5 business days</li>
                        <li>You will receive a response via email or phone</li>
                        <li>If selected, we will schedule an interview</li>
                    </ul>
                    
                    <div style="background-color: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 15px; margin: 20px 0;">
                        <p style="margin: 0; color: #92400e;">
                            <strong>Note:</strong> Please keep this email for your records. 
                            If you have any questions, feel free to contact us.
                        </p>
                    </div>
                    
                    <h3 style="color: #166534;">Contact Information</h3>
                    <p><strong>Email:</strong> gvkssceo@gvkss.com</p>
                    <p><strong>Phone:</strong> +91 7441 143 143</p>
                    <p><strong>Website:</strong> www.gvkss.com</p>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <p style="color: #666; font-size: 14px;">
                            Best regards,<br>
                            GVKSS Internship Team
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """

        if self.resend_api_key:
            try:
                return self._send_via_resend(
                    application_data['email'],
                    f"Application Received - {application_data['position']} Internship",
                    html_content,
                )
            except Exception as e:
                return False, str(e)

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Application Received - {application_data['position']} Internship"
            msg['From'] = self.sender_email
            msg['To'] = application_data['email']
            msg.attach(MIMEText(html_content, 'html'))
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=12) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            return True, "Confirmation email sent successfully"
        except Exception as e:
            return False, str(e)

# Example usage
if __name__ == "__main__":
    email_service = EmailService()
    
    # Test application data
    test_application = {
        'position': 'Full-Stack Web Development',
        'fullName': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '+1234567890',
        'university': 'Test University',
        'graduationYear': '2025',
        'skills': 'React, Node.js, Python',
        'motivation': 'I want to learn and grow in web development',
        'timestamp': '2024-01-15 10:30:00'
    }
    
    # Send application email
    success, message = email_service.send_internship_application(test_application)
    print(f"Application email: {message}")
    
    # Send confirmation email
    success, message = email_service.send_confirmation_email(test_application)
    print(f"Confirmation email: {message}")
