import logging

import dearpygui.dearpygui as dpg

from chat_client import ChatClient
from generic_callback import GenericCallback

from basic_gui import DEFAULT_VALUES, BasicGUI


class CipheredGUI(BasicGUI):
    """Encrypted GUI for chat client""" 
    def __init__(self) -> None:
        # Constructor
        super().__init__()
        self._key = None
    
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



if __name__ == "__main__":
    client = CipheredGUI()
    client.create()
    client.loop()
