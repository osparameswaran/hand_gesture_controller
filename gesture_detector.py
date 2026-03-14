import cv2
import mediapipe as mp
import time
from datetime import datetime
from media_controller import EnhancedMediaController
from ui_manager import UIManager
from gestures.gesture_library import GestureLibrary
from config import Config

class EnhancedGestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.5
        )
        
        self.controller = EnhancedMediaController()
        self.ui = UIManager()
        self.gesture_lib = GestureLibrary()
        
        self.last_gesture_time = 0
        self.current_gesture = None
        self.gesture_confidence = 0
        
    def process_frame(self, image):
        """Process a single frame for gesture detection"""
        # Flip image for mirror effect
        if Config.FLIP_CAMERA:
            image = cv2.flip(image, 1)
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        gesture_detected = None
        command_executed = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
                
                # Detect gesture
                finger_states = self.gesture_lib.get_finger_states(hand_landmarks.landmark)
                gesture, confidence = self.gesture_lib.detect_gesture(
                    finger_states, Config.CONFIDENCE_THRESHOLD)
                
                if gesture:
                    self.ui.performance_stats["gestures_detected"] += 1
                    gesture_detected = gesture
                    self.current_gesture = gesture
                    self.gesture_confidence = confidence
                    
                    # Execute command with cooldown
                    current_time = time.time()
                    if current_time - self.last_gesture_time > Config.GESTURE_COOLDOWN:
                        command_executed = self.execute_gesture_command(gesture)
                        self.last_gesture_time = current_time
                        if command_executed:
                            self.ui.add_to_history(command_executed)
                            self.ui.performance_stats["commands_executed"] += 1
        
        # Update UI
        volume_level = self.controller.get_volume_percentage()
        image = self.ui.update_display(
            image, 
            current_gesture=gesture_detected,
            confidence=self.gesture_confidence,
            volume_level=volume_level,
            show_help=Config.SHOW_HELP,
            show_stats=Config.SHOW_STATS,
            show_history=Config.SHOW_HISTORY
        )
        
        return image, command_executed
    
    def execute_gesture_command(self, gesture):
        """Execute command based on detected gesture"""
        command_map = {
            "play_pause": self.controller.play_pause,
            "next_track": self.controller.next_track,
            "previous_track": self.controller.previous_track,
            "volume_up": self.controller.volume_up,
            "volume_down": self.controller.volume_down,
            "mute": self.controller.mute_unmute,
            "fast_forward": self.controller.fast_forward,
            "rewind": self.controller.rewind,
            "fullscreen": self.controller.fullscreen,
            "space": self.controller.space_bar,
        }
        
        if gesture in command_map:
            result = command_map[gesture]()
            return result
        return None
    
    
    
    def run(self):
        """Main application loop"""
        cap = cv2.VideoCapture(Config.CAMERA_INDEX)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.WINDOW_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.WINDOW_HEIGHT)
        
        print("Enhanced Hand Gesture Controller Started!")
        print("Press 'q' to quit, 'h' to toggle help, 's' to toggle stats")
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Failed to capture image")
                continue
            
            # Process frame
            image, command = self.process_frame(image)
            
            # Display result
            cv2.imshow('Gesture Controller', image)
            
            # Handle keyboard input
            key = cv2.waitKey(5) & 0xFF
            if key == ord('q') or key == ord('Q'):
                break
            elif key == ord('h') or key == ord('H'):
                Config.SHOW_HELP = not Config.SHOW_HELP
            elif key == ord('s') or key == ord('S'):
                Config.SHOW_STATS = not Config.SHOW_STATS
            elif key == ord('r') or key == ord('R'):
                self.ui.performance_stats["start_time"] = datetime.now()
                self.ui.performance_stats["gestures_detected"] = 0
                self.ui.performance_stats["commands_executed"] = 0
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = EnhancedGestureDetector()
    detector.run()