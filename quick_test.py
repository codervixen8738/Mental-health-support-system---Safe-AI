from chatbot import chat_response

# Test the specific message that was causing issues
message = "studies are going well"
response = chat_response(message)
print(f"User: {message}")
print(f"Bot: {response['reply']}")
print(f"Sentiment: {response['sentiment']}")
if 'suggestions' in response:
    print(f"Suggestions: {response['suggestions']}")