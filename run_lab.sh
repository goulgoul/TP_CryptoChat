#!/bin/bash
read -p "Choose between BasicGUI(1), CipheredGUI(2) and FernetGUI (3, default):" -N 1 choix_fichier

case choix_fichier in
  1)
    xterm -hold -e "source .venv/bin/activate && python3 src/basic_gui.py" & 
    xterm -hold -e "source .venv/bin/activate && python3 src/basic_gui.py" & 
    ;;
    
  2)
    xterm -hold -e "source .venv/bin/activate && python3 src/ciphered_gui.py" & 
    xterm -hold -e "source .venv/bin/activate && python3 src/ciphered_gui.py" & 
    ;;

  *)
    xterm -hold -e "source .venv/bin/activate && python3 src/fernet_gui.py" & 
    xterm -hold -e "source .venv/bin/activate && python3 src/fernet_gui.py" & 
    ;;
esac

xterm -hold -e "source .venv/bin/activate && python3 src/chat_server.py" &
