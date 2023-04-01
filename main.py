import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar
from cryptography.fernet import Fernet

# Função para obter ou gerar a chave de criptografia
def obter_chave():
    try:
        with open('chave.key', 'rb') as arquivo_chave:
            return arquivo_chave.read()
    except FileNotFoundError:
        nova_chave = Fernet.generate_key()
        with open('chave.key', 'wb') as arquivo_chave:
            arquivo_chave.write(nova_chave)
        return nova_chave

# Obter a chave de criptografia
chave = obter_chave()
cipher_suite = Fernet(chave)

# Classe principal do aplicativo
class Encryptor(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    # Inicialização da interface do usuário
    def init_ui(self):
        self.setWindowTitle('Encryptor')

        layout = QVBoxLayout()

        # Criação dos elementos da interface do usuário
        self.lbl_info = QLabel('Selecione um arquivo para criptografar ou descriptografar:')
        self.btn_select = QPushButton('Selecionar Arquivo')
        self.btn_select.clicked.connect(self.select_file)
        self.btn_select.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border: 1px solid black;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 gray, stop: 1 light);
            }
        """)

        self.btn_encrypt = QPushButton('Criptografar')
        self.btn_encrypt.clicked.connect(self.encrypt_file)
        self.btn_encrypt.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: 1px solid black;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 orange, stop: 1 #bf6300);
            }
        """)

        self.btn_decrypt = QPushButton('Descriptografar')
        self.btn_decrypt.clicked.connect(self.decrypt_file)
        self.btn_decrypt.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: white;
                border: 1px solid black;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6aff6e, stop: 1 #00bf00);
            }
        """)

        self.progress_bar = QProgressBar()

        # Adicionando elementos da interface do usuário ao layout
        layout.addWidget(self.lbl_info)
        layout.addWidget(self.btn_select)
        layout.addSpacing(1)
        layout.addWidget(self.btn_encrypt)
        layout.addSpacing(1)
        layout.addWidget(self.btn_decrypt)
        layout.addSpacing(1)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    # Função para selecionar o arquivo a ser criptografado ou descriptografado
    def select_file(self):
        self.progress_bar.setValue(0)
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Selecione um arquivo", "", "Todos os Arquivos (*)", options=options)

    # Função para criptografar o arquivo selecionado
    def encrypt_file(self):
        
        if self.file_name:
            extension = ".encrypted"
            with open(self.file_name, 'rb') as file:
                file_data = file.read()

            encrypted_data = cipher_suite.encrypt(file_data)

            # Adiciona a extensão ao nome do arquivo
            output_filename = self.file_name + extension

            with open(output_filename, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)

            os.remove(self.file_name)
            self.progress_bar.setValue(100)
            

    # Função para descriptografar o arquivo selecionado
    def decrypt_file(self):
        if self.file_name:
            extension = ".encrypted"
            self.progress_bar.setValue(0)

            # Verifica se o arquivo tem a extensão
            if self.file_name.endswith(extension):
                output_filename = self.file_name[:-len(extension)]
            else:
                output_filename = self.file_name + "_decrypted"

            try:
                with open(self.file_name, 'rb') as file:
                    file_data = file.read()

                decrypted_data = cipher_suite.decrypt(file_data)

                with open(output_filename, 'wb') as decrypted_file:
                    decrypted_file.write(decrypted_data)
                
                if self.file_name.endswith(extension):
                    output_filename = self.file_name[:-len(extension)]
                    os.remove(self.file_name)

                self.progress_bar.setValue(100)

                

            except Exception as e:
                self.progress_bar.setValue(0)
                print("Erro ao descriptografar:", e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    encryptor = Encryptor()
    encryptor.show()
    encryptor.setFixedSize(250, 180)
    sys.exit(app.exec_())
