from datetime import datetime

def get_current_time() -> str:
    """
    Returns current system time
    
    Returns:
        The current date and time as a formatted string.
    """
    try:
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return f"Error getting time: {str(e)}"
