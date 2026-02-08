from .BassController import BassController
from .ProjectController import ProjectController
import os
from fastapi import UploadFile
from models import ResponseSignal
import re
class DataControllers(BassController):


    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024  # Convert MB to Bytes
    def validate_uploaded_file(self, file: UploadFile):
        # Implement file validation logic based on app settings
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE_MB * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True , ResponseSignal.FILE_VALIDATION_SUCCESS.value
    
    def generate_unique_filepath(self, orig_file_name: str, project_id: str):
        # Generate a unique filename to prevent overwriting existing files
        random_key = self.generate_random_filename()
        project_path = ProjectController().get_project_path(project_id=project_id)

        clean_file_name = self.get_clean_file_name(orig_file_name)
        
        new_file_path = os.path.join(project_path, f"{random_key}_{clean_file_name}")

        while os.path.exists(new_file_path):
            random_key = self.generate_random_filename()
            new_file_path = os.path.join(project_path, f"{random_key}_{clean_file_name}")

        return new_file_path , f"{random_key}_{clean_file_name}"

    def get_clean_file_name(self, file_name: str):
        # Remove any potentially harmful characters from the file name
        clean_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', file_name)
        return clean_name