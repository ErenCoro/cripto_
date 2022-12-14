from numpy import dtype
from .base import BaseAlgorithm
#import math

class WolframAlgorithm(BaseAlgorithm):
    def __init__(self, *args, **kwargs):
        super(WolframAlgorithm, self).__init__(*args, **kwargs)
        self.block_size = 8
        self.swap_table = [
            1,
            1,
            1,
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            0,
            1,
            1,
            1
        ]

    
    # This function must return a key that fits in 32 bits
    def fit_key(self, key):  
        #return(key)

        output = 0
        conc = ""
        for idx, byt in enumerate(key):
            conc += "{}".format(hex(byt))
            output = (output << 8) | byt
        output = output << 1
    
        #print (output, "{0:b}".format(output), len ("{0:b}".format(output)))
        return(output)


    def rshift(self, value, steps):
        return (
                (value >> steps) 
                | ((value << (self.block_size - steps)) & 0x80)
            )

    def lshift(self, value, steps):
        return (
                ((value << steps) & 0xff)
                | (value >> (self.block_size  - steps))
            )






    def process_block(self, block, key):

        key = self.fit_key(key)
        output_block = 0

        key_mask = 0x00000007
        block_mask = 0x00000001
        
        # Initial rotation
        key = self.lshift(key, 2)
        block = self.lshift(block, 1)

        for i in range(self.block_size - 1):

            neighborhood = key & key_mask
            rule_selector = block & block_mask

            index = (rule_selector << 3) | neighborhood

            output_block = output_block | self.swap_table[index]

            output_block = self.lshift(output_block, 1)
            block = self.lshift(block, 1)
            key = self.lshift(key, 1)

        output_block = self.rshift(output_block, 2)

        return output_block


    def dprocess_block(self, block, key):

        block = self.lshift(block, 2)

        key = self.fit_key(key)
        output_block = 0

 
        key_mask = 0x00000007
        block_mask = 0x00000001
        
        # Initial rotation
        key = self.lshift(key, 2)
        block = self.lshift(block, 1)

        for i in range(self.block_size - 1):

            neighborhood = key & key_mask
            rule_selector = block & block_mask

            index = (rule_selector << 3) | neighborhood

            output_block = output_block | self.swap_table[index]

            output_block = self.lshift(output_block, 1)
            block = self.lshift(block, 1)
            key = self.lshift(key, 1)



        return output_block












    def encrypt(self, key, data):


        encrypted_data = []
        encrypted_data2 = []
        encrypted_data3 = []
        encrypted_data4 = []

       
        for block in data:
            encrypted_data.append(
                self.process_block(block, key)

            )
        encrypted_data = encrypted_data[-int(len(encrypted_data)/2):] + encrypted_data[:-int(len(encrypted_data)/2)]

        for block2 in encrypted_data:
            encrypted_data2.append(
                self.process_block(block2, key)

            )
        #encrypted_data2 = encrypted_data2[-50:] + encrypted_data2[:-50]

        '''for block3 in encrypted_data2:
            encrypted_data3.append(
                self.process_block(block3, key)

            )
        encrypted_data3 = encrypted_data3[-50:] + encrypted_data3[:-50]

        for block4 in encrypted_data3:
            encrypted_data4.append(
                self.process_block(block4, key)

            )
        encrypted_data4 = encrypted_data4[-50:] + encrypted_data4[:-50]'''



        return encrypted_data2





    def decrypt(self, key, data):
        decrypted_data = []
        decrypted_data2 = []
        decrypted_data3 = []
        decrypted_data4 = []
                 

         

        
        #data = data[50:] + data[:50]

        for block in data:
            decrypted_data.append(
                self.dprocess_block(block, key)
            )


        decrypted_data = decrypted_data[int(len(decrypted_data)/2):] + decrypted_data[:int(len(decrypted_data)/2)]

        for block2 in  decrypted_data:
            decrypted_data2.append(
                self.dprocess_block(block2, key)
            )
    

        '''decrypted_data2 = decrypted_data2[50:] + decrypted_data2[:50]

        for block3 in decrypted_data2:
            decrypted_data3.append(
                self.dprocess_block(block3, key)
            )
        


        decrypted_data3 = decrypted_data3[100:] + decrypted_data3[:100]

        for block4 in decrypted_data3:
            decrypted_data4.append(
                self.dprocess_block(block4, key)
            )'''
        

   
       
        return decrypted_data2