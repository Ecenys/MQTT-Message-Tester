import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import zipfile
import importlib.util
import json
import suscriber

class TestApp(QMainWindow):
    def __init__(self):
        super(TestApp, self).__init__()

        # crear la instancia a la clase de suscriber que se encuentra en el mismo directorio que main.py
        self.suscriber = suscriber.Suscriber()
        # para usar el consoleLog en suscriber.py
        self.suscriber.consoleLog = self.consoleLog

        loadUi("mainWindow.ui", self) # Cargar la interfaz desde el archivo mainWindow.ui
        self.connectButton.clicked.connect(self.connect_with_broker)
        self.folderButton.clicked.connect(self.select_folder)
        self.zipListWidget.itemClicked.connect(self.show_Test_Resume)
        self.startButton.clicked.connect(self.start_test)

    def connect_with_broker(self):
        # Imprime en consola que se esta conetaando con el broker
        self.consoleLog("Conectando con el broker...\n")
        # Conecta con el broker
        result = self.suscriber.checkBrokerAddress(self.brokerAddressLineEdit.text())
        # si se ha podido conectar con el broker
        if result:
            #imprime en consola que se ha conectado con el broker
            self.consoleLog("Conectado con el broker\n")
            #activa el boton de seleccionar carpeta
            self.folderButton.setEnabled(True)
            
        else:
            #imprime en consola que no se ha podido conectar con el broker y se limpian los campos
            self.folderButton.setEnabled(False)
            self.zipListWidget.setEnabled(False)
            self.folderLineEdit.setText("")
            self.zipListWidget.clear()
            self.consoleLog("No se ha podido conectar con el broker\n")

    def consoleLog(self, string):
        print(string)
        self.traceTextEdit.insertPlainText(string)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta") # Abrir diálogo para seleccionar carpeta
        self.folderLineEdit.setText(folder_path)
        self.load_zip_files(folder_path)
        
    def load_zip_files(self, folder_path):
        self.zipListWidget.clear()
        zip_files = []
        try:
            zip_files = [f for f in os.listdir(folder_path) if f.endswith('.zip')] # Obtener archivos .zip del directorio
        except Exception as e:
            print("Error al leer archivos .zip:", e)
        self.zipListWidget.addItems(zip_files)
        if zip_files:
            self.zipListWidget.setEnabled(True)
            self.startButton.setEnabled(True)
        else:
            self.zipListWidget.setEnabled(False)
            self.startButton.setEnabled(False)
        
    def show_Test_Resume(self, item):
        description = ""
        testResume = ""
        zip_file = item.text()
        zip_path = os.path.join(self.folderLineEdit.text(), zip_file)
        description, stepsList = self.read_zip_data(zip_path)
        if not description:
            description = ""
        else:
            testResume = description
        for step in stepsList:
            for key, value in step.items():
                if key == "name":
                    testResume += f"\n{value}"
                elif key == "description":
                    testResume += f": {value}"            
        
        self.stepTextEdit.setPlainText(testResume)
        
    def read_zip_data(self, zip_path):
        # Abrir el archivo ZIP
        with zipfile.ZipFile(zip_path, "r") as zip_file:
            # Extraer el archivo process.py del ZIP
            self.consoleLog(f"Leyendo process de {zip_path}...\n")
            zip_file.extract("process.py")

        # Cargar el módulo process.py
        self.process_module = None
        try:
            spec = importlib.util.spec_from_file_location("process", "process.py")
            self.process_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.process_module)
        except Exception as e:
            print("Error al cargar el módulo process.py:", e)
            return "", []
        
        # Paso la instancia de la clase TestApp al modulo process.py
        self.process_module.app = self
        
        # Obtener los pasos del proceso de prueba
        description = getattr(self.process_module, "description", "")
        steps = self.process_module.steps

        return description, steps
        
    def start_test(self):
        selected_item = self.zipListWidget.currentItem()
        if selected_item:
            zip_file = selected_item.text()
            zip_path = os.path.join(self.folderLineEdit.text(), zip_file)
            self.consoleLog(f"Iniciando prueba: {zip_file}\n")
            # Lógica para iniciar la prueba con el archivo process.py
            self.process_module.run()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec_())
