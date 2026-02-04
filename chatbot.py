import json
from textblob import TextBlob
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, filename="support_report.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename)
    story = []

    story.append(Paragraph("<b>Mental Health Support Report</b>", styles["Title"]))
    story.append(Paragraph(f"Risk Level: <b>{data['risk']}</b>", styles["Normal"]))
    story.append(Paragraph(
        "This report is supportive and not a medical diagnosis.",
        styles["Italic"]
    ))

    doc.build(story)
    return filename

class SentimentChatbot:
    def __init__(self):
        self.crisis_keywords = ['suicide', 'kill myself', 'hurt myself', 'want to die', 'end my life']
        self.conversation_history = []
        self.health_factors = {
            'sleep_hours': None,
            'mental_health_history': None,
            'blood_sugar_issues': None,
            'recent_events': None
        }
        self.recent_event_triggers = ['stressed', 'overwhelmed', 'difficult', 'hard time', 'struggling', 'upset', 'worried', 'anxious']
        self.assessment_questions = [
            "How many hours of sleep did you get last night?",
            "Do you have any history of mental health conditions?",
            "Have you experienced any blood sugar issues or diabetes?",
            "Have there been any significant changes or stressful events in your life recently?"
        ]
        self.current_question = 0
    
    def analyze_sentiment(self, message):
        blob = TextBlob(message)
        sentiment = blob.sentiment
        
        if sentiment.polarity < -0.5:
            return 'very_negative'
        elif sentiment.polarity < -0.1:
            return 'negative'
        elif sentiment.polarity > 0.1:
            return 'positive'
        else:
            return 'neutral'
    
    def check_health_factors(self, message):
        message_lower = message.lower()
        
        # Check for recent events/stressors
        if any(trigger in message_lower for trigger in self.recent_event_triggers):
            if self.health_factors['recent_events'] is None:
                return "It sounds like you're going through something challenging. Can you tell me about any recent changes or stressful events in your life? This could include work, relationships, family, health, or financial situations."
        
        # Check for sleep patterns
        if any(word in message_lower for word in ['sleep', 'tired', 'exhausted', 'insomnia']):
            if self.health_factors['sleep_hours'] is None:
                return "I notice you mentioned sleep. How many hours of sleep do you typically get per night?"
        
        # Check for mental health history
        if any(word in message_lower for word in ['depression', 'anxiety', 'therapy', 'medication', 'psychiatrist']):
            if self.health_factors['mental_health_history'] is None:
                return "It sounds like you may have experience with mental health support. Do you have any diagnosed mental health conditions?"
        
        # Check for blood sugar/diabetes
        if any(word in message_lower for word in ['sugar', 'diabetes', 'glucose', 'dizzy', 'shaky']):
            if self.health_factors['blood_sugar_issues'] is None:
                return "I'm wondering about your physical health. Do you have any issues with blood sugar or diabetes?"
        
        return None
    
    def get_response(self, message):
        sentiment = self.analyze_sentiment(message)
        self.conversation_history.append({'message': message, 'sentiment': sentiment})
        
        # Check for health factor questions
        health_question = self.check_health_factors(message)
        if health_question:
            return {
                'reply': health_question,
                'sentiment': 'assessment',
                'type': 'health_screening'
            }
        
        # Crisis detection
        message_lower = message.lower()
        if any(keyword in message_lower for keyword in self.crisis_keywords):
            return {
                'reply': 'I\'m very concerned about you. Please reach out for immediate help.',
                'sentiment': 'crisis',
                'emergency': True
            }
        
        # Sentiment-based responses
        if sentiment == 'very_negative':
            return {
                'reply': 'I can sense you\'re going through a really difficult time. Your pain is real and valid. Would you like to talk about what\'s weighing on you most right now?',
                'sentiment': sentiment,
                'suggestions': ['Deep breathing exercises', 'Call a trusted friend', 'Consider professional support']
            }
        
        elif sentiment == 'negative':
            return {
                'reply': 'I hear that things are tough for you right now. It takes strength to reach out. What\'s been the hardest part of your day?',
                'sentiment': sentiment,
                'suggestions': ['Take a short walk', 'Practice mindfulness', 'Journal your thoughts']
            }
        
        elif sentiment == 'positive':
            return {
                'reply': 'I\'m glad to hear some positivity in your message! It\'s wonderful when we can find moments of light. What\'s been going well for you?',
                'sentiment': sentiment,
                'suggestions': ['Keep doing what\'s working', 'Share your positivity', 'Build on this momentum']
            }
        
        else:
            return {
                'reply': 'Thank you for sharing with me. I\'m here to listen and support you. What would be most helpful right now?',
                'sentiment': sentiment,
                'suggestions': ['Take things one step at a time', 'Focus on self-care', 'Reach out when you need support']
            }

chatbot = SentimentChatbot()

def chat_response(message):
    return chatbot.get_response(message)