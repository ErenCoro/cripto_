class BaseAlgorithm():
    def __init__(self):
        pass

    def encrypt(self, key, data):
        raise NotImplementedError("This method hasn't been implemented yet")
    
    def decrypt(self, key, data):
        raise NotImplementedError("This method hasn't been implemented yet")