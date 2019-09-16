import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from QTgeneration.MainWindow import Ui_MainWindow
from db_utils.migrate import MyConnection


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting
        self.Ui_MainWindow = Ui_MainWindow()
        self.Ui_MainWindow.setupUi(self)

        # SQL
        self.current_id = -1  # currrent id
        self.my_conn = MyConnection(path='./db_utils/db.db')

        # binding
        self.Ui_MainWindow.pushButton.clicked.connect(self.on_push_button_clicked)
        self.Ui_MainWindow.pushButton_2.clicked.connect(self.on_push_button2_clicked)
        self.Ui_MainWindow.pushButton_3.clicked.connect(self.on_push_button3_clicked)
        self.Ui_MainWindow.listWidget.doubleClicked.connect(self.on_listWidget_double_clicked)
        # call
        self.query_show()

    def query_show(self):
        """
        将所有记录show在listView
        :return:
        """
        self.refresh_record()
        # self.Ui_MainWindow.listWidget.addItem("asdhasjkhf")

    def refresh_record(self, place=None):
        result = self.my_conn.query_records(place)
        self.Ui_MainWindow.listWidget.clear()
        for item in result:
            self.Ui_MainWindow.listWidget.addItem(str(item))

    def on_listWidget_double_clicked(self, e):
        # print("hello pyqt")
        # QtCore.QModelIndex
        _data = eval(e.data())
        self.current_id = _data[0]
        self.Ui_MainWindow.lineEdit.setText(_data[1])
        self.Ui_MainWindow.lineEdit_2.setText(_data[2])
        self.Ui_MainWindow.lineEdit_3.setText(_data[3])

    def on_push_button_clicked(self):
        """
        修改
        :return:
        """
        username = self.Ui_MainWindow.lineEdit.text()
        password = self.Ui_MainWindow.lineEdit_2.text()
        place = self.Ui_MainWindow.lineEdit_3.text()

        self.my_conn.modify_record(username, password, place,self.current_id)
        self.refresh_record()
        print("refresh_record")

    def on_push_button3_clicked(self, place=None):
        """
        查询记录
        :param place:
        :return:
        """
        result = self.my_conn.query_records(place)
        print(result)

    def on_push_button2_clicked(self):
        """
        删除
        :return:
        """


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    # main_window.on_push_button3_clicked()
    main_window.show()
    sys.exit(app.exec_())
