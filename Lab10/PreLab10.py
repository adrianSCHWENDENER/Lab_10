import serial
from PySide2.QtCore import QObject, QThread, Signal
from PySide2.QtWidgets import QApplication, QMainWindow
from InterfazP import Ui_MainWindow

class SerialThread(QObject):
    data_received = Signal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.serial_port = serial.Serial(port, baudrate)

    def run(self):
        while True:
            if self.serial_port.in_waiting > 0:
                data = self.serial_port.readline().decode().rstrip()
                self.data_received.emit(data)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Enviar.clicked.connect(self.mostrar_texto)

        self.serial_thread = QThread()
        self.serial_worker = SerialThread('COM3', 9600)  # Cambia 'COM3' al puerto serial que estés usando
        self.serial_thread.started.connect(self.serial_worker.run)
        self.serial_worker.data_received.connect(self.mostrar_datos)
        self.serial_worker.moveToThread(self.serial_thread)
        self.serial_thread.start()

    def mostrar_texto(self):
        texto = self.ui.Numero.text()
        print(texto)
        self.serial_worker.serial_port.write(texto.encode())

    def mostrar_datos(self, data):
        self.ui.textBrowser.append(data)

if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec_()
