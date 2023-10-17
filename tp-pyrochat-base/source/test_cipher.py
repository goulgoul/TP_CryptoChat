
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

IV_LENGTH = 16
KEY_LENGTH = 16
KDF_NB_ITERATIONS = 480000
KDF = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = KEY_LENGTH,
        salt = b'oskour',
        iterations = KDF_NB_ITERATIONS
        )

key = KDF.derive(bytes('bite', 'utf8'))

def encrypt(message):
    iv = os.urandom(IV_LENGTH)
    cipher = Cipher(algorithms.AES128(key), modes.CTR(iv))
    encryptor = cipher.encryptor() 
    payload = encryptor.update(bytes(message, 'utf8')) + encryptor.finalize()
    return (payload, iv)

def decrypt(frame):
    payload, iv = frame
    cipher = Cipher(algorithms.AES128(key), modes.CTR(iv))
    decryptor = cipher.decryptor()
    message = decryptor.update(payload) + decryptor.finalize()
    return str(message, 'utf8')



if __name__ == "__main__":
   
    # iv = os.urandom(IV_LENGTH)
    # cipher = Cipher(algorithms.AES128(key), modes.CTR(iv))
    # encryptor = cipher.encryptor()
    # ct = encryptor.update(b"a secret message") + encryptor.finalize()
    # decryptor = cipher.decryptor()
    # ct = decryptor.update(ct) + decryptor.finalize()
    # print (ct)
    print(decrypt(encrypt('bojo')))
