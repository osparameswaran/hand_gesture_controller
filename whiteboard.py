import cv2
import numpy as np
import mediapipe as mp

class VirtualWhiteboard:
    def __init__(self):
        self.canvas = np.ones((720, 1280, 3), dtype=np.uint8) * 255  # White canvas
        self.current_color = (0, 0, 0)  # Black
        self.brush_size = 5
        self.drawing = False
        self.last_point = None
        
    def draw_on_canvas(self, current_point):
        if self.last_point and self.drawing:
            cv2.line(self.canvas, self.last_point, current_point, 
                    self.current_color, self.brush_size)
        self.last_point = current_point
    
    def process_gesture(self, finger_states, hand_position):
        thumb, index, middle, ring, pinky = finger_states
        
        if index and not any([thumb, middle, ring, pinky]):
            self.drawing = True
            self.draw_on_canvas(hand_position)
        else:
            self.drawing = False
            self.last_point = None
        
        # Change color with two fingers
        if index and middle and not any([thumb, ring, pinky]):
            self.current_color = (0, 0, 255)  # Red
        
        # Clear with open hand
        if all(finger_states):
            self.canvas = np.ones((720, 1280, 3), dtype=np.uint8) * 255