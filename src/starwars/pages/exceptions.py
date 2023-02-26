class NotSupportedFileExtension(Exception):

    def __init__(self, file_extension):
        self.file_extension = file_extension
        self.msg = f"'Collection file extension: '{file_extension}' is not supported."
        super().__init__(self.msg)


class MissingTableField(Exception):

    def __init__(self, field):
        self.field = field
        self.msg = f"'Field: '{field}' does not exist in table header."
        super().__init__(self.msg)
