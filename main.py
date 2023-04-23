import sys
import os
import zipfile
import importlib.util
import suscriber
import shutil
import time
import threading
import atexit

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from testStatus import CompletedTest, FailedTest

class TestApp(QMainWindow):
    noReadFiles = []
    mqtt_messages = {}

    def __init__(self):
        super(TestApp, self).__init__()

        # Función que se ejecuta al cerrar la aplicación
        atexit.register(self.exit_handler)

        # crear la instancia a la clase de suscriber que se encuentra en el mismo directorio que main.py
        self.suscriber = suscriber.Suscriber()
        self.suscriber.consoleLog = self.consoleLog
        # para usar el consoleLog en suscriber.py
        self.suscriber.consoleLog = self.consoleLog

        loadUi("mainWindow.ui", self) # Cargar la interfaz desde el archivo mainWindow.ui
        self.connectButton.clicked.connect(self.connect_with_broker)
        self.folderButton.clicked.connect(self.select_folder)
        self.zipListWidget.itemClicked.connect(self.show_Test_Resume)
        self.startButton.clicked.connect(self.run_test_thread)

    # Función que se ejecuta al cerrar la aplicación
    def exit_handler(self):
        # Borrar el directorio temporal
        shutil.rmtree("temp", ignore_errors=True)

    # Función que se ejecuta al presionar el botón de conectar con el broker
    def connect_with_broker(self):
        self.clear()
        # Imprime en consola que se esta conetaando con el broker
        self.consoleLog("Conectando con el broker...")
        # Conecta con el broker
        #si puerto no esta vacio
        if self.brokerPortLineEdit.text() != "":
            result = self.suscriber.checkBrokerAddress(self.brokerAddressLineEdit.text(), int(self.brokerPortLineEdit.text()))
        else:
            result = self.suscriber.checkBrokerAddress(self.brokerAddressLineEdit.text())
        # si se ha podido conectar con el broker
        if result:
            #imprime en consola que se ha conectado con el broker
            self.consoleLog("Conectado con el broker")
            #activa el boton de seleccionar carpeta
            self.folderButton.setEnabled(True)
            
        else:
            #imprime en consola que no se ha podido conectar con el broker 
            self.consoleLog("No se ha podido conectar con el broker")

    # Función que limpia la interfaz
    def clear(self):
        self.folderButton.setEnabled(False)
        self.zipListWidget.setEnabled(False)
        self.folderLineEdit.setText("")
        self.zipListWidget.clear()
        self.traceTextEdit.clear()

    # Función que muestra información en la consola y en la interfaz
    def consoleLog(self, toPrint):
        print(str(toPrint) + "\n")
        self.traceTextEdit.insertPlainText(str(toPrint) + "\n")

    # Función que se ejecuta al presionar el botón de seleccionar carpeta
    def select_folder(self):
        # Abrir diálogo para seleccionar carpeta
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta") 
        folder_path_without_extension = os.path.splitext(folder_path)[0]
        self.folderLineEdit.setText(folder_path_without_extension)
        self.load_zip_files(folder_path)
        
    # Función que carga los archivos .zip de la carpeta seleccionada
    def load_zip_files(self, folder_path):
        self.zipListWidget.clear()
        zip_files = []
        try:
            zip_files = [f for f in os.listdir(folder_path) if f.endswith('.zip')] # Obtener archivos .zip del directorio
        except Exception as e:
            self.consoleLog("Error al leer archivos .zip:", e)
        self.zipListWidget.addItems(zip_files)
        if zip_files:
            self.zipListWidget.setEnabled(True)
        else:
            self.zipListWidget.setEnabled(False)
            self.startButton.setEnabled(False)
        
    # Función que se ejecuta al preisonar un elemento de la lista de archivos .zip
    def show_Test_Resume(self, item):
        description = ""
        testResume = ""
        zip_file = item.text()
        zip_path = os.path.join(self.folderLineEdit.text(), zip_file)
        description, stepsList = self.read_zip_data(zip_path)
        if not description:
            description = ""
        else:
            testResume = description + "\n"
        for step in stepsList:
            for key, value in step.items():
                if key == "name":
                    testResume += f"\n{value}"
                elif key == "description":
                    testResume += f": {value}"            
        
        self.startButton.setEnabled(True)
        self.stepTextEdit.setPlainText(testResume)
        
    # Función que lee los datos de un archivo .zip
    def read_zip_data(self, zip_path):
        # Abrir el archivo ZIP
        with zipfile.ZipFile(zip_path, "r") as zip_file:
            # Extraer el archivo process.py del ZIP
            self.consoleLog(f"Leyendo process de {zip_path}...")
            zip_file.extract("process.py", ".\\temp")

        # Cargar el módulo process.py
        self.process_module = None
        try:
            spec = importlib.util.spec_from_file_location("process", "process.py")
            self.process_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.process_module)
            self.process_module.mmt = self
            self.process_module.suscriber = self.suscriber
            self.process_module.FailedTest = FailedTest
            self.process_module.CompletedTest = CompletedTest
        except Exception as e:
            self.consoleLog("Error al cargar el módulo process.py:", e)
            return "", []
        
        # Obtener los pasos del proceso de prueba
        description = getattr(self.process_module, "description", "")
        steps = self.process_module.steps

        return description, steps
        
    def readFiles(self, zip_path):
        # (Agregar aquí la lógica específica para leer y procesar los archivos)
        self.consoleLog(f"Leyendo posibles archivos desde {zip_path}...")
        i = 0
        with zipfile.ZipFile(zip_path, "r") as zip_file:
            for file in zip_file.namelist():
                if (not any(file.endswith(extension) for extension in self.noReadFiles)) and (not file.endswith(".py")):
                    zip_file.extract(file, ".\\temp")
                    with open(".\\temp\\" + file, "r") as f:
                        self.mqtt_messages[i] = f.read()
                        i += 1

    # Función que ejecuta los pasos del proceso de prueba
    def runStepX(self, steps):
        step = 1
        if steps > 0:
            while step <= steps:
                # Construye el nombre del método dinámicamente
                method_name = "step" + str(step)
                # Verifica si el método existe en la clase Process
                if hasattr(self.process_module, method_name):
                    # Llama al método
                    method = getattr(self.process_module, method_name)
                    try:
                        method(self.process_module)
                        self.consoleLog("El test esta en proceso")
                    except FailedTest as e:
                        self.consoleLog(f"El test {step} ha fallado.")
                        break
                        # Realizar acciones específicas para el estado failed
                    except CompletedTest as e:
                        self.consoleLog(f"El test {step} ha sido completado.")
                        step += 1
                        # Realizar acciones específicas para el estado completado
                            
                    time.sleep(1)
                else:
                    self.consoleLog(f"El método {method_name} no existe")
                    break
        else:
            self.consoleLog("No se han definido pasos")

    # Función que se ejecuta al presionar el botón de iniciar prueba
    def run_test(self):
        selected_item = self.zipListWidget.currentItem()
        if selected_item:
            self.suscriber.client.loop_start()

            # Lógica para llamar al metodo awake
            self.consoleLog(f"Buscando metodo awake")
            try:
                self.process_module.awake(self.process_module)
            except AttributeError:
                pass

            zip_file = selected_item.text()
            zip_path = os.path.join(self.folderLineEdit.text(), zip_file)
            # Lógica para leer los archivos del ZIP
            self.readFiles(zip_path)

            # Lógica para iniciar la prueba con el archivo process.py
        
            self.consoleLog(f"Iniciando prueba: {zip_file}")
            self.consoleLog(f"Buscando metodo run")
            self.process_module.run(self.process_module)

            self.consoleLog(f"Empezando pasos")
            self.runStepX(len(self.process_module.steps))
            
            #   Lógica para llamar al metodo late
            self.consoleLog(f"Buscando metodo late")
            try:
                self.process_module.late(self.process_module)
            except AttributeError:
                pass

            zip_file_without_extension = os.path.splitext(zip_file)[0]
            self.consoleLog(f"Prueba finalizada: {zip_file_without_extension}")

            # Borrar archivos temporales
            self.delete_temp_files()
            # Desconecta el cliente mqtt
            self.suscriber.client.loop_stop()

    # Metodo que lanza run_test en un hilo para evitar el bloqueo de la interfaz
    def run_test_thread(self):
        self.run_test_thread = threading.Thread(target=self.run_test)
        self.run_test_thread.start()

    # Funcion para borrar los archivos temporales
    def delete_temp_files(self):
        try:
            shutil.rmtree(".\\temp")
        except Exception as e:
            self.consoleLog("Error al borrar archivos temporales:", e)


    # Evento para conectar al broker cuando se presiona el botón Enter
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.brokerAddressLineEdit.hasFocus() or self.brokerPortLineEdit.hasFocus():
                self.connectButton.click()
    
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec_())
