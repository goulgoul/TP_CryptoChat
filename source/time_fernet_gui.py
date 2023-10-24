from fernet_gui import FernetGUI
from cryptography.fernet import Fernet, InvalidToken
import time
import logging

class TimeFernetGUI(FernetGUI):

    def __init__(self) -> None:
        super().__init__()
    
    def encrypt(self, message: str):
        encryptor = Fernet(self._key)
        token = encryptor.encrypt_at_time(bytes(message, 'utf-8'), current_time=int(time.time()))
        return token
    

    def decrypt(self, frame: bytes) -> str:
        decryptor = Fernet(self._key)
        message = ""
        try:
            message = decryptor.decrypt_at_time(frame, current_time=int(time.time()), ttl=30)

        except InvalidToken as e:
            logging.error(f"InvalidToken exception at {int(time.time())}")
            raise e
        
        return str(message, 'utf-8') 
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    client = TimeFernetGUI()
    client.create()
    client.loop()
