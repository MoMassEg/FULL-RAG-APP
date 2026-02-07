from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATION_SUCCESS = "File is valid."
    FILE_UPLOAD_SUCCESS = "File uploaded successfully."
    FILE_TYPE_NOT_SUPPORTED = "Invalid file type. Only .txt, .pdf, and .docx files are allowed."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit of 10 MB."
    FILE_UPLOAD_FAILED = "File upload failed due to an unexpected error."