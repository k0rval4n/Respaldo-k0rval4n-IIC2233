from servidor import Servidor
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    servidor = Servidor(sys.argv[1])
    esp = '-' * 57
    input(f"|{esp: ^21.21}|{esp: ^28.28}|{esp: ^57.57}|\n")
    sys.exit()
