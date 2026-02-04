from trauma_chatbot import TraumaInformedChatbot, generate_trauma_report
import os

class TraumaInformedApp:
    def __init__(self):
        self.chatbot = TraumaInformedChatbot()
    
    def chat(self, message):
        return self.chatbot.get_response(message)
    
    def generate_trauma_report(self):
        if not self.chatbot.conversation_history:
            return "No conversation data available for report generation."
        
        # Analyze conversation for trauma-specific indicators
        sentiments = [entry['sentiment'] for entry in self.chatbot.conversation_history]
        trauma_indicators = sum(1 for entry in self.chatbot.conversation_history 
                              if entry.get('trauma_indicator') is not None)
        
        # Determine risk level with trauma-informed approach
        if any(s == 'crisis' for s in sentiments):
            risk_level = "Critical - Immediate Support Needed"
        elif any(s == 'severe_distress' for s in sentiments) or trauma_indicators > 2:
            risk_level = "High - Trauma-Informed Care Recommended"
        elif any(s == 'distressed' for s in sentiments) or trauma_indicators > 0:
            risk_level = "Moderate - Ongoing Support Beneficial"
        else:
            risk_level = "Stable - Continue Self-Care"
        
        # Trauma-specific factors
        trauma_factors = {
            "Total Messages": len(self.chatbot.conversation_history),
            "Trauma Disclosures": trauma_indicators,
            "Crisis Indicators": sum(1 for s in sentiments if s == 'crisis'),
            "Severe Distress Episodes": sum(1 for s in sentiments if s == 'severe_distress'),
            "Safety Concerns": 'Yes' if self.chatbot.trauma_factors.get('safety_concerns') else 'Not assessed'
        }
        
        # Generate specialized recommendations
        recommendations = []
        if risk_level.startswith("Critical"):
            recommendations = [
                "Immediate crisis intervention required",
                "Contact RAINN: 1-800-656-HOPE",
                "Consider emergency services if in immediate danger",
                "Activate safety plan if available"
            ]
        elif risk_level.startswith("High"):
            recommendations = [
                "Trauma-informed therapy strongly recommended",
                "Consider EMDR or trauma-focused CBT",
                "Establish safety planning",
                "Connect with sexual assault support center"
            ]
        elif risk_level.startswith("Moderate"):
            recommendations = [
                "Continue trauma-informed support",
                "Practice grounding and self-care techniques",
                "Consider support groups for survivors",
                "Maintain connection with trusted support system"
            ]
        else:
            recommendations = [
                "Continue current coping strategies",
                "Maintain self-care practices",
                "Stay connected with support network",
                "Remember healing is not linear"
            ]
        
        # Generate report
        report_data = {
            'risk': risk_level,
            'trauma_indicators': trauma_indicators,
            'factors': trauma_factors,
            'recommendations': recommendations
        }
        
        output_path = os.path.join(os.path.dirname(__file__), "trauma_support_report.pdf")
        generate_trauma_report(report_data, output_path)
        
        return f"SAFE AI trauma support report generated at: {output_path}"

# Simple CLI interface for trauma support
if __name__ == "__main__":
    app = TraumaInformedApp()
    
    print("🌸 SAFE AI - Trauma-Informed Support")
    print("This is a safe space. You control what you share.")
    print("Type 'report' to generate support report, 'resources' for crisis resources, 'quit' to exit")
    print("=" * 60)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Take care of yourself. You are not alone. 💙")
            break
        elif user_input.lower() == 'report':
            print(app.generate_trauma_report())
        elif user_input.lower() == 'resources':
            print("\n🆘 SAFE AI Crisis Resources:")
            print("• RAINN: 1-800-656-HOPE (4673)")
            print("• Crisis Text Line: Text HOME to 741741")
            print("• National Suicide Prevention Lifeline: 988")
            print("• Emergency: 911")
        else:
            response = app.chat(user_input)
            print(f"\nSAFE AI: {response['reply']}")
            
            if 'resources' in response:
                print("\n📞 Resources:")
                for resource in response['resources']:
                    print(f"• {resource}")
            
            if 'suggestions' in response:
                print("\n💡 Suggestions:")
                for suggestion in response['suggestions']:
                    print(f"• {suggestion}")