from ciphered_gui import CipheredGUI
from cryptography import fernet
from cryptography.hazmat.primitives.hashes import Hash, SHA256 


class FernetGUI(CipheredGUI):
    def __init__(self) -> None:
        super().__init__()


    def run_chat(self) -> None:
        key = Hash(SHA256())
        key.update(super()._password)
        key.finalize()
        print(key)
        super().run_chat(None, None)

if __name__ == "__main__":
    client = FernetGUI()
    client.create()
    client.loop()
