from PyQt6.QtWidgets import QApplication
from frontend.ventanas import MainWindow
from backend.cliente import Cliente
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        mainwindow = MainWindow()
        cliente = Cliente(int(sys.argv[1]))
        cliente.senal_a_ventana.connect(mainwindow.manejar_mensaje)
        mainwindow.senal_a_cliente.connect(cliente.manejar_mensaje)
    except IndexError:
        print("Debe ingresar un puerto de servidor")
        sys.exit()
    except ValueError:
        print("Debe ingresar un puerto de servidor válido")
        sys.exit()
    sys.exit(app.exec())
