from logging import log, warn
import dearpygui.dearpygui as dpg
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from chat_client import ChatClient
# from generic_callback import GenericCallback
import serpent
from basic_gui import DEFAULT_VALUES, BasicGUI

IV_LENGTH = 16
KEY_LENGTH = 16
KDF_NB_ITERATIONS = 480000
KDF = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = KEY_LENGTH,
        salt = b'oskour',
        iterations = KDF_NB_ITERATIONS
        )


class CipheredGUI(BasicGUI):
    """Encrypted GUI for chat client""" 
    def __init__(self) -> None:
        # Constructor
        super().__init__()
        self._key = b""

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
        self._key = KDF.derive(bytes(password, 'utf-8'))
        super().run_chat(None, None)

    def encrypt(self, message: str):
        iv = os.urandom(IV_LENGTH)
        cipher = Cipher(algorithms.AES128(self._key), modes.CTR(iv))
        encryptor = cipher.encryptor() 
        payload = encryptor.update(bytes(message, 'utf-8')) + encryptor.finalize()
        return (iv, payload)

    def decrypt(self, frame: tuple[bytes, bytes]):
        iv, payload = frame
        cipher = Cipher(algorithms.AES128(self._key), modes.CTR(iv))
        decryptor = cipher.decryptor()
        message = decryptor.update(payload) + decryptor.finalize()
        return str(message, 'utf-8')

    def send(self, message: str) -> None:
        if message != "": print("SEND FUNCTION")
        frame = self.encrypt(message)
        # frame = (serpent.tobytes(frame[0]), serpent.tobytes(frame[1]))
        super().send(frame)

    def recv(self) -> None:
        # function called to get incoming messages and display them
        if self._callback is None:
            return

        for user, frame in self._callback.get():
            print("RECIEVE FUNCTION")
            # print(serpent.loads(frame)) # ERROR
            # print(serpent.tobytes(frame)) # ERROR
            frame_TB = (serpent.tobytes(frame[0]), serpent.tobytes(frame[1]))
            message = self.decrypt(frame_TB)
            self.update_text_screen(f"{user} : {message}")
        self._callback.clear()

        

if __name__ == "__main__":
    client = CipheredGUI()
    client.create()
    client.loop()
