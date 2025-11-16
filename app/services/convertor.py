import os
import tempfile
import pypandoc
import uuid
from fastapi import HTTPException

# Automatically download Pandoc if not found
try:
    pypandoc.get_pandoc_version()
except OSError:
    print("[INFO] Pandoc not found. Downloading locally...")
    pypandoc.download_pandoc()

UPLOAD_DIR = "converted_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # make sure directory exists

async def convert_file(file, target_format: str) -> str:
    
    if file is None:
        raise HTTPException(status_code= 400, detail="No file provided for conversion.")
    
    # Save uploaded file temporarily
    original_name, ext = os.path.splitext(file.filename)

    # Simulate an output file path
    output_path = f"{original_name}.{target_format}"

    formatSupported = ['txt', 'docx', 'pdf']
    if ext not in formatSupported:
        raise HTTPException(status_code= 400, detail=f"Unsupported text format: {ext}")
    
    if target_format not in formatSupported:
        raise HTTPException(status_code= 400, detail=f"Unsupported text format: {target_format}")

    # Generate a unique identifier to prevent overwriting files
    unique_id = str(uuid.uuid4())[:4]
    safe_filename = f"{original_name}_{unique_id}.{target_format}"

    if original_name == "":
        raise HTTPException(status_code=400, detail="Invalid file name.")
    
    print(f"Starting to convert {original_name} to {target_format}")

    # Create local paths
    input_path = os.path.join(UPLOAD_DIR, f"{original_name}_{unique_id}{ext}")
    output_path = os.path.join(UPLOAD_DIR, safe_filename)

    # Save the uploaded file to input_path
    try:
        with open(input_path, "wb") as f:
            f.write(await file.read())

    except Exception as e:
        print(f"Failed to save uploaded file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.") from e
    
    format_map = {
        ".txt": "markdown",   # treat .txt as markdown/plain text
        ".docx": "docx"
    }

    input_format = format_map.get(ext.lower(), "markdown")  # default to markdown

    try:
        pypandoc.convert_file(input_path, to=target_format, format=input_format, outputfile=output_path)
        print(f"file Conversion Successful... {output_path}")

    except Exception as e:
        print(f"Conversion failed: {e}")
        raise RuntimeError("File conversion failed.") from e

    return output_path
