from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
import base64

BLOCK_SIZE = 16


def decode_base64(b64):
    return base64.b64decode(b64)

def read_from_base64():
    return [ decode_base64(input()), decode_base64(input()), decode_base64(input())]

def decrypt_message(key, iv, message):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(message)
    unpaded_text = unpad(plaintext, BLOCK_SIZE)
    return unpaded_text
    # AES 256 암호화 구현

[secretkey, iv, message] = read_from_base64()

result = decrypt_message(secretkey, iv, message).decode('utf-8')
print(result)