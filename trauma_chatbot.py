import json
from textblob import TextBlob
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class TraumaInformedChatbot:
    def __init__(self):
        self.crisis_keywords = ['suicide', 'kill myself', 'hurt myself', 'want to die', 'end my life', 'not safe', 'harm myself']
        self.trauma_keywords = ['assault', 'rape', 'abuse', 'attacked', 'violated', 'forced', 'unwanted touch', 'sexual violence']
        self.ptsd_keywords = ['flashbacks', 'nightmares', 'triggered', 'panic attacks', 'hypervigilant', 'dissociate', 'numb']
        
        self.conversation_history = []
        self.trauma_factors = {
            'trauma_type': None,
            'time_since_trauma': None,
            'support_system': None,
            'therapy_history': None,
            'safety_concerns': None,
            'ptsd_symptoms': None
        }
        
        self.safety_first = True
        
    def analyze_sentiment(self, message):
        blob = TextBlob(message)
        sentiment = blob.sentiment
        
        if sentiment.polarity < -0.6:
            return 'severe_distress'
        elif sentiment.polarity < -0.3:
            return 'distressed'
        elif sentiment.polarity < -0.1:
            return 'negative'
        elif sentiment.polarity > 0.1:
            return 'positive'
        else:
            return 'neutral'
    
    def detect_trauma_indicators(self, message):
        message_lower = message.lower()
        
        # Check for trauma-related content
        if any(keyword in message_lower for keyword in self.trauma_keywords):
            return 'trauma_disclosure'
        
        # Check for PTSD symptoms
        if any(keyword in message_lower for keyword in self.ptsd_keywords):
            return 'ptsd_symptoms'
        
        return None
    
    def check_trauma_factors(self, message):
        message_lower = message.lower()
        
        # Safety assessment
        if any(word in message_lower for word in ['unsafe', 'danger', 'threat', 'scared', 'afraid']):
            if self.trauma_factors['safety_concerns'] is None:
                return "Your safety is my primary concern. Are you currently in a safe place? Do you feel safe right now?"
        
        # Support system inquiry
        if any(word in message_lower for word in ['alone', 'isolated', 'no one', 'lonely']):
            if self.trauma_factors['support_system'] is None:
                return "Having support is crucial for healing. Do you have trusted people in your life you can talk to - friends, family, or professionals?"
        
        # Therapy/treatment history
        if any(word in message_lower for word in ['therapy', 'counselor', 'treatment', 'help']):
            if self.trauma_factors['therapy_history'] is None:
                return "Professional support can be very helpful. Have you worked with a trauma-informed therapist or counselor before?"
        
        return None
    
    def get_response(self, message):
        sentiment = self.analyze_sentiment(message)
        trauma_indicator = self.detect_trauma_indicators(message)
        
        self.conversation_history.append({
            'message': message, 
            'sentiment': sentiment,
            'trauma_indicator': trauma_indicator
        })
        
        # Priority 1: Crisis detection
        if any(keyword in message.lower() for keyword in self.crisis_keywords):
            return {
                'reply': 'I\'m very concerned about your safety right now. Please reach out for immediate help:\n• Call 911 if in immediate danger\n• National Suicide Prevention Lifeline: 988\n• Crisis Text Line: Text HOME to 741741\n\nYou matter, and there are people who want to help you.',
                'sentiment': 'crisis',
                'emergency': True,
                'resources': ['911', '988', 'Crisis Text Line: 741741']
            }
        
        # Priority 2: Trauma disclosure response
        if trauma_indicator == 'trauma_disclosure':
            return {
                'reply': 'Thank you for trusting me with something so difficult to share. What happened to you was not your fault. You showed incredible strength by surviving and reaching out. I\'m here to support you in whatever way feels helpful right now.',
                'sentiment': 'trauma_support',
                'validation': True,
                'resources': ['RAINN: 1-800-656-HOPE', 'Crisis Text Line: 741741']
            }
        
        # Priority 3: PTSD symptoms support
        if trauma_indicator == 'ptsd_symptoms':
            return {
                'reply': 'What you\'re experiencing sounds like trauma responses, which are normal reactions to abnormal experiences. These symptoms can be very distressing, but they can improve with proper support and treatment. Have you been able to connect with a trauma-informed therapist?',
                'sentiment': 'ptsd_support',
                'suggestions': ['Grounding techniques', 'Deep breathing', 'Professional trauma therapy']
            }
        
        # Check for trauma-specific factors
        trauma_question = self.check_trauma_factors(message)
        if trauma_question:
            return {
                'reply': trauma_question,
                'sentiment': 'assessment',
                'type': 'trauma_screening'
            }
        
        # Sentiment-based responses with trauma-informed approach
        if sentiment == 'severe_distress':
            return {
                'reply': 'I can hear how much pain you\'re in right now. That level of distress is overwhelming, and you don\'t have to face it alone. Your feelings are valid, and healing is possible, even when it doesn\'t feel that way.',
                'sentiment': sentiment,
                'suggestions': ['Contact RAINN: 1-800-656-HOPE', 'Reach out to a trusted person', 'Consider crisis support']
            }
        
        elif sentiment == 'distressed':
            return {
                'reply': 'I can sense you\'re struggling right now. Trauma can make everything feel more difficult, and that\'s understandable. You\'ve already shown so much strength. What would feel most supportive right now?',
                'sentiment': sentiment,
                'suggestions': ['Practice self-compassion', 'Use grounding techniques', 'Connect with support']
            }
        
        elif sentiment == 'positive':
            return {
                'reply': 'I\'m glad to hear some hope or positivity in your words. Healing isn\'t linear, and these moments of light are important to acknowledge. You\'re doing important work in your recovery.',
                'sentiment': sentiment,
                'suggestions': ['Celebrate small victories', 'Build on positive moments', 'Continue self-care practices']
            }
        
        else:
            return {
                'reply': 'I\'m here to listen and support you. Trauma recovery takes time, and every step forward matters, no matter how small. What\'s on your mind today?',
                'sentiment': sentiment,
                'suggestions': ['Take things at your own pace', 'Practice self-care', 'Remember you\'re not alone']
            }

def generate_trauma_report(data, filename="trauma_support_report.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename)
    story = []

    story.append(Paragraph("<b>SAFE AI - Trauma Support Report</b>", styles["Title"]))
    story.append(Paragraph(f"Risk Level: <b>{data['risk']}</b>", styles["Normal"]))
    story.append(Paragraph(f"Trauma Indicators: <b>{data.get('trauma_indicators', 0)}</b>", styles["Normal"]))
    
    story.append(Paragraph("<b>Specialized Resources:</b>", styles["Heading2"]))
    resources = [
        "RAINN National Sexual Assault Hotline: 1-800-656-HOPE (4673)",
        "Crisis Text Line: Text HOME to 741741",
        "National Suicide Prevention Lifeline: 988",
        "National Domestic Violence Hotline: 1-800-799-7233"
    ]
    
    for resource in resources:
        story.append(Paragraph(f"• {resource}", styles["Normal"]))
    
    story.append(Paragraph(
        "<i>This SAFE AI report provides trauma-informed support resources and is not a medical diagnosis. "
        "Professional trauma therapy is recommended for comprehensive care.</i>",
        styles["Italic"]
    ))

    doc.build(story)
    return filename

# Initialize trauma-informed chatbot
trauma_chatbot = TraumaInformedChatbot()

def trauma_chat_response(message):
    return trauma_chatbot.get_response(message)