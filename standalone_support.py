import streamlit as st

st.title('🧠 SAFE-MIND AI Support')

# Simple chatbot responses
def get_response(message):
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['low', 'sad', 'depressed', 'down']):
        return "I hear that you're feeling low. That takes courage to share. Remember that these feelings are temporary and you're not alone. Have you been able to talk to someone you trust about how you're feeling?"
    
    if any(word in message_lower for word in ['anxious', 'worried', 'scared']):
        return "Anxiety can feel overwhelming. Try this: Take a slow breath in for 4 counts, hold for 4, then breathe out for 6. You're safe right now."
    
    if any(word in message_lower for word in ['help', 'support']):
        return "I'm here to support you. What's been on your mind lately? Sometimes talking through things can help."
    
    return "Thank you for sharing with me. Your feelings are valid and important. What would be most helpful for you right now?"

# Chat interface
st.header('💬 Talk to SAFE-MIND AI')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

if prompt := st.chat_input('How are you feeling?'):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    
    response = get_response(prompt)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
    
    st.rerun()

# Risk assessment
st.header('📊 Quick Risk Check')
age = st.slider('Age', 18, 80, 25)
imc = st.slider('BMI', 15.0, 40.0, 22.5)

if st.button('Check Risk'):
    if imc < 18.5:
        risk = 'Medium Risk'
    elif imc > 30:
        risk = 'Medium Risk' 
    else:
        risk = 'Low Risk'
    st.success(f'Risk Level: {risk}')

st.error('🆘 Emergency: Call 988 (Suicide & Crisis Lifeline) or 911')