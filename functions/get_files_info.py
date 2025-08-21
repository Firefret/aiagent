import os

def get_files_info(working_directory, directory="."):
    try:

        # Check if the directory is valid
        path = os.path.join(working_directory, directory)
        absolute_path = os.path.abspath(path)
        if not os.path.isdir(absolute_path):
            print (f'Error: "{absolute_path}" is not a directory')
            return None
        if not absolute_path.startswith(os.path.abspath(working_directory)):
            print (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
            return None

        # List files in the directory
        filelist = os.listdir(absolute_path)
        print(f'Result for {"current directory" if directory == "." else directory}:')
        for filename in filelist:
            file_reference = os.path.join(absolute_path, filename)
            is_dir = os.path.isdir(file_reference)
            file_size = os.path.getsize(file_reference)
            print(f'- {filename}: file_size={file_size} bytes, is_dir={is_dir}')
    except Exception as e:
        return f'Error: {e}'
