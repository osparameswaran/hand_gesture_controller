import cv2
import numpy as np
from datetime import datetime, timedelta

class UIManager:
    def __init__(self, window_name="Gesture Controller"):
        self.window_name = window_name
        self.control_history = []
        self.max_history = 2
        self.performance_stats = {
            "gestures_detected": 0,
            "commands_executed": 0,
            "start_time": datetime.now()
        }
    
    def draw_control_panel(self, image, current_gesture, confidence, volume_level):
        """Draw control panel on the image"""
        height, width = image.shape[:2]
        
        # Create semi-transparent overlay
        overlay = image.copy()
        panel_height = 500
        
        # Draw main panel
        cv2.rectangle(overlay, (0, 0), (width, panel_height), (0, 0, 0), -1)
        image = cv2.addWeighted(overlay, 0.5, image, 0.7, 0)
        
        # Current gesture info
        if current_gesture:
            gesture_text = f"Gesture: {current_gesture} ({confidence:.0%})"
            cv2.putText(image, gesture_text, (190, 20), 
                       cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)
        
        # Volume bar
        vol_bar_width = 90
        vol_bar_height = 10
        vol_x = width - vol_bar_width - 10
        vol_y = 10
        
        # Volume background
        cv2.rectangle(image, (vol_x, vol_y), 
                     (vol_x + vol_bar_width, vol_y + vol_bar_height), 
                     (50, 50, 50), -1)
        
        # Volume level
        vol_fill = int(vol_bar_width * volume_level / 100)
        if volume_level > 0:
            cv2.rectangle(image, (vol_x, vol_y), 
                         (vol_x + vol_fill, vol_y + vol_bar_height), 
                         (225, 225, 225), -1)
        
        # Volume text
        vol_text = f"Volume: {volume_level}%"
        cv2.putText(image, vol_text, (vol_x + 10, vol_y + vol_bar_height + 12), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
        
        return image
    
    def draw_gesture_help(self, image):
        """Draw gesture help guide"""
        help_text = [
            "GESTURE GUIDE:",
            " Thumb - Volume Up",
            " Pinky - Volume Down", 
            " Index - Play/Pause",
            " Index+Middle - Next Track",
            " 3 Fingers - Previous Track",
            " Index+Pinky - Fast Forward",
            " Fist - Mute",
            " All Fingers - Space Bar",
            " Index+Thumb - Fullscreen"
        ]
        
        y_start = 20
        for i, text in enumerate(help_text):
            color = (225, 225, 225) if i == 0 else (225, 225, 225)
            cv2.putText(image, text, (20, y_start + i * 15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1)
        
        return image
    
    def draw_performance_stats(self, image):
        """Draw performance statistics"""
        current_time = datetime.now()
        uptime = current_time - self.performance_stats["start_time"]
        uptime_str = str(uptime).split('.')[0]  # Remove microseconds
        
        stats_text = [
            f"Uptime: {uptime_str}",
            f"Gestures Detected: {self.performance_stats['gestures_detected']}",
            f"Commands Executed: {self.performance_stats['commands_executed']}"
        ]
        
        height, width = image.shape[:2]
        y_start = height - 60
        
        for i, text in enumerate(stats_text):
            cv2.putText(image, text, (20, y_start + i * 15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.3, (225, 225, 225), 1)
        
        return image
    
    def add_to_history(self, command):
        """Add command to history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.control_history.insert(0, f"{timestamp}: {command}")
        if len(self.control_history) > self.max_history:
            self.control_history.pop()
    
    def draw_command_history(self, image):
        """Draw command history"""
        height, width = image.shape[:2]
        history_x = width - 100
        history_y = height -60
        
        
        
        # History title
        cv2.putText(image, "RECENT COMMANDS", (history_x, history_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.3, (225, 225, 225), 1)
        
        # History items
        for i, item in enumerate(self.control_history):
            cv2.putText(image, item, (history_x, history_y + (i + 1) * 15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.3, (200, 200, 200), 1)
        
        return image
    
    def update_display(self, image, current_gesture=None, confidence=0, volume_level=50, 
                      show_help=True, show_stats=True, show_history=True):
        """Update the complete display"""
        # Draw control panel
        image = self.draw_control_panel(image, current_gesture, confidence, volume_level)
        
        # Draw gesture help
        if show_help:
            image = self.draw_gesture_help(image)
        
        # Draw command history
        if show_history:
            image = self.draw_command_history(image)
        
        # Draw performance stats
        if show_stats:
            image = self.draw_performance_stats(image)
        
        return image
    
    def increment_counter(self, counter_name):
        """Increment performance counter"""
        if counter_name in self.performance_stats:
            self.performance_stats[counter_name] += 1