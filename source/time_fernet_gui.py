from fernet_gui import FernetGUI
from cryptography.fernet import Fernet, InvalidToken
import time
import logging

DUREE_DE_VIE_MESSAGE = 30

"""
@class TimeFernetGUI
@brief A class handling message time-to-live in addition to Fernet encrypting.
@extends FernetGUI
"""
class TimeFernetGUI(FernetGUI):

    """
    @fn __init__()
    @brief Regular __init__ function
    """
    def __init__(self) -> None:
        super().__init__()
    

    """
    @fn encrypt()
    @brief Encrypts a message with Fernet and gives a TTL to it.
    @param message A message string
    """
    def encrypt(self, message: str):
        encryptor = Fernet(self._key)
        token = encryptor.encrypt_at_time(bytes(message, 'utf-8'), current_time=int(time.time()))
        return token
    
    """
    @fn decrypt()
    @brief Decrypts the message sent by another user with Fernet. This time, the TTL handling is added as part of the try/except statement. If the message has expired, an error is logged and the GUI crashes.
    @param frame A frame containing an encrypted message
    """
    def decrypt(self, frame: bytes) -> str:
        decryptor = Fernet(self._key)
        message = ""
        try:
            message = decryptor.decrypt_at_time(frame, current_time=int(time.time()), ttl=DUREE_DE_VIE_MESSAGE)

        except InvalidToken as e:
            logging.error(f"InvalidToken exception at {int(time.time())}")
            raise e
        
        return str(message, 'utf-8') 
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    client = TimeFernetGUI()
    client.create()
    client.loop()
