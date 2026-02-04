from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
from trauma_app import TraumaInformedApp
from risk_model import predict_risk
import os
import json

app = Flask(__name__)
CORS(app)

# Initialize SAFE AI app
safe_ai_app = TraumaInformedApp()

@app.route('/')
def index():
    with open('safe_ai_frontend.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get response from SAFE AI
        response = safe_ai_app.chat(message)
        
        return jsonify({
            'reply': response['reply'],
            'sentiment': response.get('sentiment', 'neutral'),
            'type': response.get('type', 'normal'),
            'suggestions': response.get('suggestions', []),
            'resources': response.get('resources', []),
            'emergency': response.get('emergency', False)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/risk-assessment', methods=['POST'])
def risk_assessment():
    try:
        data = request.json
        age = data.get('age')
        bmi = data.get('bmi')
        
        if not age or not bmi:
            return jsonify({'error': 'Age and BMI are required'}), 400
        
        # Get risk prediction
        risk_result = predict_risk(float(age), float(bmi))
        
        if 'error' in risk_result:
            return jsonify({'error': 'Risk model not available'}), 500
        
        return jsonify(risk_result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    try:
        if not safe_ai_app.chatbot.conversation_history:
            return jsonify({'error': 'No conversation data available'}), 400
        
        # Generate trauma support report
        result = safe_ai_app.generate_trauma_report()
        
        return jsonify({
            'message': 'Report generated successfully',
            'path': result,
            'download_url': '/api/download-report'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-report')
def download_report():
    try:
        report_path = os.path.join(os.path.dirname(__file__), "trauma_support_report.pdf")
        if os.path.exists(report_path):
            return send_from_directory(
                os.path.dirname(__file__), 
                "trauma_support_report.pdf",
                as_attachment=True,
                download_name="safe_ai_trauma_report.pdf"
            )
        else:
            return jsonify({'error': 'Report not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversation-stats')
def conversation_stats():
    try:
        history = safe_ai_app.chatbot.conversation_history
        
        if not history:
            return jsonify({
                'total_messages': 0,
                'trauma_indicators': 0,
                'crisis_indicators': 0,
                'sentiment_breakdown': {}
            })
        
        sentiments = [entry['sentiment'] for entry in history]
        trauma_indicators = sum(1 for entry in history 
                              if entry.get('trauma_indicator') is not None)
        
        sentiment_counts = {}
        for sentiment in sentiments:
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        return jsonify({
            'total_messages': len(history),
            'trauma_indicators': trauma_indicators,
            'crisis_indicators': sentiment_counts.get('crisis', 0),
            'sentiment_breakdown': sentiment_counts
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear-conversation', methods=['POST'])
def clear_conversation():
    try:
        global safe_ai_app
        safe_ai_app = TraumaInformedApp()
        return jsonify({'message': 'Conversation cleared successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting SAFE AI - Trauma Support System")
    print("Access the application at: http://localhost:5000")
    print("Mobile-friendly responsive design")
    print("Trauma-informed and confidential")
    app.run(debug=True, host='0.0.0.0', port=5000)