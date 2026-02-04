from chatbot import chat_response

# Test messages that should trigger recent events questions
test_messages = [
    "I'm feeling really stressed lately",
    "I'm overwhelmed with everything going on",
    "Having a hard time dealing with things",
    "I'm struggling with some difficult situations"
]

for message in test_messages:
    print(f"User: {message}")
    response = chat_response(message)
    print(f"Bot: {response['reply']}")
    print(f"Type: {response.get('type', 'normal')}")
    print("-" * 60)