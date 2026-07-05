from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import List
import uuid
import os
import aiofiles
from app.middleware.exception_handler import response_handler
from app.services.jwt_bearer import get_payload
from app.config.settings import settings

router = APIRouter(prefix="/upload", tags=["Upload"])

def cleanup(saved_paths):
    for path in saved_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            pass

@router.post("/image")
async def upload_image(files: List[UploadFile] = File(...), positions: List[str] = Form(...), payload = Depends(get_payload)):
    saved_paths = []
    try:
        if payload["role"] != "admin":
            raise HTTPException(status_code=403, detail="Access denied")

        if not files:
            raise HTTPException(status_code=400, detail="At least one file is required")
        
        if len(files) != len(positions):
            raise HTTPException(status_code=400, detail="Files and positions length mismatch")

        os.makedirs(settings.UPLOAD_IMAGES_PRODUCT, exist_ok=True)

        results = []
        for file, position in zip(files, positions):

            if file.content_type not in settings.ALLOWED_CONTENT_TYPES:
                raise HTTPException(status_code=400, detail="Only image files are allowed")
            
            file_ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
            if file_ext not in settings.ALLOWED_EXTENSIONS:
                raise HTTPException(status_code=400, detail="Invalid file extension")
            
            content = await file.read()

            if len(content) > settings.MAX_FILE_SIZE:
                raise HTTPException(status_code=400, detail="File too large (max 5MB)")

            file_name = f"{uuid.uuid4().hex}.{file_ext}"
            file_path = os.path.join(settings.UPLOAD_IMAGES_PRODUCT, file_name)

            saved_paths.append(file_path)
            
            async with aiofiles.open(file_path, "wb") as buffer:
                await buffer.write(content)

            results.append({
                "url": f"/{settings.UPLOAD_IMAGES_PRODUCT}/{file_name}",
                "position": position
            })

        return response_handler(
            status = True,
            message="Image uploaded successfully",
            data=results,
            status_code=201
        )
    except HTTPException:
        cleanup(saved_paths)
        raise
    except Exception:
        cleanup(saved_paths)
        raise HTTPException(status_code=500, detail="Image upload failed")
