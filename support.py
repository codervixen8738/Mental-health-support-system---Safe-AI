import streamlit as st
from chatbot import chat_response, generate_pdf

st.title('🧠 SAFE-MIND AI Support')

# Chat interface
st.header('💬 Chat Support')
if 'messages' not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

if prompt := st.chat_input('How are you feeling?'):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    response = chat_response(prompt)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
    st.rerun()

# Risk check
st.header('📊 Risk Check')
age = st.slider('Age', 18, 80, 25)
imc = st.slider('BMI', 15.0, 40.0, 22.5)

if st.button('Check Risk'):
    risk = 'Medium Risk' if imc < 18.5 or imc > 30 else 'Low Risk'
    st.success(f'Risk: {risk}')
    
    # Generate PDF report
    if st.button('📄 Generate Report'):
        filename = generate_pdf({'risk': risk})
        st.success(f'Report saved as {filename}')
        with open(filename, 'rb') as f:
            st.download_button('Download Report', f.read(), filename, 'application/pdf')

st.error('🆘 Crisis: Call 988 or 911')