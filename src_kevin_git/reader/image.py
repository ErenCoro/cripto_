from PIL import Image
import numpy as np

from .base import BaseReader

class ImageReader(BaseReader):
    
    def read(self):
        image = Image.open(self.filename)

        image_array = np.array(image)

        self.width = image_array.shape[1]
        self.height = image_array.shape[0]
        self.channels = image_array.shape[2]

        return image_array.flatten().tolist()

    def write(self, arr, dest_filename):
        arr = np.array(arr).reshape(self.height, self.width, self.channels)
        image = Image.fromarray(arr.astype(np.uint8)).resize((self.width, self.height))
        image.save(dest_filename)

