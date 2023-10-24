#!/bin/bash
read -p "Choose between BasicGUI(1), CipheredGUI(2), FernetGUI (3) and TimeFernetGUI (4, default):" -N 1 choix_fichier

case choix_fichier in
  1)
    xterm -hold -e "source .venv/bin/activate && python3 src/basic_gui.py" & 
    xterm -hold -e "source .venv/bin/activate && python3 src/basic_gui.py" & 
    ;;
    
  2)
    xterm -hold -e "source .venv/bin/activate && python3 src/ciphered_gui.py" & 
    xterm -hold -e "source .venv/bin/activate && python3 src/ciphered_gui.py" & 
    ;;
  3)
    xterm -hold -e "source .venv/bin/activate && python3 src/fernet_gui.py" &
    xterm -hold -e "source .venv/bin/activate && python3 src/fernet_gui.py" & 
    ;;
  *)
    xterm -hold -e "source .venv/bin/activate && python3 src/time_fernet_gui.py" &
    xterm -hold -e "source .venv/bin/activate && python3 src/time_fernet_gui.py" & 
    ;;

esac

xterm -hold -e "source .venv/bin/activate && python3 src/chat_server.py" &
