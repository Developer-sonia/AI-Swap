import os
import json
from typing import List, Dict, Any, Optional
from ..models.schemas import Template

class TemplateService:
    def __init__(self):
        """Initialize template service"""
        self.templates_dir = "templates"
        self.templates_metadata_file = "templates_metadata.json"
        
        # Create templates directory if it doesn't exist
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Initialize default templates metadata
        self._initialize_default_templates()

    def _initialize_default_templates(self):
        """Initialize default templates metadata"""
        default_templates = {
            "doctor": {
                "name": "Doctor",
                "description": "Medical professional",
                "angles": ["front", "side", "three_quarter", "back"],
                "colors": ["white", "blue"],
                "accessories": ["stethoscope", "lab_coat"]
            },
            "professor": {
                "name": "Professor",
                "description": "Academic educator",
                "angles": ["front", "side", "three_quarter", "back"],
                "colors": ["black", "brown"],
                "accessories": ["glasses", "tie", "blazer"]
            },
            "engineer": {
                "name": "Engineer",
                "description": "Technical professional",
                "angles": ["front", "side", "three_quarter", "back"],
                "colors": ["blue", "gray"],
                "accessories": ["hard_hat", "safety_vest"]
            },
            "lawyer": {
                "name": "Lawyer",
                "description": "Legal professional",
                "angles": ["front", "side", "three_quarter", "back"],
                "colors": ["black", "navy"],
                "accessories": ["suit", "tie", "briefcase"]
            },
            "business": {
                "name": "Business Executive",
                "description": "Corporate professional",
                "angles": ["front", "side", "three_quarter", "back"],
                "colors": ["black", "gray", "navy"],
                "accessories": ["suit", "tie", "watch"]
            },
            "artist": {
                "name": "Artist",
                "description": "Creative professional",
                "angles": ["front", "side", "three_quarter", "back"],
                "colors": ["vibrant", "creative"],
                "accessories": ["beret", "paint_brush", "palette"]
            }
        }
        
        # Save metadata if it doesn't exist
        metadata_path = os.path.join(self.templates_dir, self.templates_metadata_file)
        if not os.path.exists(metadata_path):
            with open(metadata_path, 'w') as f:
                json.dump(default_templates, f, indent=2)

    async def get_templates(self, profession: str) -> List[Dict[str, Any]]:
        """Get available templates for a specific profession"""
        try:
            metadata_path = os.path.join(self.templates_dir, self.templates_metadata_file)
            
            if not os.path.exists(metadata_path):
                return []
            
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            if profession not in metadata:
                return []
            
            profession_data = metadata[profession]
            templates = []
            
            for angle in profession_data.get("angles", []):
                template_path = os.path.join(self.templates_dir, profession, f"{angle}.jpg")
                
                # Check if template file exists, otherwise create placeholder
                if not os.path.exists(template_path):
                    await self._create_placeholder_template(profession, angle)
                
                templates.append({
                    "id": f"{profession}_{angle}",
                    "profession": profession,
                    "angle": angle,
                    "image_url": f"/templates/{profession}/{angle}.jpg",
                    "description": f"{profession_data['name']} - {angle.replace('_', ' ').title()} view",
                    "available": os.path.exists(template_path)
                })
            
            return templates
            
        except Exception as e:
            print(f"Error getting templates: {str(e)}")
            return []

    async def _create_placeholder_template(self, profession: str, angle: str):
        """Create a placeholder template image"""
        import cv2
        import numpy as np
        
        # Create profession directory
        profession_dir = os.path.join(self.templates_dir, profession)
        os.makedirs(profession_dir, exist_ok=True)
        
        # Create placeholder image
        template = np.ones((512, 512, 3), dtype=np.uint8) * 128
        
        # Add profession and angle text
        cv2.putText(template, profession.title(), (50, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        cv2.putText(template, f"Angle: {angle.replace('_', ' ').title()}", (50, 250), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(template, "Template Placeholder", (50, 350), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
        
        # Save template
        template_path = os.path.join(profession_dir, f"{angle}.jpg")
        cv2.imwrite(template_path, template)

    async def get_template_path(self, profession: str, angle: str) -> Optional[str]:
        """Get the file path for a specific template"""
        template_path = os.path.join(self.templates_dir, profession, f"{angle}.jpg")
        
        if os.path.exists(template_path):
            return template_path
        
        # Create placeholder if it doesn't exist
        await self._create_placeholder_template(profession, angle)
        return template_path if os.path.exists(template_path) else None

    async def get_all_professions(self) -> List[Dict[str, Any]]:
        """Get all available professions with their metadata"""
        try:
            metadata_path = os.path.join(self.templates_dir, self.templates_metadata_file)
            
            if not os.path.exists(metadata_path):
                return []
            
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            professions = []
            for prof_id, prof_data in metadata.items():
                professions.append({
                    "id": prof_id,
                    "name": prof_data["name"],
                    "description": prof_data["description"],
                    "angles": prof_data.get("angles", []),
                    "colors": prof_data.get("colors", []),
                    "accessories": prof_data.get("accessories", [])
                })
            
            return professions
            
        except Exception as e:
            print(f"Error getting professions: {str(e)}")
            return []

    async def add_template(self, profession: str, angle: str, image_path: str) -> bool:
        """Add a new template for a profession and angle"""
        try:
            # Create profession directory
            profession_dir = os.path.join(self.templates_dir, profession)
            os.makedirs(profession_dir, exist_ok=True)
            
            # Copy image to template directory
            import shutil
            template_path = os.path.join(profession_dir, f"{angle}.jpg")
            shutil.copy2(image_path, template_path)
            
            return True
            
        except Exception as e:
            print(f"Error adding template: {str(e)}")
            return False 