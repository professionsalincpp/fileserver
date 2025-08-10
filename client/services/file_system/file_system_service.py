from services.file_system.file_system_repository import FileSystemRepository


class FileSystemService(FileSystemRepository):
    def __init__(self):
        super().__init__()

    def save_file(self, file_name, content):
        self.write_file(file_name, content)