"""Email controller for sending photos."""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from typing import Optional


class EmailController:
    """Manages email sending."""
    
    def __init__(
        self,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 587,
        sender_email: str = "",
        sender_password: str = "",
        use_tls: bool = True,
        enabled: bool = False
    ):
        """Initialize email controller.
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP server port
            sender_email: Sender email address
            sender_password: Sender email password
            use_tls: Whether to use TLS
            enabled: Whether email is enabled
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.use_tls = use_tls
        self.enabled = enabled
    
    def send_photo(
        self,
        recipient_email: str,
        photo_path: str,
        subject: str = "Your Photobooth Photo",
        message: str = "Thank you for using our photobooth! Here's your photo."
    ) -> bool:
        """Send a photo via email.
        
        Args:
            recipient_email: Recipient's email address
            photo_path: Path to photo file
            subject: Email subject
            message: Email message body
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.enabled or not self.sender_email or not os.path.exists(photo_path):
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Add text
            msg.attach(MIMEText(message, 'plain'))
            
            # Add photo
            with open(photo_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(photo_path))
                msg.attach(img)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
