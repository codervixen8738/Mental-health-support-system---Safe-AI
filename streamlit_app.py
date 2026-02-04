import streamlit as st
import pandas as pd
from trauma_chatbot import TraumaInformedChatbot
from trauma_app import TraumaInformedApp
from risk_model import predict_risk
import os
import base64

# Page config
st.set_page_config(
    page_title="SAFE AI - Trauma Support System",
    page_icon="🛡️",
    layout="wide"
)

# Initialize session state
if 'app' not in st.session_state:
    st.session_state.app = TraumaInformedApp()
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Title and header
st.title("🛡️ SAFE AI - Trauma Support System")
st.markdown("*Specialized AI for Sexual Assault & Trauma Recovery*")
st.markdown("---")

# Sidebar for user info and risk prediction
with st.sidebar:
    st.header("📊 Risk Assessment")
    
    # User input for risk prediction
    age = st.number_input("Age", min_value=18, max_value=100, value=25)
    bmi = st.number_input("BMI", min_value=15.0, max_value=50.0, value=22.5, step=0.1)
    
    if st.button("Predict Risk"):
        try:
            risk_result = predict_risk(age, bmi)
            if 'error' not in risk_result:
                st.success(f"**Risk Level:** {risk_result['risk_level']}")
                st.info(f"**Confidence:** {risk_result['confidence']:.1%}")
                
                # Display probabilities
                st.write("**Risk Probabilities:**")
                for risk, prob in risk_result['probabilities'].items():
                    st.write(f"• {risk}: {prob:.1%}")
            else:
                st.error(f"Error: {risk_result['error']}")
        except Exception as e:
            st.error("Model files not found. Please train the model first.")
    
    st.markdown("---")
    
    # Trauma factors summary
    st.header("🛡️ Trauma Factors")
    trauma_factors = st.session_state.app.chatbot.trauma_factors
    
    for factor, value in trauma_factors.items():
        if value is not None:
            st.write(f"**{factor.replace('_', ' ').title()}:** {value}")
        else:
            st.write(f"**{factor.replace('_', ' ').title()}:** Not assessed")

# Main chat interface
st.header("💬 Chat with SAFE AI Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "type" in message and message["type"] == "trauma_screening":
            st.info("🛡️ Trauma-informed assessment question")

# Chat input
if prompt := st.chat_input("This is a safe space. Share what feels comfortable..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get bot response
    response = st.session_state.app.chat(prompt)
    
    # Add bot response
    bot_message = {
        "role": "assistant", 
        "content": response['reply']
    }
    
    if response.get('type') == 'trauma_screening':
        bot_message["type"] = "trauma_screening"
    
    st.session_state.messages.append(bot_message)
    
    # Display new messages
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        st.write(response['reply'])
        if response.get('type') == 'trauma_screening':
            st.info("🛡️ Trauma-informed assessment question")
        
        # Show suggestions if available
        if 'suggestions' in response:
            st.write("**Suggestions:**")
            for suggestion in response['suggestions']:
                st.write(f"• {suggestion}")

# Report generation section
st.markdown("---")
st.header("📋 Generate SAFE AI Report")

col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Trauma Support Report", type="primary"):
        if st.session_state.app.chatbot.conversation_history:
            try:
                result = st.session_state.app.generate_trauma_report()
                st.success("Report generated successfully!")
                st.info(result)
                
                # Provide download link
                report_path = os.path.join(os.path.dirname(__file__), "trauma_support_report.pdf")
                if os.path.exists(report_path):
                    with open(report_path, "rb") as pdf_file:
                        pdf_data = pdf_file.read()
                        b64_pdf = base64.b64encode(pdf_data).decode()
                        href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="safe_ai_trauma_report.pdf">Download SAFE AI Report</a>'
                        st.markdown(href, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
        else:
            st.warning("No conversation data available. Please chat first.")

with col2:
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.app = TraumaInformedApp()
        st.success("Conversation cleared!")
        st.rerun()

# Statistics section
if st.session_state.app.chatbot.conversation_history:
    st.markdown("---")
    st.header("📈 Conversation Statistics")
    
    history = st.session_state.app.chatbot.conversation_history
    sentiments = [entry['sentiment'] for entry in history]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Messages", len(history))
    
    with col2:
        negative_count = sum(1 for s in sentiments if s in ['negative', 'very_negative'])
        st.metric("Negative Sentiment", negative_count)
    
    with col3:
        positive_count = sum(1 for s in sentiments if s == 'positive')
        st.metric("Positive Sentiment", positive_count)
    
    with col4:
        crisis_count = sum(1 for s in sentiments if s == 'crisis')
        st.metric("Crisis Indicators", crisis_count, delta_color="inverse")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p><strong>🛡️ SAFE AI - Specialized Support for Trauma Survivors</strong></p>
        <p><em>This system provides trauma-informed support and is not a substitute for professional therapy.</em></p>
        <p>🆘 <strong>Crisis Support:</strong> If you're in immediate danger, call 911</p>
        <p>📞 <strong>RAINN:</strong> 1-800-656-HOPE (4673) | <strong>Crisis Text:</strong> HOME to 741741</p>
    </div>
    """, 
    unsafe_allow_html=True
)