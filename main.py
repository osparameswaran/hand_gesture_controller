from gesture_detector import EnhancedGestureDetector
import argparse

def main():
    parser = argparse.ArgumentParser(description='Gesture Media Controller')
    parser.add_argument('--camera', type=int, default=0, help='Camera index (default: 0)')
    parser.add_argument('--no-help', action='store_true', help='Hide help panel')
    parser.add_argument('--no-stats', action='store_true', help='Hide statistics')
    parser.add_argument('--confidence', type=float, default=0.7, help='Gesture confidence threshold')

    args = parser.parse_args()
    
    # Update configuration
    from config import Config
    Config.CAMERA_INDEX = args.camera
    Config.SHOW_HELP = not args.no_help
    Config.SHOW_STATS = not args.no_stats
    Config.CONFIDENCE_THRESHOLD = args.confidence
    
    
    print("\nControls:")
    print("• Press 'q' to quit")
    print("• Press 'h' to toggle help")
    print("• Press 's' to toggle statistics")
    print("• Press 'r' to reset counters")
    print("=" * 50)
    
    try:
        detector = EnhancedGestureDetector()
        detector.run()
    except KeyboardInterrupt:
        print("\n Controller stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your camera and dependencies")

if __name__ == "__main__":
    main()