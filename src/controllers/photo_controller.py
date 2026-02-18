"""Photo controller for managing photo operations."""
import os
from datetime import datetime
from typing import Optional
import cv2
import numpy as np
from PIL import Image
from src.models.photo import Photo


class PhotoController:
    """Manages photo operations like saving, applying frames, etc."""
    
    def __init__(self, photos_directory: str = "assets/photos"):
        """Initialize photo controller.
        
        Args:
            photos_directory: Directory to save photos
        """
        self.photos_directory = photos_directory
        os.makedirs(photos_directory, exist_ok=True)
    
    def apply_frame(self, photo: Photo, frame_path: str) -> Photo:
        """Apply a frame overlay to a photo.
        
        Args:
            photo: Photo object
            frame_path: Path to frame image
            
        Returns:
            Photo with frame applied
        """
        if not frame_path or not os.path.exists(frame_path):
            return photo
        
        try:
            photo.image_data = self.apply_frame_to_array(photo.image_data, frame_path)
            photo.frame_path = frame_path
            photo.frame_applied = True
            
            return photo
        except Exception as e:
            print(f"Error applying frame: {e}")
            return photo

    def apply_frame_to_array(self, image_data: np.ndarray, frame_path: str) -> np.ndarray:
        """Apply a frame overlay to raw RGB image data.

        Args:
            image_data: RGB image data
            frame_path: Path to frame image

        Returns:
            RGB image with frame applied
        """
        if image_data is None or not frame_path or not os.path.exists(frame_path):
            return image_data

        # Load frame
        frame = Image.open(frame_path).convert('RGBA')

        # Convert photo to PIL Image
        photo_img = Image.fromarray(image_data).convert('RGBA')

        # Resize frame to match photo size
        frame = frame.resize(photo_img.size, Image.Resampling.LANCZOS)

        # Composite photo and frame
        combined = Image.alpha_composite(photo_img, frame)

        # Convert back to numpy array
        return np.array(combined.convert('RGB'))
    
    def save_photo(self, photo: Photo, filename: Optional[str] = None) -> str:
        """Save photo to disk.
        
        Args:
            photo: Photo object to save
            filename: Optional filename, generates one if not provided
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = photo.timestamp.strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{timestamp}.jpg"
        
        filepath = os.path.join(self.photos_directory, filename)
        
        # Convert RGB to BGR for OpenCV
        bgr_image = cv2.cvtColor(photo.image_data, cv2.COLOR_RGB2BGR)
        cv2.imwrite(filepath, bgr_image)
        
        return filepath
    
    def get_photo_thumbnail(self, photo: Photo, size: tuple = (300, 200)) -> np.ndarray:
        """Generate a thumbnail of the photo.
        
        Args:
            photo: Photo object
            size: Tuple of (width, height) for thumbnail
            
        Returns:
            Thumbnail as numpy array
        """
        img = Image.fromarray(photo.image_data)
        img.thumbnail(size, Image.Resampling.LANCZOS)
        return np.array(img)
