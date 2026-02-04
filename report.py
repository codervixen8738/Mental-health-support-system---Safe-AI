from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch




def generate_report(data, output_path):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path)
    story = []

    story.append(Paragraph("<b>Mental Health Support Report</b>", styles['Title']))
    story.append(Paragraph(f"Risk Level: <b>{data['risk_level']}</b>", styles['Normal']))
    
    # Risk Explanation Section
    story.append(Paragraph("<b>Risk Assessment Explanation:</b>", styles['Heading2']))
    risk_explanations = {
        'Critical': 'Immediate intervention required. Crisis indicators detected suggesting potential self-harm risk.',
        'High': 'Significant mental health concerns present. Professional evaluation strongly recommended.',
        'Medium': 'Moderate risk factors identified. Monitoring and support recommended.',
        'Low': 'Minimal risk indicators. Maintain current positive practices.'
    }
    story.append(Paragraph(risk_explanations.get(data['risk_level'], 'Risk level assessment unavailable.'), styles['Normal']))
    
    # Medical Assessment Factors
    story.append(Paragraph("<b>Medical Assessment Factors:</b>", styles['Heading2']))
    if 'medical_factors' in data:
        for factor, value in data['medical_factors'].items():
            impact = get_medical_impact(factor, value)
            story.append(Paragraph(f"• {factor}: {value} - {impact}", styles['Normal']))
    
    # Key Indicators
    story.append(Paragraph("<b>Key Indicators:</b>", styles['Heading2']))
    for k, v in data['indicators'].items():
        story.append(Paragraph(f"• {k}: {v}", styles['Normal']))

    # Support Recommendations
    story.append(Paragraph("<b>Support Recommendations:</b>", styles['Heading2']))
    for rec in data['recommendations']:
        story.append(Paragraph(f"• {rec}", styles['Normal']))
    
    # Clinical Notes
    story.append(Paragraph("<b>Clinical Considerations:</b>", styles['Heading2']))
    clinical_notes = get_clinical_notes(data['risk_level'], data.get('medical_factors', {}))
    for note in clinical_notes:
        story.append(Paragraph(f"• {note}", styles['Normal']))

    story.append(Paragraph("<i>This report is for support purposes only and is not a medical diagnosis.</i>", styles['Italic']))

    doc.build(story)

def get_medical_impact(factor, value):
    impacts = {
        'Sleep Hours': {
            'low': 'Sleep deprivation can significantly impact mood regulation and cognitive function.',
            'normal': 'Adequate sleep supports mental health stability.',
            'high': 'Excessive sleep may indicate depression or other underlying conditions.'
        },
        'Mental Health History': {
            'yes': 'Previous mental health conditions increase risk of recurrence.',
            'no': 'No documented history reduces baseline risk factors.'
        },
        'Blood Sugar Issues': {
            'yes': 'Blood sugar fluctuations can affect mood, anxiety, and cognitive function.',
            'no': 'Stable blood sugar supports consistent mental health.'
        },
        'Recent Life Events': {
            'work stress': 'Work-related stress can significantly impact mental health and requires coping strategies.',
            'relationship issues': 'Relationship problems are major stressors that can trigger depression and anxiety.',
            'financial problems': 'Financial stress is strongly linked to increased mental health risks.',
            'health issues': 'Physical health problems can compound mental health challenges.',
            'family problems': 'Family conflicts or changes can be significant emotional stressors.',
            'loss/grief': 'Recent loss or grief requires specialized support and monitoring.',
            'major life change': 'Significant life transitions can temporarily increase mental health vulnerability.',
            'none': 'No recent major stressors identified.',
            'not assessed': 'Recent life events not yet evaluated.'
        }
    }
    
    if factor in impacts:
        if isinstance(value, (int, float)):
            if value < 6:
                return impacts[factor].get('low', 'May impact mental health negatively.')
            elif value > 9:
                return impacts[factor].get('high', 'May indicate underlying issues.')
            else:
                return impacts[factor].get('normal', 'Within normal range.')
        else:
            return impacts[factor].get(str(value).lower(), 'Impact assessment unavailable.')
    return 'Medical significance under evaluation.'

def get_clinical_notes(risk_level, medical_factors):
    notes = []
    
    if risk_level == 'Critical':
        notes.extend([
            'Immediate psychiatric evaluation recommended',
            'Consider safety planning and crisis intervention',
            'Monitor for suicidal ideation or self-harm behaviors'
        ])
    elif risk_level == 'High':
        notes.extend([
            'Professional mental health assessment advised within 1-2 weeks',
            'Consider medication evaluation if not currently treated',
            'Implement regular check-ins and support system activation'
        ])
    elif risk_level == 'Medium':
        notes.extend([
            'Monitor symptoms and functioning over next 2-4 weeks',
            'Consider counseling or therapy if symptoms persist',
            'Encourage healthy coping strategies and lifestyle modifications'
        ])
    
    # Add medical factor specific notes
    if medical_factors.get('Sleep Hours', 0) < 6:
        notes.append('Address sleep hygiene and consider sleep study if chronic insomnia persists')
    
    if medical_factors.get('Blood Sugar Issues') == 'yes':
        notes.append('Coordinate with primary care physician for diabetes/glucose management')
    
    # Add recent events specific notes
    recent_events = medical_factors.get('Recent Life Events', 'Not assessed')
    if recent_events != 'Not assessed' and recent_events != 'none':
        notes.append('Address recent life stressors through targeted counseling or stress management techniques')
        if 'loss' in str(recent_events).lower() or 'grief' in str(recent_events).lower():
            notes.append('Consider grief counseling or bereavement support groups')
        if 'work' in str(recent_events).lower():
            notes.append('Evaluate work-life balance and consider workplace accommodations if needed')
    
    return notes