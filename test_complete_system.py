from app import MentalHealthApp

# Create app instance
app = MentalHealthApp()

# Simulate conversation with recent events
print("=== Conversation Simulation ===")
messages = [
    "I'm feeling really stressed lately",
    "I'm having trouble sleeping",
    "I have anxiety issues"
]

for msg in messages:
    print(f"User: {msg}")
    response = app.chat(msg)
    print(f"Bot: {response['reply']}")
    print()

# Simulate health factor responses
app.chatbot.health_factors['sleep_hours'] = 4
app.chatbot.health_factors['mental_health_history'] = 'yes'
app.chatbot.health_factors['recent_events'] = 'work stress'

print("=== Generating Enhanced Report ===")
result = app.generate_in_app_report()
print(result)