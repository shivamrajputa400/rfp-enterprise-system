import os
import aiofiles
import logging
from fastapi import UploadFile

logger = logging.getLogger(__name__)

class FileProcessor:
    def __init__(self):
        self.upload_dir = "uploads"
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def save_uploaded_file(self, file: UploadFile) -> str:
        file_path = os.path.join(self.upload_dir, file.filename)
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        return file_path
    
    async def extract_text(self, file_path: str) -> str:
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                return await f.read()
        except:
            async with aiofiles.open(file_path, 'r', encoding='latin-1') as f:
                return await f.read()
