from algorithm.base import BaseAlgorithm
from reader.base import BaseReader

import numpy as np
import importlib
import json
from hashlib import blake2b





def import_class(module):
    module_list = module.split(".")
    module = importlib.import_module(".".join(module_list[:-1]))
    clazz = getattr(module, module_list[-1])
    return clazz


def validate_data(data):
    #if not isinstance(data, (np.ndarray,)):
    #    raise TypeError("Readed data is not an np.array")
    #elif data.dtype is not np.dtype('int16'):
    #    raise TypeError("Readed data is not np.uint8")
    #elif len(data.shape) > 1:
    #    raise ValueError("The dimensions of your array must be one")
    pass


def process(key, file, output, reader, algorithm):
    Reader = import_class(reader)
    Algorithm = import_class(algorithm)

    reader = Reader(file)
    algorithm = Algorithm()

    #key = np.frombuffer(bytes(key, "utf-8"), dtype=np.uint8).tolist()

    ########PROCESS KEY 
    h = blake2b()
    key = h.hexdigest()
    key = np.frombuffer(bytes(key, "utf-8"), dtype=np.uint8).tolist()


    if not issubclass(type(reader), BaseReader):
        raise TypeError("reader must be a subclass of reader.base.BaseReader")

    
    if not issubclass(type(algorithm), BaseAlgorithm):
        raise TypeError("algorithm must be a subclass of algorithm.base.BaseAlgorithm")

    data = reader.read()
    validate_data(data)

    data = algorithm.encrypt(key, data)
    validate_data(data)

    reader.write(data, "encrypted_{}".format(output))
    validate_data(data)

    data = algorithm.decrypt(key, data)
    validate_data(data)


    reader.write(data, "decrypted_{}".format(output))
    validate_data(data)


if __name__ == "__main__":
    with open("config.json") as jsonFile:
        config = json.load(jsonFile)
        
    process(config["key"], config["file"], config["output"], config["reader"], config["algorithm"])
