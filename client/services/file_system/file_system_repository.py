import os


class FileSystemRepository:
    def __init__(self):
        self.current_dir = os.getcwd()

    def get_current_dir(self):
        return self.current_dir

    def get_files(self):
        return os.listdir(self.current_dir)

    def get_file_path(self, file_name):
        return os.path.join(self.current_dir, file_name)

    def change_dir(self, dir_name):
        self.current_dir = os.path.join(self.current_dir, dir_name)

    def is_file(self, file_name):
        return os.path.isfile(self.get_file_path(file_name))

    def is_dir(self, dir_name):
        return os.path.isdir(self.get_file_path(dir_name))

    def read_file(self, file_name):
        with open(self.get_file_path(file_name), 'r') as f:
            return f.read()
        
        return None
    
    def write_file(self, file_name, content):
        if not os.path.exists(self.current_dir):
            os.makedirs(self.current_dir)
        with open(self.get_file_path(file_name), 'w') as f:
            open("log.txt", "a").write(f"{file_name} {content[:20]}\n")
            f.write(content)