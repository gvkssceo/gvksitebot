# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
import datetime

class ActionGetInternshipInfo(Action):
    def name(self) -> Text:
        return "action_get_internship_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        internship_name = tracker.get_slot("internship_name")
        
        if not internship_name:
            dispatcher.utter_message(text="I'm sorry, I couldn't identify which internship you're interested in. Please select one from the options.")
            return []
        
        # Internship descriptions
        internship_descriptions = {
            "Full-Stack Web Development": {
                "description": "Learn to build complete web applications using modern technologies like React, Node.js, and databases. You'll work on real projects and gain experience with both frontend and backend development.",
                "skills": "HTML, CSS, JavaScript, React, Node.js, databases",
                "duration": "3-6 months",
                "stipend": "$800-1200/month"
            },
            "Mobile App Development": {
                "description": "Develop mobile applications for iOS and Android platforms. Learn React Native, Flutter, or native development. Work on user experience and mobile-specific features.",
                "skills": "React Native, Flutter, mobile UI/UX, app store deployment",
                "duration": "3-6 months",
                "stipend": "$800-1200/month"
            },
            "UI/UX Design & Prototyping": {
                "description": "Create beautiful and functional user interfaces. Learn design principles, prototyping tools, and user research methods. Work on real design projects.",
                "skills": "Figma, Adobe XD, design principles, user research, prototyping",
                "duration": "3-6 months",
                "stipend": "$700-1000/month"
            },
            "Data Science & Machine Learning": {
                "description": "Work with large datasets, build machine learning models, and create data-driven insights. Learn Python, statistics, and ML frameworks.",
                "skills": "Python, pandas, scikit-learn, statistics, data visualization",
                "duration": "3-6 months",
                "stipend": "$900-1300/month"
            },
            "Cybersecurity & Ethical Hacking": {
                "description": "Learn about network security, penetration testing, and ethical hacking. Work on security assessments and learn to protect systems from threats.",
                "skills": "Network security, penetration testing, ethical hacking, security tools",
                "duration": "3-6 months",
                "stipend": "$900-1300/month"
            }
        }
        
        if internship_name in internship_descriptions:
            info = internship_descriptions[internship_name]
            
            message = f"""
🎯 **{internship_name} Internship**

📅 **Duration:** {info['duration']}
💰 **Stipend:** {info['stipend']}
🌍 **Location:** Remote/Hybrid

📝 **Description:**
{info['description']}

🛠️ **Skills You'll Learn:**
{info['skills']}

Would you like to apply for this position?
            """
            
            dispatcher.utter_message(
                text=message,
                buttons=[
                    {"title": "Apply Now", "payload": "/apply_internship"},
                    {"title": "View Other Internships", "payload": "/show_internships"},
                    {"title": "Back to Main Menu", "payload": "/greet"}
                ]
            )
        else:
            dispatcher.utter_message(text=f"I'm sorry, I don't have information about {internship_name}. Please select from our available options.")
        
        return []

class ActionSaveApplication(Action):
    def name(self) -> Text:
        return "action_save_application"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get all the form data
        full_name = tracker.get_slot("full_name")
        email = tracker.get_slot("email")
        phone = tracker.get_slot("phone")
        university = tracker.get_slot("university")
        graduation_year = tracker.get_slot("graduation_year")
        skills = tracker.get_slot("skills")
        motivation = tracker.get_slot("motivation")
        internship_name = tracker.get_slot("internship_name")
        
        # Create application summary
        application_summary = f"""
🎉 **Application Submitted Successfully!**

📋 **Application Details:**
- **Position:** {internship_name}
- **Name:** {full_name}
- **Email:** {email}
- **Phone:** {phone}
- **University:** {university}
- **Graduation Year:** {graduation_year}

💡 **Skills:** {skills}
🎯 **Motivation:** {motivation}

📧 **Next Steps:**
Our team will review your application and contact you within 3-5 business days. You'll receive a confirmation email at {email}.

Thank you for your interest in our internship program!
        """
        
        dispatcher.utter_message(text=application_summary)
        
        # In a real application, you would save this to a database
        # For now, we'll just log it
        print(f"New application received for {internship_name} from {full_name} ({email})")
        
        return []
