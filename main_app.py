from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import sys
import os
from interface import Ui_MainWindow
from param import Ui_Dialog
import bd


def excepthook(type, value, traceback):
    sys.__excepthook__(type, value, traceback)  # Вызываем стандартный обработчик
    # Добавьте здесь свой код для обработки ошибок
    print("An error occurred:", value)

sys.excepthook = excepthook


def update(table):
    col_names = ["Цвет", "Размер", "Количество", "Обрезки"]
    rows = bd.count_rows('base.db')
    table.setColumnCount(len(col_names))
    table.setRowCount(rows)
    table.setHorizontalHeaderLabels(col_names)

    for row in range(rows):
        for column in range(len(col_names)):
            info = bd.import_table('base.db')
            item = QtWidgets.QTableWidgetItem(f'{info[row][column + 1]}')
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            table.setItem(row, column, item)


class CustomDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.get_numbers)
        self.task = None

    def error_check(self, func):
        if func is not None:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"{func}")
        else:
            self.close()

    def get_numbers(self):
        color = self.lineEdit.text()
        size = self.lineEdit_2.text()
        quantity = self.lineEdit_3.text()
        if color and size and quantity:
            if self.task == "add":
                try:
                    func = bd.add_sheet("base.db", int(color), size, int(quantity))
                    self.error_check(func)
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите RAL и количество цифрами")
            elif self.task == "delete":
                try:
                    func = bd.delete_sheet("base.db", int(color), size, int(quantity))
                    self.error_check(func)
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите RAL и количество цифрами")
            else:
                QtWidgets.QMessageBox.warning(self, "Ты чё еблан?", "Ты как эту ошибку получил?")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Заполните все поля")


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        update(self.tableWidget)

        self.pushButton_addMany.clicked.connect(self.pushButton_addMany_clicked)
        self.pushButton_deleteMany.clicked.connect(self.pushButton_deleteMany_clicked)
        #self.pushButton_update.clicked.connect(self.pushButton_update_clicked)
        self.pushButton_deleteInfo.clicked.connect(self.pushButton_deleteInfo_clicked)
        self.pushButton_add1.clicked.connect(self.pushButton_add1_clicked)
        self.pushButton_delete1.clicked.connect(self.pushButton_delete1_clicked)
        self.pushButton_cut.clicked.connect(self.pushButton_cut_clicked)

    def pushButton_addMany_clicked(self):
        dialog = CustomDialog()
        dialog.task = "add"
        dialog.exec_()
        update(self.tableWidget)

    def pushButton_deleteMany_clicked(self):
        dialog = CustomDialog()
        dialog.task = "delete"
        dialog.exec_()
        update(self.tableWidget)

    #def pushButton_update_clicked(self):
        #update(self.tableWidget)


    def index_selection(self):
        select_index = self.tableWidget.selectedItems()
        if select_index:
            row = select_index[0].row()
            color = int(self.tableWidget.item(row, 0).text())
            size = self.tableWidget.item(row, 1).text()
            return color, size
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Ни одна ячейка не выбрана")
            return None

    def error_check(self, func):
        if func is not None:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"{func}")
        else:
            update(self.tableWidget)

    def pushButton_deleteInfo_clicked(self):
        parameters = self.index_selection()
        if parameters is None:
            return
        else:
            accept = QtWidgets.QMessageBox()
            accept.setWindowTitle("Вы уверены?")
            accept.setText("Удалить выделенную запись?")
            accept.setIcon(QtWidgets.QMessageBox.Question)
            accept.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            accept.setDefaultButton(QtWidgets.QMessageBox.No)
            accept.exec_()
            clicked_button = accept.clickedButton()
            if clicked_button == accept.button(QtWidgets.QMessageBox.Yes):
                func = bd.delete_info("base.db", parameters[0], parameters[1])
                self.error_check(func)

    def pushButton_add1_clicked(self):
        parameters = self.index_selection()
        func = bd.add_sheet("base.db", parameters[0], parameters[1], 1)
        self.error_check(func)

    def pushButton_delete1_clicked(self):
        parameters = self.index_selection()
        func = bd.delete_sheet("base.db", parameters[0], parameters[1], 1)
        self.error_check(func)

    def pushButton_cut_clicked(self):
        parameters = self.index_selection()
        func = bd.cut_sheet("base.db", parameters[0], parameters[1], 1)
        self.error_check(func)


if __name__ == "__main__":
    bd_name = "base.db"
    if not os.path.isfile(f"{bd_name}"):
        bd.create_database(bd_name)
    app = QtWidgets.QApplication(sys.argv)
    main_window = Window()
    main_window.show()
    sys.exit(app.exec_())

