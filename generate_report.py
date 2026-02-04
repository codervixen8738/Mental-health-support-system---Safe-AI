from chatbot import chatbot, generate_pdf

# Simulate some conversation data
test_messages = [
    "I'm feeling really sad today",
    "studies are going well", 
    "I don't know how I feel"
]

# Process messages to build history
for msg in test_messages:
    chatbot.get_response(msg)

# Analyze conversation history for risk assessment
sentiments = [entry['sentiment'] for entry in chatbot.conversation_history]
risk_level = "Low"

if 'crisis' in sentiments:
    risk_level = "Critical"
elif 'very_negative' in sentiments:
    risk_level = "High"
elif 'negative' in sentiments:
    risk_level = "Medium"

# Generate report
report_data = {'risk': risk_level}
filename = generate_pdf(report_data)
print(f"Report generated: {filename}")