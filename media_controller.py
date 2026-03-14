import pyautogui
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class EnhancedMediaController:
    def __init__(self):
        self.setup_volume_control()
        self.volume_step = 2.0  # dB per step
        self.last_volume_time = 0
        self.volume_cooldown = 0.1  # seconds
        
    def setup_volume_control(self):
        """Initialize volume control system"""
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        # Get volume range
        self.volume_range = self.volume.GetVolumeRange()
        self.min_vol = self.volume_range[0]
        self.max_vol = self.volume_range[1]
    
    def get_current_volume(self):
        """Get current volume level"""
        return self.volume.GetMasterVolumeLevel()
    
    def get_volume_percentage(self):
        """Get volume as percentage (0-100)"""
        current_vol = self.get_current_volume()
        vol_range = self.max_vol - self.min_vol
        return int(((current_vol - self.min_vol) / vol_range) * 100)
    
    def play_pause(self):
        """Play/Pause media"""
        pyautogui.press('playpause')
        return "Play/Pause"
    
    def next_track(self):
        """Next track"""
        pyautogui.press('nexttrack')
        return "Next Track"
    
    def previous_track(self):
        """Previous track"""
        pyautogui.press('prevtrack')
        return "Previous Track"
    
    def volume_up(self):
        """Increase volume"""
        current_time = time.time()
        if current_time - self.last_volume_time > self.volume_cooldown:
            current_vol = self.get_current_volume()
            new_vol = min(current_vol + self.volume_step, self.max_vol)
            self.volume.SetMasterVolumeLevel(new_vol, None)
            self.last_volume_time = current_time
            return f"Volume: {self.get_volume_percentage()}%"
        return None
    
    def volume_down(self):
        """Decrease volume"""
        current_time = time.time()
        if current_time - self.last_volume_time > self.volume_cooldown:
            current_vol = self.get_current_volume()
            new_vol = max(current_vol - self.volume_step, self.min_vol)
            self.volume.SetMasterVolumeLevel(new_vol, None)
            self.last_volume_time = current_time
            return f"Volume: {self.get_volume_percentage()}%"
        return None
    
    def mute_unmute(self):
        """Toggle mute"""
        is_muted = self.volume.GetMute()
        self.volume.SetMute(not is_muted, None)
        return "Muted" if not is_muted else "Unmuted"
    
    def fast_forward(self):
        """Fast forward - Right arrow key"""
        pyautogui.press('right')
        return "Fast Forward"
    
    def rewind(self):
        """Rewind - Left arrow key"""
        pyautogui.press('left')
        return "Rewind"
    
    def fullscreen(self):
        """Toggle fullscreen - F key"""
        pyautogui.press('f')
        return "Fullscreen Toggle"
    
    def space_bar(self):
        """Space bar action"""
        pyautogui.press('space')
        return "Space"
    
    def escape(self):
        """Escape key"""
        pyautogui.press('escape')
        return "Escape"