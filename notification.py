import os
from twilio.rest import Client
from logger import setup_logger
from dotenv import load_dotenv

load_dotenv()

logger = setup_logger("notification_service")

class WhatsAppSender:
    def __init__(self):
        #Ideally these should be environment variables
        self.sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_FROM_NUMBER") # Format: 'whatsapp:+14155238886'
        self.to_number = os.getenv("MY_PHONE_NUMBER")      # Format: 'whatsapp:+1234567890'
        
        if not all([self.sid, self.token, self.from_number, self.to_number]):
            logger.warning("Twilio credentials not fully set in environment variables.")
        
        try:
            self.client = Client(self.sid, self.token)
        except Exception as e:
            logger.exception("Failed to initialize Twilio Client")
            self.client = None

    def send_message(self, message_body):
        """
        Sends a WhatsApp message to the configured number.
        """
        if not self.client:
            logger.error("Twilio client is not initialized. Cannot send message.")
            return

        try:
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=self.to_number
            )
            logger.info(f"Message sent successfully! SID: {message.sid}")
            return message.sid
        except Exception as e:
            logger.exception("Failed to send WhatsApp message")

if __name__ == "__main__":
    # Test the sender
    sender = WhatsAppSender()
    sender.send_message("Hello! This is a test message from your Meal Planner Agent.")
