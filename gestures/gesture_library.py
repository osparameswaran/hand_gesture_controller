import math

class GestureLibrary:
    def __init__(self):
        self.gestures = {
            "play_pause": {"fingers": [0, 1, 0, 0, 0], "description": "Play/Pause"},
            "next_track": {"fingers": [0, 1, 1, 0, 0], "description": "Next Track"},
            "previous_track": {"fingers": [0, 1, 1, 1, 0], "description": "Previous Track"},
            "volume_up": {"fingers": [1, 0, 0, 0, 0], "description": "Volume Up"},
            "volume_down": {"fingers": [0, 0, 0, 0, 1], "description": "Volume Down"},
            "mute": {"fingers": [0, 0, 0, 0, 0], "description": "Mute/Unmute"},
            "fast_forward": {"fingers": [0, 1, 0, 0, 1], "description": "Fast Forward"},
            "rewind": {"fingers": [1, 1, 0, 0, 1], "description": "Rewind"},
            "fullscreen": {"fingers": [1, 1, 0, 0, 0], "description": "Fullscreen"},
            "space": {"fingers": [1, 1, 1, 1, 1], "description": "Space Bar"},
        }
    
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def is_finger_extended(self, landmarks, finger_tip, finger_dip, finger_pip, finger_mcp, is_thumb=False):
        """Improved finger extension detection with better accuracy"""
        tip = landmarks[finger_tip]
        dip = landmarks[finger_dip]
        pip = landmarks[finger_pip]
        mcp = landmarks[finger_mcp]
        
        if is_thumb:
            # For thumb, use different logic
            return tip.x < pip.x - 0.02
        else:
            # Check if finger is extended (tip higher than dip, and dip higher than pip)
            return tip.y < dip.y < pip.y
    
    def get_finger_states(self, landmarks):
        """Get state of all fingers with confidence"""
        finger_states = []
        
        # Thumb (4, 3, 2, 1)
        thumb_extended = self.is_finger_extended(landmarks, 4, 3, 2, 1, is_thumb=True)
        finger_states.append(1 if thumb_extended else 0)
        
        # Index (8, 7, 6, 5)
        index_extended = self.is_finger_extended(landmarks, 8, 7, 6, 5)
        finger_states.append(1 if index_extended else 0)
        
        # Middle (12, 11, 10, 9)
        middle_extended = self.is_finger_extended(landmarks, 12, 11, 10, 9)
        finger_states.append(1 if middle_extended else 0)
        
        # Ring (16, 15, 14, 13)
        ring_extended = self.is_finger_extended(landmarks, 16, 15, 14, 13)
        finger_states.append(1 if ring_extended else 0)
        
        # Pinky (20, 19, 18, 17)
        pinky_extended = self.is_finger_extended(landmarks, 20, 19, 18, 17)
        finger_states.append(1 if pinky_extended else 0)
        
        return finger_states
    
    def detect_gesture(self, finger_states, confidence_threshold=0.8):
        """Detect gesture with confidence scoring"""
        best_match = None
        best_confidence = 0
        
        for gesture_name, gesture_data in self.gestures.items():
            expected_fingers = gesture_data["fingers"]
            
            # Calculate match confidence
            matches = sum(1 for i in range(5) if finger_states[i] == expected_fingers[i])
            confidence = matches / 5.0
            
            if confidence > best_confidence and confidence >= confidence_threshold:
                best_confidence = confidence
                best_match = gesture_name
        
        return best_match, best_confidence
    
    def get_gesture_description(self, gesture_name):
        """Get description for a gesture"""
        return self.gestures.get(gesture_name, {}).get("description", "Unknown")