from os.path import expanduser
from os import getlogin
from PyQt5.QtWidgets import QFileSystemModel, QApplication, QMainWindow, QTreeView, QVBoxLayout, QLineEdit, QWidget, QPushButton
from PyQt5.QtCore import QDir
from sys import exit, argv


class UserInfo:
    def __init__(self) -> None:
        self.username = None
        self.path = None
    
    # информация о пользователе. путь к его домашней директории и логин 
    def get_cur_user_information(self):
        self.username = getlogin()
        self.path = expanduser('~')


class FileSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user = UserInfo()
        self.user.get_cur_user_information()
        self.initUI()

    # инициализация графического интерфейса
    def initUI(self):

        # параметры окна
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle(f'File System Tree for {self.user.username}')

        # создаем модель данныхх локальной системы
        self.model = QFileSystemModel()
        self.model.setRootPath(self.user.path)

        # создаем древовидное представление модели
        self.treeView = QTreeView(self)
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(self.user.path))
        
        # задаем фильтры
        self.model.setFilter(QDir.Dirs | QDir.Files | QDir.Hidden)
        self.model.setNameFilterDisables(False)

        # создается кнопка и LineEdit и подключение функции поиска файлов
        self.searchLineEdit = QLineEdit(self)
        self.searchButton = QPushButton('Поиск', self)
        self.searchButton.clicked.connect(self.searchFiles)

        # создаем Layout и добавляем в него все виджеты
        layout = QVBoxLayout()
        layout.addWidget(self.searchLineEdit)
        layout.addWidget(self.searchButton)
        layout.addWidget(self.treeView)

        # создаем виджет графического интерфейса
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.treeView.expandAll()

    # функция задающая фильтр поиска по содержимому LineEdit
    def searchFiles(self):

        # открываем все вложенные файлы, берем текст из LineEdit и меняем фильтр
        self.treeView.expandAll()
        search_text = self.searchLineEdit.text()
        self.treeView.setModel(self.model)
        self.model.setNameFilters([f'*{search_text}*'])


if __name__ == '__main__':  

    # создаем обработчик приложения и отображаем наше приложение 
    app = QApplication(argv)
    ex = FileSearchApp()
    ex.show()
    exit(app.exec_())