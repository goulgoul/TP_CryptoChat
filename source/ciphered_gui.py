import dearpygui.dearpygui as dpg
import os
import serpent
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from basic_gui import DEFAULT_VALUES, BasicGUI

"""
Here are some global variable definitions:
"""
 
"""@var IV_LENGTH The length of the IV of our encryption in bytes"""
IV_LENGTH = 16

"""@var KEY_LENGTH The length of the cryptographic key in bytes."""
KEY_LENGTH = 16

"""@var KDF_NB_ITERATIONS The number of iterations during which the KDF will run"""
KDF_NB_ITERATIONS = 480000

"""
@var KDF The key derivation function used to creae the private key for the encrypt phase.
@param algorithm The chosen hashing algorithm, namely SHA256.
@param salt Has been set to a constant, but it is usually random
@param iterations The number of iterations of the kdf loop
"""
KDF = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = KEY_LENGTH,
        salt = b'oskour',
        iterations = KDF_NB_ITERATIONS
        )

"""
@class CipheredGUI 
@brief A class that extends the BasicGUI class by adding a cryptography layer on top of the messaging functionality. The encrypting is done with the help of AES128 and PBKDF2HMAC key derivation function.
@extends BasicGUI
""" 
class CipheredGUI(BasicGUI):
    """
    @fn __init__()
    @brief The initialisation functionality

    Initialises the mother BasicGUI and sets two member variables to a zero-value.
    """
    def __init__(self) -> None:
        # Constructor
        super().__init__()
        """The encryption key"""
        self._key = b""
        """The password set by users to encrypt their communication"""
        self._password = ""

    """
    @fn _create_connection_window()
    @brief A method copied from BasicGUI's window creation function; it adds a label and an input field reserved for user password input.
    """
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
    """
    @fn run_chat()
    @brief A function called as the user submits their connection information; this is where the module gets the password and derives the key based on it. 
    All other functionalities having been written as part of BasicGUI's run_chat function, the latter is simply called before return.
    """
    def run_chat(self) -> None:
        self._password = dpg.get_value("connection_password")
        self._key = KDF.derive(bytes(self._password, 'utf-8'))
        super().run_chat(None, None)

    """
    @fn encrypt()
    @brief A function for message encryption
    @param message A string containing the message the user wants to send through the server without it being read by admins
    """
    def encrypt(self, message: str) -> tuple[bytes, bytes]:
        iv = os.urandom(IV_LENGTH)
        cipher = Cipher(algorithms.AES128(self._key), modes.CTR(iv))
        encryptor = cipher.encryptor() 
        payload = encryptor.update(bytes(message, 'utf-8')) + encryptor.finalize()
        return (iv, payload)
    
    """@fn decrypt()
    @brief A function for message decryption
    @param frame A tuple containing an encrypted message and an IV to help decrypt it
    """
    def decrypt(self, frame: tuple[bytes, bytes]) -> str:
        iv, payload = frame
        cipher = Cipher(algorithms.AES128(self._key), modes.CTR(iv))
        decryptor = cipher.decryptor()
        message = decryptor.update(payload) + decryptor.finalize()
        return str(message, 'utf-8')
    
    """
    @fn send()
    @brief A function that sends messages from the GUI to the server; it requires the encrypt function to send encrypted messages.
    @param message The string input by the user, that has to be transmitted to the receiver
    """
    def send(self, message: str) -> None:
        frame = self.encrypt(message)
        super().send(frame)
    
    """@fn recv()
    @brief A function run periodically by the chat client class; it allows messages to be received, whatever their nature.
    This function does not require any parameter, but the input messages have to be of the same type as those sent by send().
    """
    def recv(self) -> None:
        if self._callback is None:
            return

        for user, frame in self._callback.get():
            frame_TB = (serpent.tobytes(frame[0]), serpent.tobytes(frame[1]))
            message = self.decrypt(frame_TB)
            self.update_text_screen(f"{user} : {message}")
        self._callback.clear()

        

if __name__ == "__main__":
    client = CipheredGUI()
    client.create()
    client.loop()
