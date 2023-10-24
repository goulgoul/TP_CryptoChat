import base64
import dearpygui.dearpygui as dpg
from generic_callback import GenericCallback
import serpent
from chat_client import ChatClient
from ciphered_gui import CipheredGUI
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes


class FernetGUI(CipheredGUI):
    def __init__(self) -> None:
        super().__init__()


    def run_chat(self) -> None:
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        self._log.info(f"Connecting {name}@{host}:{port}")

        self._callback = GenericCallback()

        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

        self._password = dpg.get_value("connection_password")
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(self._password, 'utf-8'))
        key = digest.finalize()
        self._key = base64.urlsafe_b64encode(key)
        
    
    def encrypt(self, message: str):
        encryptor = Fernet(self._key)
        token = encryptor.encrypt(bytes(message, 'utf-8'))
        return token
    
    def decrypt(self, frame: bytes) -> str:
        decryptor = Fernet(self._key)
        message = decryptor.decrypt(frame)
        return str(message, 'utf-8') 
    
    """@fn recv()
    @brief A function run periodically by the chat client class; it allows messages to be received, whatever their nature.
    This function does not require any parameter, but the input messages have to be of the same type as those sent by send().
    """
    def recv(self) -> None:
        if self._callback is None:
            return

        for user, frame in self._callback.get():
            message = self.decrypt(serpent.tobytes(frame))
            self.update_text_screen(f"{user} : {message}")
        self._callback.clear()

if __name__ == "__main__":
    client = FernetGUI()
    client.create()
    client.loop()
