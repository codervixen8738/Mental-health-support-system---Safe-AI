from trauma_app import TraumaInformedApp

# Test SAFE AI system
app = TraumaInformedApp()

print("SAFE AI - Testing Trauma Support System")
print("=" * 50)

# Test trauma-informed responses
test_messages = [
    "I was assaulted last month",
    "I keep having nightmares",
    "I don't feel safe anymore",
    "I'm having flashbacks"
]

for message in test_messages:
    print(f"\nUser: {message}")
    response = app.chat(message)
    print(f"SAFE AI: {response['reply']}")
    
    if 'resources' in response:
        print("Resources provided:")
        for resource in response['resources']:
            print(f"  • {resource}")

print("\n" + "=" * 50)
print("SAFE AI - Specialized support for trauma survivors")
print("Report generation available for comprehensive assessment")