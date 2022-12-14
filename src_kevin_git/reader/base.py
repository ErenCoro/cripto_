class BaseReader():
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        raise NotImplementedError("This method hasn't been implemented yet")

    def write(self, arr, dest_filename):
        raise NotImplementedError("This method hasn't been implemented yet")
