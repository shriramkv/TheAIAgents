import smtplib
from email.mime.text import MIMEText
from shared.utils import get_env_var
from shared.logger import logger

def send_email_approval(message: str) -> str:
    """
    Sends approval email.
    """
    smtp_server = get_env_var("SMTP_SERVER")
    smtp_port = int(get_env_var("SMTP_PORT", 587))
    username = get_env_var("SMTP_USERNAME")
    password = get_env_var("SMTP_PASSWORD")
    receiver = get_env_var("EMAIL_RECEIVER")
    
    if not all([smtp_server, username, password, receiver]):
        logger.error("Email credentials missing. Simulation mode.")
        return "SIMULATED_EMAIL_ID"

    msg = MIMEText(f"Agent Approval Required:\n\n{message}")
    msg['Subject'] = '🚨 HITL Agent Approval Needed'
    msg['From'] = username
    msg['To'] = receiver

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            logger.log_approval_request("Email")
            return "EMAIL_SENT"
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return "ERROR"
助力助
