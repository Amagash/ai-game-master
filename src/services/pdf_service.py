import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class PDFService:
    @staticmethod
    def create_chat_pdf(messages):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        
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