import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "dineshnampally393@gmail.com"
        self.sender_password = os.getenv("GMAIL_APP_PASSWORD")  # Use app password from environment
        
        # Check if email service is properly configured
        if not self.sender_password:
            print("Warning: GMAIL_APP_PASSWORD not found in environment variables.")
            print("Email functionality will be limited. Please set GMAIL_APP_PASSWORD in your .env file.")
        
    def send_internship_application(self, application_data):
        """
        Send internship application email
        """
        # Check if email service is properly configured
        if not self.sender_password:
            return False, "Email service not configured. Please set GMAIL_APP_PASSWORD in your .env file."
            
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"New Internship Application - {application_data['position']}"
            msg['From'] = self.sender_email
            msg['To'] = "gvkssceo@gvkss.com"
            
            # Create HTML content
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
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True, "Email sent successfully"
            
        except Exception as e:
            return False, str(e)
    
    def send_confirmation_email(self, application_data):
        """
        Send confirmation email to applicant
        """
        # Check if email service is properly configured
        if not self.sender_password:
            return False, "Email service not configured. Please set GMAIL_APP_PASSWORD in your .env file."
            
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Application Received - {application_data['position']} Internship"
            msg['From'] = self.sender_email
            msg['To'] = application_data['email']
            
            # Create HTML content
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
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
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
