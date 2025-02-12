import streamlit as st
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from config import S3_CONFIG

def create_pdf(messages):
    """Create a PDF from chat messages"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles for user and assistant messages
    styles.add(ParagraphStyle(
        name='User',
        parent=styles['Normal'],
        textColor=colors.blue,
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name='Assistant',
        parent=styles['Normal'],
        textColor=colors.green,
        spaceAfter=12
    ))
    
    story = []
    for message in messages:
        style = 'User' if message["role"] == "user" else 'Assistant'
        text = f"{message['role'].title()}: {message['content']}"
        story.append(Paragraph(text, styles[style]))
        story.append(Spacer(1, 12))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def save_game():
    """Save the chat history to S3 as a PDF, replacing any previous save"""
    if not st.session_state.messages:
        st.warning("No conversation to save!")
        return
    
    try:
        # Create PDF
        pdf_buffer = create_pdf(st.session_state.messages)
        
        # Use a consistent filename for each player
        filename = f"game_session_{st.session_state.name}.pdf"
        
        # Upload to S3, overwriting any existing file
        st.session_state.s3_client.upload_fileobj(
            pdf_buffer,
            S3_CONFIG['bucket_name'],
            filename,
            ExtraArgs={'ContentType': 'application/pdf'}
        )
        
        st.success(f"Game saved successfully as {filename}!")
    except Exception as e:
        st.error(f"Error saving game: {str(e)}") 