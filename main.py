import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import zipfile
import json

class TestApp(QMainWindow):
    def __init__(self):
        super(TestApp, self).__init__()
        loadUi("mainWindow.ui", self) # Cargar la interfaz desde el archivo mainWindow.ui
        self.folderButton.clicked.connect(self.select_folder)
        self.zipListWidget.itemClicked.connect(self.show_steps)
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
        
    def show_steps(self, item):
        zip_file = item.text()
        zip_path = os.path.join(self.folderLineEdit.text(), zip_file)
        steps = self.read_zip_steps(zip_path)
        self.stepTextEdit.setPlainText(steps)
        
    def read_zip_steps(self, zip_path):
        steps = ""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_name in zip_ref.namelist():
                    if file_name.endswith('.json') or file_name.endswith('.cbor'): # Leer archivos .json o .cbor
                        with zip_ref.open(file_name) as file:
                            data = file.read()
                            # Decodificar archivo y obtener información de los pasos del test
                            # (asumiendo que los archivos contienen un diccionario con la información de los pasos)
                            step_data = json.loads(data)
                            steps += f"Nombre: {step_data['nombre']}\n"
                            steps += f"Pasos: {step_data['pasos']}\n\n"
        except Exception as e:
            print("Error al leer archivos del zip:", e)
        return steps
        
    def start_test(self):
        selected_item = self.zipListWidget.currentItem()
        if selected_item:
            zip_file = selected_item.text()
            zip_path = os.path.join(self.folderLineEdit.text(), zip_file)
            self.traceTextEdit.clear()
            self.traceTextEdit.appendPlainText(f"Iniciando prueba: {zip_file}")
            # Lógica para iniciar la prueba con el archivo process.py
            # ... (Aquí se debe implementar la lógica para realizar la prueba con el archivo process.py y actualizar las trazas en el cuadro de texto traceTextEdit)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec_())
