import requests
from shared.utils import get_env_var
from shared.logger import logger

def send_slack_approval(message: str) -> str:
    """
    Sends approval request to Slack channel.
    Returns approval request ID (or simple confirmation).
    """
    token = get_env_var("SLACK_BOT_TOKEN")
    channel_id = get_env_var("SLACK_CHANNEL_ID")
    
    if not token or not channel_id:
        logger.error("Slack credentials missing. Simulation mode.")
        return "SIMULATED_SLACK_REQ_ID"

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel_id,
        "text": f"🚨 *HITL Agent Approval Required*\n\n{message}\n\nReply with 'Approve' or 'Reject'."
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        if data.get("ok"):
            ts = data.get("ts")
            logger.log_approval_request(f"Slack (TS: {ts})")
            return ts
        else:
            logger.error(f"Slack API error: {data.get('error')}")
            return "ERROR"
    except Exception as e:
        logger.error(f"Failed to send Slack message: {e}")
        return "ERROR"
