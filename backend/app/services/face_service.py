import cv2
import numpy as np
from PIL import Image
import io
import uuid
import os
from typing import Dict, List, Any, Optional
import time
from ..models.schemas import ProcessingResult, FaceLandmarks

class FaceService:
    def __init__(self):
        """Initialize face detection and processing services"""
        # Load OpenCV's pre-trained face detection model
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Create uploads directory if it doesn't exist
        self.uploads_dir = "uploads"
        self.results_dir = "results"
        os.makedirs(self.uploads_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)

    async def process_upload(self, file) -> Dict[str, Any]:
        """Process uploaded image and extract face information"""
        start_time = time.time()
        
        try:
            # Read image from uploaded file
            image_data = await file.read()
            image = Image.open(io.BytesIO(image_data))
            
            # Convert PIL image to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Generate unique image ID
            image_id = str(uuid.uuid4())
            
            # Save original image
            image_path = os.path.join(self.uploads_dir, f"{image_id}.jpg")
            image.save(image_path)
            
            # Detect face and extract landmarks
            face_detected, landmarks, confidence = self._detect_face_and_landmarks(cv_image)
            
            processing_time = time.time() - start_time
            
            return {
                "image_id": image_id,
                "face_detected": face_detected,
                "landmarks": landmarks,
                "confidence": confidence,
                "processing_time": processing_time
            }
            
        except Exception as e:
            raise Exception(f"Error processing upload: {str(e)}")

    def _detect_face_and_landmarks(self, image) -> tuple[bool, Optional[List[Dict]], float]:
        """Detect face and extract landmarks using OpenCV"""
        try:
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(30, 30)
            )
            
            if len(faces) == 0:
                return False, None, 0.0
            
            # Get the first detected face
            (x, y, w, h) = faces[0]
            confidence = 0.8  # OpenCV doesn't provide confidence, so we estimate
            
            # Extract basic landmarks (simplified version)
            landmarks = self._extract_basic_landmarks(x, y, w, h, image.shape)
            
            return True, landmarks, confidence
            
        except Exception as e:
            print(f"Error in face detection: {str(e)}")
            return False, None, 0.0

    def _extract_basic_landmarks(self, x, y, w, h, image_shape) -> List[Dict[str, Any]]:
        """Extract basic facial landmarks from detected face rectangle"""
        height, width = image_shape[:2]
        
        # Calculate basic face points
        center_x = x + w // 2
        center_y = y + h // 2
        
        landmarks = [
            {
                "name": "nose",
                "x": center_x,
                "y": center_y,
                "z": 0.0,
                "visibility": 1.0
            },
            {
                "name": "left_eye",
                "x": center_x - w // 4,
                "y": center_y - h // 4,
                "z": 0.0,
                "visibility": 1.0
            },
            {
                "name": "right_eye",
                "x": center_x + w // 4,
                "y": center_y - h // 4,
                "z": 0.0,
                "visibility": 1.0
            },
            {
                "name": "left_ear",
                "x": x,
                "y": center_y,
                "z": 0.0,
                "visibility": 1.0
            },
            {
                "name": "right_ear",
                "x": x + w,
                "y": center_y,
                "z": 0.0,
                "visibility": 1.0
            },
            {
                "name": "mouth",
                "x": center_x,
                "y": center_y + h // 3,
                "z": 0.0,
                "visibility": 1.0
            },
            {
                "name": "chin",
                "x": center_x,
                "y": y + h,
                "z": 0.0,
                "visibility": 1.0
            }
        ]
        
        return landmarks

    async def swap_face(self, image_id: str, profession: str, angle: str = "front") -> Dict[str, Any]:
        """Perform face swapping with selected profession template"""
        try:
            # Load original image
            original_path = os.path.join(self.uploads_dir, f"{image_id}.jpg")
            if not os.path.exists(original_path):
                raise Exception("Original image not found")
            
            original_image = cv2.imread(original_path)
            
            # Load template image (placeholder - in real implementation, load from template service)
            template_image = self._load_template(profession, angle)
            
            # Perform face swapping
            result_image = self._perform_face_swap(original_image, template_image)
            
            # Save result
            result_id = str(uuid.uuid4())
            result_path = os.path.join(self.results_dir, f"{result_id}.jpg")
            cv2.imwrite(result_path, result_image)
            
            return {
                "result_url": f"/results/{result_id}.jpg",
                "result_id": result_id,
                "profession": profession,
                "angle": angle
            }
            
        except Exception as e:
            raise Exception(f"Error in face swapping: {str(e)}")

    def _load_template(self, profession: str, angle: str):
        """Load template image for given profession and angle"""
        # Placeholder implementation - in real app, load from template directory
        # For now, create a simple colored background
        template = np.ones((512, 512, 3), dtype=np.uint8) * 128
        
        # Add some visual indication of profession
        cv2.putText(template, f"{profession.title()}", (50, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        cv2.putText(template, f"Angle: {angle}", (50, 200), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        return template

    def _perform_face_swap(self, source_image, target_image):
        """Perform face swapping between source and target images"""
        # This is a simplified implementation
        # In a real application, you would use more sophisticated techniques:
        # 1. Face alignment using landmarks
        # 2. Seamless cloning
        # 3. Color correction
        # 4. Edge blending
        
        # For MVP, we'll do a simple overlay
        # Resize source to match target
        target_height, target_width = target_image.shape[:2]
        source_resized = cv2.resize(source_image, (target_width, target_height))
        
        # Simple alpha blending (50% source, 50% target)
        result = cv2.addWeighted(source_resized, 0.5, target_image, 0.5, 0)
        
        return result

    def get_face_angle(self, landmarks: List[Dict[str, Any]]) -> str:
        """Determine the face angle from landmarks"""
        if not landmarks:
            return "unknown"
        
        # Simple angle detection based on eye positions
        left_eye = None
        right_eye = None
        
        for landmark in landmarks:
            if landmark["name"] == "left_eye":
                left_eye = landmark
            elif landmark["name"] == "right_eye":
                right_eye = landmark
        
        if left_eye and right_eye:
            # Calculate eye distance and position
            eye_distance = abs(right_eye["x"] - left_eye["x"])
            eye_center_x = (left_eye["x"] + right_eye["x"]) / 2
            
            # Simple heuristics for angle detection
            if eye_distance < 50:  # Eyes very close - likely side view
                return "side"
            elif eye_distance > 100:  # Eyes far apart - likely front view
                return "front"
            else:
                return "three_quarter"
        
        return "unknown" 