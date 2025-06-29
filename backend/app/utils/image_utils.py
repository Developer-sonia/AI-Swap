import cv2
import numpy as np
from PIL import Image
import io
from typing import Tuple, Optional, List
import os

class ImageUtils:
    """Utility class for image processing operations"""
    
    @staticmethod
    def validate_image(file_content: bytes, max_size: int = 10 * 1024 * 1024) -> Tuple[bool, str]:
        """Validate uploaded image file"""
        try:
            # Check file size
            if len(file_content) > max_size:
                return False, f"File size exceeds {max_size // (1024*1024)}MB limit"
            
            # Try to open image
            image = Image.open(io.BytesIO(file_content))
            
            # Check image format
            if image.format not in ['JPEG', 'JPG', 'PNG', 'WEBP']:
                return False, "Unsupported image format. Use JPEG, PNG, or WebP"
            
            # Check image dimensions
            width, height = image.size
            if width < 256 or height < 256:
                return False, "Image too small. Minimum size is 256x256 pixels"
            
            if width > 4096 or height > 4096:
                return False, "Image too large. Maximum size is 4096x4096 pixels"
            
            return True, "Image validation passed"
            
        except Exception as e:
            return False, f"Image validation failed: {str(e)}"
    
    @staticmethod
    def resize_image(image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
        """Resize image to target size while maintaining aspect ratio"""
        height, width = image.shape[:2]
        target_width, target_height = target_size
        
        # Calculate aspect ratios
        aspect_ratio = width / height
        target_aspect_ratio = target_width / target_height
        
        if aspect_ratio > target_aspect_ratio:
            # Image is wider than target
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            # Image is taller than target
            new_height = target_height
            new_width = int(target_height * aspect_ratio)
        
        # Resize image
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
        
        # Create canvas with target size
        canvas = np.zeros((target_height, target_width, 3), dtype=np.uint8)
        
        # Calculate position to center the image
        y_offset = (target_height - new_height) // 2
        x_offset = (target_width - new_width) // 2
        
        # Place resized image on canvas
        canvas[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = resized
        
        return canvas
    
    @staticmethod
    def enhance_image(image: np.ndarray) -> np.ndarray:
        """Apply basic image enhancement"""
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        lab[:,:,0] = clahe.apply(lab[:,:,0])
        
        # Convert back to BGR
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Apply slight sharpening
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        
        return sharpened
    
    @staticmethod
    def create_face_mask(landmarks: List[dict], image_shape: Tuple[int, int]) -> np.ndarray:
        """Create a mask for the face region based on landmarks"""
        height, width = image_shape[:2]
        mask = np.zeros((height, width), dtype=np.uint8)
        
        if not landmarks:
            return mask
        
        # Extract face boundary points
        face_points = []
        for landmark in landmarks:
            x, y = int(landmark['x']), int(landmark['y'])
            face_points.append([x, y])
        
        if len(face_points) < 3:
            return mask
        
        # Create convex hull for face region
        face_points = np.array(face_points, dtype=np.int32)
        hull = cv2.convexHull(face_points)
        
        # Fill the face region
        cv2.fillPoly(mask, [hull], 255)
        
        # Apply Gaussian blur for smooth edges
        mask = cv2.GaussianBlur(mask, (15, 15), 0)
        
        return mask
    
    @staticmethod
    def blend_images(source: np.ndarray, target: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """Blend source image into target image using mask"""
        # Normalize mask to 0-1 range
        mask_norm = mask.astype(np.float32) / 255.0
        mask_norm = np.stack([mask_norm] * 3, axis=2)
        
        # Ensure images have same size
        if source.shape != target.shape:
            source = cv2.resize(source, (target.shape[1], target.shape[0]))
        
        # Blend images
        blended = source * mask_norm + target * (1 - mask_norm)
        
        return blended.astype(np.uint8)
    
    @staticmethod
    def save_image(image: np.ndarray, filepath: str, quality: int = 95) -> bool:
        """Save image to file with specified quality"""
        try:
            # Convert BGR to RGB for PIL
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_image)
            
            # Save with quality setting
            pil_image.save(filepath, quality=quality, optimize=True)
            return True
            
        except Exception as e:
            print(f"Error saving image: {str(e)}")
            return False
    
    @staticmethod
    def load_image(filepath: str) -> Optional[np.ndarray]:
        """Load image from file"""
        try:
            if not os.path.exists(filepath):
                return None
            
            image = cv2.imread(filepath)
            if image is None:
                return None
            
            return image
            
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            return None 