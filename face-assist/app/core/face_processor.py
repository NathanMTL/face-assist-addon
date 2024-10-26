import os
import numpy as np
import face_recognition
from PIL import Image
import logging
from typing import Dict, List, Tuple, Optional

class FaceProcessor:
    def __init__(self, face_db_path: str):
        """Initialize the face processor.
        
        Args:
            face_db_path: Path to the face database directory
        """
        self.face_db_path = face_db_path
        self.known_faces: Dict[str, List[np.ndarray]] = {}
        self.load_known_faces()
        self.logger = logging.getLogger(__name__)

    def load_known_faces(self) -> None:
        """Load all known faces from the database directory."""
        try:
            for person_dir in os.listdir(self.face_db_path):
                person_path = os.path.join(self.face_db_path, person_dir)
                if os.path.isdir(person_path):
                    self._load_person_faces(person_dir, person_path)
        except Exception as e:
            self.logger.error(f"Error loading faces: {e}")

    def _load_person_faces(self, person: str, path: str) -> None:
        """Load face encodings for a specific person.
        
        Args:
            person: Name of the person
            path: Path to person's directory
        """
        encodings = []
        for img_file in os.listdir(path):
            if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    img_path = os.path.join(path, img_file)
                    image = face_recognition.load_image_file(img_path)
                    face_encodings = face_recognition.face_encodings(image)
                    if face_encodings:
                        encodings.extend(face_encodings)
                except Exception as e:
                    self.logger.error(f"Error processing {img_path}: {e}")
        
        if encodings:
            self.known_faces[person] = encodings

    def add_face(self, person: str, image_path: str) -> Tuple[bool, str]:
        """Add a new face to the database.
        
        Args:
            person: Name of the person
            image_path: Path to the image file
            
        Returns:
            Tuple of (success, message)
        """
        try:
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if not face_encodings:
                return False, "No face detected in image"
            
            if person not in self.known_faces:
                self.known_faces[person] = []
            
            self.known_faces[person].extend(face_encodings)
            return True, "Face added successfully"
            
        except Exception as e:
            self.logger.error(f"Error adding face: {e}")
            return False, f"Error processing image: {str(e)}"

    def verify_face(self, person: str, image_path: str) -> Tuple[bool, float]:
        """Verify if a face matches a known person.
        
        Args:
            person: Name of the person to verify against
            image_path: Path to the image to verify
            
        Returns:
            Tuple of (match boolean, confidence percentage)
        """
        try:
            if person not in self.known_faces:
                return False, 0.0
            
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if not face_encodings:
                return False, 0.0
            
            matches = face_recognition.compare_faces(
                self.known_faces[person], 
                face_encodings[0],
                tolerance=0.6
            )
            
            confidence = (sum(matches) / len(matches)) * 100 if matches else 0.0
            return confidence >= 80, confidence
            
        except Exception as e:
            self.logger.error(f"Error verifying face: {e}")
            return False, 0.0

    def get_face_count(self, person: str) -> int:
        """Get the number of faces stored for a person.
        
        Args:
            person: Name of the person
            
        Returns:
            Number of faces stored
        """
        return len(self.known_faces.get(person, []))

    def list_people(self) -> List[Dict[str, any]]:
        """Get list of all people in the database with their face counts.
        
        Returns:
            List of dictionaries containing person details
        """
        return [
            {
                'name': person,
                'face_count': len(encodings)
            }
            for person, encodings in self.known_faces.items()
        ]
