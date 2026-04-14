import os
import mimetypes

def get_mime_type(file_path:str):
    """
    Detects the MIME type of a file.
    - First tries python-magic (content-based detection)
    - Falls back to mimetypes (extension-based detection)
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Try python-magic if available
    try:
        import magic
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(file_path)
        if mime_type:
            return mime_type
    except ImportError:
        print("python-magic not installed. Falling back to mimetypes.")
    except Exception as e:
        print(f"python-magic failed: {e}. Falling back to mimetypes.")

    # Fallback: mimetypes (based on file extension)
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "Unknown"
