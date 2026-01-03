import os
import pypandoc
import uuid
from fastapi import HTTPException
from app.services.filters import apply_filters

# Automatically download Pandoc if not found

#try:
#   pypandoc.get_pandoc_version()
#except OSError:
#    print("[INFO] Pandoc not found. Downloading locally...")
#    pypandoc.download_pandoc()
###
pypandoc.ensure_pandoc_installed()

UPLOAD_DIR = "converted_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # make sure directory exists

def convert_to_txt(input_path: str, input_ext: str, output_txt_path: str):
    input_format_map = {
        ".txt": "markdown",
        ".docx": "docx"
    }

    input_format = input_format_map.get(input_ext)
    if not input_format:
        raise HTTPException(400, "Unsupported input format for text conversion")

    pypandoc.convert_file(
        input_path,
        to="plain",
        format=input_format,
        outputfile=output_txt_path
    )

def convert_from_txt(txt_path: str, target_format: str, output_path: str):
    """
    Converts plain text (.txt) into the requested output format.
    """
    output_format_map = {
        "txt": "markdown",
        "docx": "docx",
        "pdf": "pdf"
    }

    output_format = output_format_map.get(target_format)
    if not output_format:
        raise HTTPException(400, "Unsupported output format")

    pypandoc.convert_file(
        txt_path,
        to=output_format,
        format="markdown",
        outputfile=output_path
    )

async def convert_file(file, target_format: str, run_profanity: bool, run_spellcheck: bool) -> str:
    
    if file is None:
        raise HTTPException(status_code= 400, detail="No file provided for conversion.")
    
    original_name, ext = os.path.splitext(file.filename)

    # Simulate an output file path
    output_path = f"{original_name}.{target_format}"

    #print("File extension detected:", ext)

    allowed_inputs = ['.txt', '.docx']
    allowed_outputs = ['pdf', 'docx', 'txt']

    if ext not in allowed_inputs:
        raise HTTPException(status_code= 400, detail=f"Unsupported text format: {ext}")
    
    if target_format.lower() not in allowed_outputs:
        raise HTTPException(status_code= 400, detail=f"Unsupported text format: {target_format}")

    # Generate a unique identifier to prevent overwriting files
    unique_id = str(uuid.uuid4())[:4]
    safe_filename = f"{original_name}_{unique_id}.{target_format}"

    input_path = os.path.join(UPLOAD_DIR, f"{original_name}_{unique_id}{ext}")
    txt_path = os.path.join(UPLOAD_DIR, f"{original_name}_{unique_id}_filtered.txt")
    output_path = os.path.join(UPLOAD_DIR, f"{original_name}_{unique_id}_final.{target_format}")


    if original_name == "":
        raise HTTPException(status_code=400, detail="Invalid file name.")
    
    print(f"Starting to convert {original_name} to {target_format}")

    # Create local paths
    #input_path = os.path.join(UPLOAD_DIR, f"{original_name}_{unique_id}{ext}")
    #output_path = os.path.join(UPLOAD_DIR, safe_filename)

    # Save the uploaded file to input_path
    try:
        with open(input_path, "wb") as f:
            f.write(await file.read())

    except Exception as e:
        print(f"Failed to save uploaded file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.") from e
    
    
    try:
        # Convert upload to TXT
        convert_to_txt(input_path, ext, txt_path)

        # Apply filters (ONLY on TXT)
        if run_profanity or run_spellcheck:
            await apply_filters(
                txt_path,
                run_profanity=run_profanity,
                run_spellcheck=run_spellcheck
            )

        # Convert TXT to target format
        if target_format == "txt":
            return txt_path

        convert_from_txt(txt_path, target_format, output_path)
        print(f"File conversion successful: {output_path}")

    except Exception as e:
        print("CONVERSION ERROR:", repr(e))
        raise HTTPException(500, f"Conversion failed: {str(e)}")

    return output_path
