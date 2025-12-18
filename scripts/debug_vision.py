import cv2
import numpy as np
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    print("Importing PoseService...")
    from backend.source.vision.pose_service import PoseService
    print("PoseService imported.")
except ImportError as e:
    print(f"Failed to import PoseService: {e}")
    sys.path.append(os.path.join(os.getcwd(), 'backend', 'source', 'vision'))
    try:
        from pose_service import PoseService
        print("PoseService imported from subpath.")
    except Exception as e2:
        print(f"Failed again: {e2}")
        sys.exit(1)

def test():
    print("Initializing PoseService...")
    try:
        service = PoseService()
        print("PoseService initialized.")
    except Exception as e:
        print(f"Failed to init PoseService: {e}")
        import traceback
        traceback.print_exc()
        return

    # Create dummy frame
    print("Creating dummy frame...")
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    print("Processing frame...")
    try:
        processed = service.process_frame(frame)
        print(f"Frame processed. Shape: {processed.shape}")
    except Exception as e:
        print(f"Failed during process_frame: {e}")
        import traceback
        traceback.print_exc()
        
    print("Done.")

if __name__ == "__main__":
    test()
