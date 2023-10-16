from logging import warn
import os
import dearpygui.dearpygui as dpg
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from chat_client import ChatClient
from generic_callback import GenericCallback

from basic_gui import DEFAULT_VALUES, BasicGUI


class CipheredGUI(BasicGUI):
    """Encrypted GUI for chat client""" 
    def __init__(self) -> None:
        # Constructor
        super().__init__()
        self._key = None
        self._encryptor = None
        self._decryptor = None

    def _create_connection_window(self) -> None:
        # Connection window
        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):
            for field in ["host", "port", "name"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    dpg.add_input_text(default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")
                    
            with dpg.group(horizontal=True):
                dpg.add_text("password")
                dpg.add_input_text(default_value = "", tag = "connection_password", password = True)
            
            dpg.add_button(label="Connect", callback=self.run_chat)

    def run_chat(self) -> None:
        password = dpg.get_value("connection_password")
        kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 16,
        salt = b'oskour',
        iterations = 480000,
        )
        self._key = kdf.derive(bytes(password, 'utf-8'))
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES128(self._key), modes.CBC(iv))
        self._encryptor = cipher.encryptor()
        self._decryptor = cipher.decryptor()
        super().run_chat()
        return

    def encrypt(self, message) -> None:
        payload = self._encryptor.update(bytes(message, 'utf-8')) + self._encryptor.finalize()
        return payload

    def decrypt(self, payload) -> None:
        message = self._decryptor.update(payload) + self._decryptor.finalize()
        return str(message, 'utf-8')

if __name__ == "__main__":
    client = CipheredGUI()
    client.create()
    client.loop()
