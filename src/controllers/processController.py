from .BassController import BassController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum


class ProcessController(BassController):
    
    # Define supported text extensions
    TEXT_EXTENSIONS = {'.txt', '.text'}
    PDF_EXTENSIONS = {'.pdf'}
    
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str):
        ext = os.path.splitext(file_id)[-1].lower()
        return ext

    def get_file_loader(self, file_id: str):
        file_ext = self.get_file_extension(file_id)
        file_path = os.path.join(self.project_path, file_id)

        # Check for text files (.txt, .text, etc.)
        if file_ext in self.TEXT_EXTENSIONS:
            return TextLoader(file_path, encoding='utf-8')

        # Check for PDF files
        if file_ext in self.PDF_EXTENSIONS:
            return PyMuPDFLoader(file_path)

        return None

    def get_file_content(self, file_id: str):
        loader = self.get_file_loader(file_id=file_id)

        if loader is None:
            file_ext = self.get_file_extension(file_id)
            supported = self.TEXT_EXTENSIONS | self.PDF_EXTENSIONS
            raise ValueError(
                f"Unsupported file type: '{file_ext}' for file '{file_id}'. "
                f"Supported extensions: {supported}"
            )

        return loader.load()

    def process_file_content(self, file_content: list, file_id: str, chunk_size: int = 100, overlap: int = 20):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            length_function=len
        )

        file_content_texts = [rec.page_content for rec in file_content]
        file_content_metadata = [rec.metadata for rec in file_content]

        chunks = text_splitter.create_documents(file_content_texts, metadatas=file_content_metadata)

        return chunks