import base64
from ciphered_gui import CipheredGUI
from cryptography import fernet
from cryptography.hazmat.primitives.hashes import Hash, SHA256 


class FernetGUI(CipheredGUI):
    def __init__(self) -> None:
        super().__init__()


    def run_chat(self) -> None:
        digest = Hash(SHA256())
        digest.update(bytes(self._password, 'utf-8'))
        self._key = base64.b64encode(digest.finalize())
        super().run_chat()
    
    def encrypt(self, message: str) -> 

if __name__ == "__main__":
    client = FernetGUI()
    client.create()
    client.loop()
