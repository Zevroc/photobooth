"""Photo model."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import numpy as np


@dataclass
class Photo:
    """Represents a captured photo."""
    image_data: np.ndarray  # The actual image data (with frame if applied)
    timestamp: datetime
    frame_path: Optional[str] = None
    frame_applied: bool = False
    raw_image_data: Optional[np.ndarray] = None  # Original image without frame
    width: int = 0
    height: int = 0
    
    def __post_init__(self):
        if self.image_data is not None and len(self.image_data.shape) >= 2:
            self.height, self.width = self.image_data.shape[:2]
