class IOManager:
    @staticmethod
    def read_file(file_path: str):
        return open(file_path, 'r').read()
