from chatbot import chat_response

# Test different types of messages
test_messages = [
    "I'm feeling really sad today",
    "I want to hurt myself",
    "Things are going great!",
    "I don't know how I feel"
]

for message in test_messages:
    print(f"User: {message}")
    response = chat_response(message)
    print(f"Bot: {response['reply']}")
    print(f"Sentiment: {response['sentiment']}")
    if 'suggestions' in response:
        print(f"Suggestions: {response['suggestions']}")
    print("-" * 50)