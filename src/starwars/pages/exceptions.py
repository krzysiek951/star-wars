class NotSupportedFileExtension(Exception):

    def __init__(self, file_extension):
        self.file_extension = file_extension
        self.msg = f"'Collection file extension: '{file_extension}' is not supported."
        super().__init__(self.msg)
