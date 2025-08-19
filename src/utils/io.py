def read_file(file_path):
    """Read the contents of a file and return it."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    """Write content to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def append_to_file(file_path, content):
    """Append content to a file."""
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content)

def file_exists(file_path):
    """Check if a file exists."""
    import os
    return os.path.isfile(file_path)

def create_directory(directory_path):
    """Create a directory if it does not exist."""
    import os
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def list_files_in_directory(directory_path):
    """List all files in a directory."""
    import os
    return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]