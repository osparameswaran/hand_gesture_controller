class Config:
    # Gesture detection settings
    CONFIDENCE_THRESHOLD = 0.7
    GESTURE_COOLDOWN = 1.5  # seconds
    
    # Media control settings
    VOLUME_STEP = 1 # dB
    VOLUME_COOLDOWN = 0.1  # seconds
    
    # UI settings
    SHOW_HELP = True
    SHOW_STATS = True
    SHOW_HISTORY = True
    HISTORY_LENGTH = 1
    WINDOW_WIDTH = 950
    WINDOW_HEIGHT = 500
    
    # Camera settings
    CAMERA_INDEX = 0
    FLIP_CAMERA = True
    
    @classmethod
    def update_from_dict(cls, config_dict):
        """Update configuration from dictionary"""
        for key, value in config_dict.items():
            if hasattr(cls, key):
                setattr(cls, key, value)