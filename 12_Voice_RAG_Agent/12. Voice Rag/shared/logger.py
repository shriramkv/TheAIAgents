import logging
import sys

def setup_logger(name: str = "VoiceRAGAgent") -> logging.Logger:
    """
    Setup a custom logger with a specific format.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        # Using a simple format as requested in the logging format requirement
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Buffer for UI
        class ListHandler(logging.Handler):
            def __init__(self):
                super().__init__()
                self.logs = []
            def emit(self, record):
                self.logs.append(self.format(record))
        
        ui_handler = ListHandler()
        ui_handler.setFormatter(formatter)
        logger.addHandler(ui_handler)
        logger.ui_handler = ui_handler # Attach specifically

    return logger

# Single instance for the application
logger = setup_logger()

def log_audio_received():
    logger.info("[AUDIO INPUT RECEIVED]")

def log_transcript(transcript: str):
    logger.info(f"[TRANSCRIPT] {transcript}")

def log_retrieved_context(context: str):
    logger.info(f"[RETRIEVED CONTEXT] {context[:100]}...") # Log partial for brevity

def log_answer_generated():
    logger.info("[ANSWER GENERATED]")

def log_audio_response_created():
    logger.info("[AUDIO RESPONSE CREATED]")

def get_ui_logs():
    if hasattr(logger, "ui_handler"):
        return "\n".join(logger.ui_handler.logs)
    return ""

def clear_ui_logs():
    if hasattr(logger, "ui_handler"):
        logger.ui_handler.logs = []
