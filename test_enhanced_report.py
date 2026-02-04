from app import MentalHealthApp

# Create app instance
app = MentalHealthApp()

# Simulate conversation with health factors
app.chat("I'm feeling really tired and can't sleep")
app.chat("I have anxiety and take medication")
app.chat("I feel dizzy sometimes")

# Simulate health factor responses
app.chatbot.health_factors['sleep_hours'] = 4
app.chatbot.health_factors['mental_health_history'] = 'yes'
app.chatbot.health_factors['blood_sugar_issues'] = 'yes'

# Generate comprehensive report
result = app.generate_in_app_report()
print(result)