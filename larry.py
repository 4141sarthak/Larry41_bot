import os
import smtplib
import ssl
from email.message import EmailMessage
from telegram import Update
from telegail.comram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Configuration (using environment variables for security) ---
# SENDER_EMAIL: The email address that will send the messages.
# SENDER_PASSWORD: The App Password for the sender email (REQUIRED for Gmail).
# RECEIVER_EMAIL: The email address where the messages will be forwarded.
SENDER_EMAIL = os.getenv("larry41bot@gmail.com")
RECEIVER_EMAIL = os.getenv("4141sarthak@gmail.com")
SENDER_PASSWORD = os.getenv("Larry@123")
SMTP_SERVER = "smtp.gmail.com"
PORT = 465  # Default port for SSL

# --- Function to send an email ---
def send_email(subject: str, body: str):
    """
    Sends an email with the specified subject and body using the configured credentials.
    """
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        print("Error: Email credentials are not fully configured in the environment variables.")
        return

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print(f"Email sent successfully with subject: '{subject}'")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")

# --- Telegram message handler ---
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function is triggered every time your bot receives a new message.
    It extracts the message content and sender info, then forwards it via email.
    """
    # Get the user's message text
    user_message = update.message.text
    
    # Get sender information for the email subject
    sender_info = "Unknown User"
    if update.message.from_user.username:
        sender_info = f"@{update.message.from_user.username}"
    elif update.message.from_user.full_name:
        sender_info = update.message.from_user.full_name
        
    # Prepare the email subject and body
    email_subject = f"New Telegram Message from {sender_info}"
    email_body = f"Message from {sender_info}:\n\n{user_message}"

    # Send the email
    send_email(email_subject, email_body)
    
    # Send a confirmation message back to the user on Telegram
    await update.message.reply_text("Message received and forwarded to the manager. Thank you!")

# --- Main function to run the bot ---
def main():
    """
    Initializes and starts the Telegram bot.
    """
    # Get the Telegram bot token from environment variables
    bot_token = os.getenv("8330439933:AAHzca72g_pvaHBZEuhsivp2wkxM2Tg3AWU")
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN is not set. Please set the environment variable.")
        return
    
    # Create the bot Application
    application = Application.builder().token(bot_token).build()

    # Create a message handler for all text messages (excluding commands)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), forward_message)

    # Add the handler to the application
    application.add_handler(message_handler)

    # Start the bot. This will keep the script running and listening for messages.
    print("Bot is running... Awaiting messages.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
