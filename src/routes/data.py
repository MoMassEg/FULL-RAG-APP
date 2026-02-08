from fastapi import FastAPI, APIRouter , Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings , Settings
from controllers import DataControllers, ProjectController
import aiofiles
from models import ResponseSignal
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):

    # Validate file type and size
    data_controller = DataControllers()
    is_valid, message = data_controller.validate_uploaded_file(file=file)

    
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": message})

    project_dir_path = ProjectController().get_project_path(project_id=project_id)

    file_path, file_id = data_controller.generate_unique_filepath(orig_file_name=file.filename, project_id=project_id)


    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFULT_CHUNK_SIZE):  # Read file in chunks
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=ResponseSignal.FILE_UPLOAD_FAILED.value)

    return JSONResponse( content={"message": ResponseSignal.FILE_UPLOAD_SUCCESS.value, "file_id": file_id})
    