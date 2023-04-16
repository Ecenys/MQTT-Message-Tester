import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import zipfile
import importlib.util
import json

class TestApp(QMainWindow):
    def __init__(self):
        super(TestApp, self).__init__()
        loadUi("mainWindow.ui", self) # Cargar la interfaz desde el archivo mainWindow.ui
        self.folderButton.clicked.connect(self.select_folder)
        self.zipListWidget.itemClicked.connect(self.show_Test_Resume)
        self.startButton.clicked.connect(self.start_test)
        
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
            print(f"Leyendo process de {zip_path}...")
            self.traceTextEdit.insertPlainText(f"Leyendo process de {zip_path}...\n")
            zip_file.extract("process.py")

        # Cargar el módulo process.py
        spec = importlib.util.spec_from_file_location("process", "process.py")
        process_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(process_module)

        # Obtener los pasos del proceso de prueba
        description = getattr(process_module, "description", "")
        steps = process_module.steps

        return description, steps
        
    def start_test(self):
        selected_item = self.zipListWidget.currentItem()
        if selected_item:
            zip_file = selected_item.text()
            zip_path = os.path.join(self.folderLineEdit.text(), zip_file)
            self.traceTextEdit.insertPlainText(f"Iniciando prueba: {zip_file}\n")
            # Lógica para iniciar la prueba con el archivo process.py
            # ... (Aquí se debe implementar la lógica para realizar la prueba con el archivo process.py y actualizar las trazas en el cuadro de texto traceTextEdit)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec_())
