from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.convertor import convert_file

router = APIRouter()

@router.post("/")
async def convert_endpoint(
    file: UploadFile = File(...),
    target_format: str = Form(...),
    run_profanity: bool = Form(False),
    run_spellcheck: bool = Form(False)
):
    # endpoint to handle file conversion requests

    # Call conversion function
    output_path = await convert_file(file, target_format, run_profanity, run_spellcheck)

    return JSONResponse(
        {"message": "Conversion endpoint reached.", "output_path": output_path}
    )