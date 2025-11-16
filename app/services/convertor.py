import os
import tempfile
import pypandoc
import uuid

# Automatically download Pandoc if not found
try:
    pypandoc.get_pandoc_version()
except OSError:
    print("[INFO] Pandoc not found. Downloading locally...")
    pypandoc.download_pandoc()

UPLOAD_DIR = "converted_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # make sure directory exists

async def convert_file(file, target_format: str) -> str:
    """
    Placeholder function for file conversion logic.
    For now, just saves the uploaded file temporarily and returns its path.
    """
    # Save uploaded file temporarily
    original_name, ext = os.path.splitext(file.filename)
    # with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
    #    tmp.write(await file.read())
    #    tmp_path = tmp.name

    # Simulate an output file path
    output_path = f"{original_name}.{target_format}"

    # Generate a unique identifier to prevent overwriting files
    unique_id = str(uuid.uuid4())[:8]
    safe_filename = f"{original_name}_{unique_id}.{target_format}"

    print(f"Starting to convert {original_name} to {target_format}")

    # Create local paths
    input_path = os.path.join(UPLOAD_DIR, f"{original_name}_{unique_id}{ext}")
    output_path = os.path.join(UPLOAD_DIR, safe_filename)

    # Save the uploaded file to input_path
    with open(input_path, "wb") as f:
        f.write(await file.read())

    formatSupported = ['txt', 'docx', 'pdf']

    if target_format not in formatSupported:
        raise ValueError(f"Unsupported text format: {target_format}")
    
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
