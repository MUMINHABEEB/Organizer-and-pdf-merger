# Configuration settings for the AI Automation Suite

class Config:
    """Configuration settings for the AI Automation Suite."""
    
    # General settings
    APP_NAME = "AI Automation Suite"
    VERSION = "1.0.0"
    
    # AI model settings
    AI_MODEL_PATH = "src/ai/model.pkl"
    AI_PROMPT_PATH = "src/ai/prompts/system.txt"
    
    # File handling settings
    DEFAULT_INPUT_DIR = "input/"
    DEFAULT_OUTPUT_DIR = "output/"
    
    # Logging settings
    LOGGING_LEVEL = "DEBUG"
    LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # GUI settings
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    
    # PDF settings
    PDF_TOOL_OPTIONS = {
        "compress": True,
        "merge": True,
        "split": False
    }