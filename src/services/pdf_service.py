import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class PDFService:
    """
    Service for creating PDF documents from game data.
    
    This class provides static methods to convert chat history into
    formatted PDF documents.
    """
    
    @staticmethod
    def create_chat_pdf(messages):
        """
        Create a PDF document from chat messages.
        
        Args:
            messages (list): List of message dictionaries containing the chat history
            
        Returns:
            io.BytesIO: PDF document as a BytesIO buffer
            
        The PDF will format user and assistant messages differently,
        with user messages in blue and assistant messages in green.
        """
        # Create a BytesIO buffer to receive the PDF data
        buffer = io.BytesIO()
        
        # Create the PDF document with letter size pages
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        # Get the default styles and add custom styles for user and assistant messages
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
        
        # Build the PDF content
        story = []
        for message in messages:
            style = 'User' if message["role"] == "user" else 'Assistant'
            text = f"{message['role'].title()}: {message['content']}"
            story.append(Paragraph(text, styles[style]))
            story.append(Spacer(1, 12))
        
        # Build the PDF and reset the buffer position
        doc.build(story)
        buffer.seek(0)
        
        return buffer 