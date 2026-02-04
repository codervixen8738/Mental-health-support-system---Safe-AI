from chatbot import chat_response

# Test messages that should trigger health screening questions
test_messages = [
    "I'm feeling tired all the time",
    "I have anxiety and take medication", 
    "I feel dizzy and shaky sometimes",
    "I can't sleep well at night"
]

for message in test_messages:
    print(f"User: {message}")
    response = chat_response(message)
    print(f"Bot: {response['reply']}")
    print(f"Type: {response.get('type', 'normal')}")
    print("-" * 50)