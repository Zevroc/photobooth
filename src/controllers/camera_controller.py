"""Camera controller for managing camera devices and capture."""
import cv2
import numpy as np
from typing import Optional, List, Tuple
from src.models.photo import Photo
from datetime import datetime


class CameraController:
    """Manages camera operations."""
    
    def __init__(self, device_id: int = 0, resolution: Tuple[int, int] = (1920, 1080)):
        """Initialize camera controller.
        
        Args:
            device_id: Camera device ID
            resolution: Tuple of (width, height)
        """
        self.device_id = device_id
        self.resolution = resolution
        self.camera: Optional[cv2.VideoCapture] = None
        self.is_active = False
    
    def start(self) -> bool:
        """Start the camera.
        
        Returns:
            True if camera started successfully, False otherwise
        """
        try:
            self.camera = cv2.VideoCapture(self.device_id)
            if not self.camera.isOpened():
                return False
            
            # Set resolution
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            
            self.is_active = True
            return True
        except Exception as e:
            print(f"Error starting camera: {e}")
            return False
    
    def stop(self) -> None:
        """Stop the camera."""
        if self.camera:
            self.camera.release()
            self.is_active = False
    
    def get_frame(self) -> Optional[np.ndarray]:
        """Get current frame from camera.
        
        Returns:
            Frame as numpy array or None if failed
        """
        if not self.is_active or not self.camera:
            return None
        
        ret, frame = self.camera.read()
        if ret:
            # Convert BGR to RGB
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None
    
    def capture_photo(self, frame_path: Optional[str] = None) -> Optional[Photo]:
        """Capture a photo from the camera.
        
        Args:
            frame_path: Optional path to a frame image to overlay
            
        Returns:
            Photo object or None if capture failed
        """
        frame = self.get_frame()
        if frame is None:
            return None
        
        photo = Photo(
            image_data=frame,
            timestamp=datetime.now(),
            frame_path=frame_path
        )
        
        return photo
    
    @staticmethod
    def list_available_cameras() -> List[Tuple[int, str]]:
        """List all available cameras.
        
        Returns:
            List of tuples (device_id, device_name)
        """
        cameras = []
        for i in range(10):  # Check first 10 indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append((i, f"Camera {i}"))
                cap.release()
        return cameras
    
    def __del__(self):
        """Cleanup on deletion."""
        self.stop()
