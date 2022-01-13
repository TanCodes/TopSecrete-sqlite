# import basehash

# hash_fn = basehash.base62()  # you can initialize a 36, 52, 56, 58, 62 and 94 base fn
# password = int("1")
# hash_value = hash_fn.hash(password) 
# unhashed = hash_fn.unhash(hash_value) 

# print(hash_value)
# print(unhashed)

# alphabets="abcdefghijklmnopqrsdt"
# message=input("Enter the message to encrypt: ")
# encrypt,decrypt="",""
# key=5

# for letter in message:
#     new_position=(alphabets.find(letter)+key)%len(alphabets)
#     encrypt+=alphabets[new_position]

# for letter in encrypt:
#     new_position=(alphabets.find(letter)-key)%len(alphabets)
#     decrypt+=alphabets[new_position]


# print("Encrypted message:",encrypt)
# print("Decrypted message:",decrypt)

# ---------------------------------------------------------------

import base64
import random 
import string

text = input("enter :")
password =text.encode("utf-8")

encoded = base64.b64encode(password)
x = str(encoded, 'UTF8')
print("encoded",x )

S = 10  
create_random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))   
len_c = len(create_random_string)

final_encoded_string = f"{create_random_string}{x}{create_random_string}"
print("ddddddfinal_encoded_string",final_encoded_string)

to_slice = final_encoded_string[len_c:-len_c]

decoded = base64.b64decode(to_slice)
final_decoded = str(decoded, 'UTF8')
print("final_decoded",final_decoded)


# BIV5AZCH9TdGFubWF5BIV5AZCH9T
# 0IMAOECKJ2dGFubWF50IMAOECKJ2
# Q9B8398L0MOTc2Njg4NTM3MQ==Q9B8398L0M