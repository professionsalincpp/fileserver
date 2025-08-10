import os

class FileProcessor:
    @classmethod
    def read_file(cls, filepath: str) -> bytes | None:
        """
        Reads the content of a file and returns it as a string.
        
        Params:
            filepath (str): The path to the file to be read.
        
        Returns:
            (str or None): The content of the file as a string, or None if the file does not exist.
        """
        if cls.file_exists(filepath):
            with open(filepath, 'rb') as file:
                return file.read()
            
        return None
    
    @classmethod
    def write_file(cls, filepath: str, data: bytes) -> None:
        """
        Writes a string to a file.
        
        Params:
            filepath (str): The path to the file to be written.
        """
        with open(filepath, 'wb') as file:
            return file.write(data)

    @classmethod
    def file_exists(cls, file_path: str) -> bool:
        """
        Checks if a file exists.
        
        Params:
            file_path (str): The path to the file to be checked.
        
        Returns:
            (bool): True if the file exists, False otherwise.
        """
        return os.path.exists(file_path) and os.path.isfile(file_path)