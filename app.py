from chatbot import SentimentChatbot
from report import generate_report
import os

class MentalHealthApp:
    def __init__(self):
        self.chatbot = SentimentChatbot()
    
    def chat(self, message):
        return self.chatbot.get_response(message)
    
    def generate_in_app_report(self):
        if not self.chatbot.conversation_history:
            return "No conversation data available for report generation."
        
        # Analyze conversation
        sentiments = [entry['sentiment'] for entry in self.chatbot.conversation_history]
        
        # Determine risk level
        if any(s == 'crisis' for s in sentiments):
            risk_level = "Critical"
        elif any(s == 'very_negative' for s in sentiments):
            risk_level = "High"
        elif any(s == 'negative' for s in sentiments):
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        # Count indicators
        indicators = {
            "Total Messages": len(self.chatbot.conversation_history),
            "Negative Sentiment": sum(1 for s in sentiments if s in ['negative', 'very_negative']),
            "Positive Sentiment": sum(1 for s in sentiments if s == 'positive'),
            "Crisis Indicators": sum(1 for s in sentiments if s == 'crisis')
        }
        
        # Medical factors from health screening
        medical_factors = {
            "Sleep Hours": self.chatbot.health_factors.get('sleep_hours', 'Not assessed'),
            "Mental Health History": self.chatbot.health_factors.get('mental_health_history', 'Not assessed'),
            "Blood Sugar Issues": self.chatbot.health_factors.get('blood_sugar_issues', 'Not assessed'),
            "Recent Life Events": self.chatbot.health_factors.get('recent_events', 'Not assessed')
        }
        
        # Generate recommendations based on risk and medical factors
        recommendations = []
        if risk_level == "Critical":
            recommendations = ["Seek immediate professional help", "Contact crisis hotline: 988", "Go to nearest emergency room if in immediate danger"]
        elif risk_level == "High":
            recommendations = ["Schedule appointment with mental health professional within 1-2 weeks", "Contact primary care physician", "Activate support network"]
        elif risk_level == "Medium":
            recommendations = ["Consider counseling or therapy", "Monitor symptoms daily", "Practice stress-reduction techniques"]
        else:
            recommendations = ["Continue positive practices", "Maintain healthy routines", "Stay connected with support system"]
        
        # Add medical-specific recommendations
        if medical_factors["Sleep Hours"] != 'Not assessed' and isinstance(medical_factors["Sleep Hours"], (int, float)) and medical_factors["Sleep Hours"] < 6:
            recommendations.append("Address sleep hygiene and consider sleep study")
        
        if medical_factors["Blood Sugar Issues"] == 'yes':
            recommendations.append("Coordinate with primary care for glucose management")
        
        # Generate report
        report_data = {
            'risk_level': risk_level,
            'indicators': indicators,
            'medical_factors': medical_factors,
            'recommendations': recommendations
        }
        
        output_path = os.path.join(os.path.dirname(__file__), "mental_health_report.pdf")
        generate_report(report_data, output_path)
        
        return f"Comprehensive report with medical assessment generated at: {output_path}"

# Simple CLI interface
if __name__ == "__main__":
    app = MentalHealthApp()
    
    print("Mental Health Support App")
    print("Type 'report' to generate report, 'quit' to exit")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'report':
            print(app.generate_in_app_report())
        else:
            response = app.chat(user_input)
            print(f"Bot: {response['reply']}")