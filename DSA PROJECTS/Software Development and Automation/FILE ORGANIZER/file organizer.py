import os
from pathlib import Path
import time
import sys

def organize_downloads(folder_path):
    if not Path(folder_path).is_dir():
        sys.exit(f"The path {folder_path} does not exist or is not a directory.")

    extension_directories = {}

    for entry in os.scandir(folder_path):
        if entry.is_file():
            file_path = Path(entry)
            file_extension = file_path.suffix.lower()
            if not file_extension:
                continue
            if file_extension not in extension_directories:
                directory_path = Path(folder_path) / file_extension[1:]  # Removes dot from extension
                directory_path.mkdir(exist_ok=True)
                extension_directories[file_extension] = directory_path
            else:
                directory_path = extension_directories[file_extension]
            try:
                file_path.rename(directory_path.joinpath(file_path.name))
            except Exception as e:
                sys.exit(f"Error moving file {file_path}: {e}")

print("Sample Usage: C:/Users/YourUsername/Downloads")
organize_downloads(input("Enter the directory/folder you want to sort (copy address of directory/folder): "))
print("Operation completed successfully.")
time.sleep(2)
sys.exit("Goodbye!")
