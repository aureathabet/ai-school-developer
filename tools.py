import os
import subprocess
import requests
from typing import Optional
from langchain.tools import tool

ROOT_DIR = "./"
VALID_FILE_TYPES = {"py", "txt", "md", "cpp", "c", "java", "js", "html", "css", "ts", "json"}


@tool
def create_directory(directory: str) -> str:
    """
    Create a new writable directory with the given directory name if it does not exist.
    If the directory exists, it ensures the directory is writable.

    Parameters:
    directory (str): The name of the directory to create.

    Returns:
    str: Success or error message.
    """
    if ".." in directory:
        return f"Cannot make a directory with '..' in path"
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            # Set directory as writable
            os.chmod(directory, 0o700)
            return f"Directory '{directory}' successfully created and set as writeable."
        else:
            # Ensure the existing directory is writable
            os.chmod(directory, 0o700)
            return f"Directory '{directory}' already exists and is now set as writeable."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


@tool
def find_file(filename: str, path: str) -> Optional[str]:
    """
    Recursively searches for a file in the given path.
    Returns string of full path to file, or None if file not found.
    """
    # TODO handle multiple matches
    for root, dirs, files in os.walk(path):
        if filename in files:
            return os.path.join(root, filename)
    return None


@tool
def create_file(filename: str, content: str = "", directory=""):
    """Creates a new file and content in the specified directory."""
    # Validate file type
    try:
        file_stem, file_type = filename.split(".")
        assert file_type in VALID_FILE_TYPES
    except:
        return f"Invalid filename {filename} - must end with a valid file type: {VALID_FILE_TYPES}"
    directory_path = os.path.join(ROOT_DIR, directory)
    file_path = os.path.join(directory_path, filename)
    if not os.path.exists(file_path):
        try:
            with open(file_path, "w")as file:
                file.write(content)
            print(f"File '{filename}' created successfully at: '{file_path}'.")
            return f"File '{filename}' created successfully at: '{file_path}'."
        except Exception as e:
            print(f"Failed to create file '{filename}' at: '{file_path}': {str(e)}")
            return f"Failed to create file '{filename}' at: '{file_path}': {str(e)}"
    else:
        print(f"File '{filename}' already exists at: '{file_path}'.")
        return f"File '{filename}' already exists at: '{file_path}'."


@tool
def update_file(filename: str, content: str, directory: str = ""):
    """Updates, appends, or modifies an existing file with new content."""
    if directory:
        file_path = os.path.join(ROOT_DIR, directory, filename)
    else:
        file_path = find_file(filename, ROOT_DIR)

    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, "a") as file:
                file.write(content)
            return f"File '{filename}' updated successfully at: '{file_path}'"
        except Exception as e:
            return f"Failed to update file '{filename}' at: '{file_path}' - {str(e)}"
    else:
        return f"File '{filename}' not found at: '{file_path}'"


@tool
def tavily_web_search(query: str):
    """Performs a web search using the Tavily API."""
    try:
        # Assuming Tavily API requires an API key and the search query
        api_key = os.getenv('TAVILY_API_KEY')
        url = f"https://api.tavily.com/search?query={query}"
        headers = {"Authorization": f"Bearer {api_key}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Assuming the response is in JSON format
        results = response.json()
        return results
    except Exception as e:
        return f"Failed to perform Tavily web search: {str(e)}"


@tool
def get_files_in_directory(directory: str):
    """Retrieves the recursive list of files in a directory and returns them as an array of file paths."""
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


@tool
def read_file(filename: str, directory: str = ""):
    """Reads the contents of a file."""
    if directory:
        file_path = os.path.join(ROOT_DIR, directory, filename)
    else:
        file_path = find_file(filename, ROOT_DIR)

    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read()
            return content
        except Exception as e:
            return f"Failed to read file '{filename}' at: '{file_path}' - {str(e)}"
    else:
        return f"File '{filename}' not found at: '{file_path}'"
