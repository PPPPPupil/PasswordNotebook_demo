import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore
import PyQt5
from PyQt5 import QtWidgets
from QTgeneration.MainWindow import Ui_MainWindow
from QTgeneration.AddWindow import Ui_Form
from db_utils.migrate import MyConnection


class AddWindow(QtWidgets.QWidget):
    """
        mainwindow点击add按钮后，弹出add窗口，用于增加记录
    """

    def __init__(self, father_MainWindow):
        super().__init__()

        # Setting
        self.Ui_Form = Ui_Form()
        self.Ui_Form.setupUi(self)
        self.setWindowTitle('Add record')

        self.father_MainWindow = father_MainWindow

        # SQL
        self.my_conn = MyConnection(path='./db_utils/db.db')

        # binding
        self.Ui_Form.pushButton.clicked.connect(self.on_push_Button_clicked)
        self.Ui_Form.pushButton_2.clicked.connect(self.on_push_Button2_clicked)

    def on_push_Button_clicked(self):
        """
        增加记录，依次传入username，password，place
        :return:
        """
        self.my_conn.add_record(self.Ui_Form.lineEdit.text(), self.Ui_Form.lineEdit_2.text(),
                                self.Ui_Form.lineEdit_3.text())
        self.father_MainWindow.refresh_record()

    def on_push_Button2_clicked(self):
        """
        清空输入
        :return:
        """
        self.Ui_Form.lineEdit.setText(None)
        self.Ui_Form.lineEdit_2.setText(None)
        self.Ui_Form.lineEdit_3.setText(None)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting
        self.Ui_MainWindow = Ui_MainWindow()
        self.Ui_MainWindow.setupUi(self)
        self.add_window = AddWindow(self)  # add window for adding record

        # SQL
        self.current_id = -1  # currrent id
        self.my_conn = MyConnection(path='./db_utils/db.db')

        # binding
        self.Ui_MainWindow.pushButton.clicked.connect(self.on_push_button_clicked)
        self.Ui_MainWindow.pushButton_2.clicked.connect(self.on_push_button2_clicked)
        self.Ui_MainWindow.pushButton_3.clicked.connect(self.on_push_button3_clicked)
        self.Ui_MainWindow.listWidget.doubleClicked.connect(self.on_list_Widget_double_clicked)
        self.Ui_MainWindow.tableWidget.doubleClicked.connect(self.on_table_Widget_double_clicked)
        self.Ui_MainWindow.pushButton_4.clicked.connect(self.on_push_button4_clicked)

        # call
        self.table_widget_init()
        self.show_all()
        self.Ui_MainWindow.lineEdit_4.setPlaceholderText("query all if nothing")

    def table_widget_init(self):
        self.Ui_MainWindow.tableWidget.setColumnCount(4)  # 设置table的列数
        self.Ui_MainWindow.tableWidget.verticalHeader().setSectionsClickable(False)  # 表头不可点击
        self.Ui_MainWindow.tableWidget.setHorizontalHeaderLabels(["id", "username", "password", "place"])  # 表头内容
        # self.Ui_MainWindow.tableWidget.horizontalHeader().setBackgroundRole()
        self.Ui_MainWindow.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 一次选一行
        self.Ui_MainWindow.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


    def show_all(self):
        """
        将所有记录show在listView，在打开主面板的时候调用
        :return:
        """
        self.refresh_record()
        # self.Ui_MainWindow.listWidget.addItem("asdhasjkhf")

    def remove_all_tableW_row(self):
        current_row = self.Ui_MainWindow.tableWidget.rowCount()
        for r in range(0, current_row)[::-1]:  # 倒序是关键
            self.Ui_MainWindow.tableWidget.removeRow(r)

    def refresh_record(self, place=None):
        """
        刷新listView，（可传入条件place）
        :param place:
        :return:
        """
        result = self.my_conn.query_records(place)
        self.Ui_MainWindow.listWidget.clear()
        self.remove_all_tableW_row()
        for item in result:
            self.Ui_MainWindow.listWidget.addItem(str(item))
            # table widget
            current_row = self.Ui_MainWindow.tableWidget.rowCount()
            self.Ui_MainWindow.tableWidget.insertRow(current_row)
            self.Ui_MainWindow.tableWidget.setItem(current_row, 0, QtWidgets.QTableWidgetItem(str(item[0])))
            self.Ui_MainWindow.tableWidget.setItem(current_row, 1, QtWidgets.QTableWidgetItem(item[1]))
            self.Ui_MainWindow.tableWidget.setItem(current_row, 2, QtWidgets.QTableWidgetItem(item[2]))
            self.Ui_MainWindow.tableWidget.setItem(current_row, 3, QtWidgets.QTableWidgetItem(item[3]))

    def on_list_Widget_double_clicked(self, e):
        """
        双击listView事件，读取该条记录的信息，并显示在面板上
        :param e:
        :return:
        """
        # print("hello pyqt")
        # QtCore.QModelIndex
        _data = eval(e.data())
        self.current_id = _data[0]
        self.Ui_MainWindow.lineEdit.setText(_data[1])
        self.Ui_MainWindow.lineEdit_2.setText(_data[2])
        self.Ui_MainWindow.lineEdit_3.setText(_data[3])

    def on_table_Widget_double_clicked(self, e):
        """
        双击listView事件，读取该条记录的信息，并显示在面板上
        :param e:
        :return:
        """

        # print(e.data())  # 点击事件以item为单位（can not row）
        selected_row = e.row()  # 获取当前点击item所在的行数
        # _data = eval(e.data()[1])
        self.current_id = self.Ui_MainWindow.tableWidget.item(selected_row, 0).text()
        self.Ui_MainWindow.lineEdit.setText(self.Ui_MainWindow.tableWidget.item(selected_row, 1).text())
        self.Ui_MainWindow.lineEdit_2.setText(self.Ui_MainWindow.tableWidget.item(selected_row, 2).text())
        self.Ui_MainWindow.lineEdit_3.setText(self.Ui_MainWindow.tableWidget.item(selected_row, 3).text())

    def on_push_button_clicked(self):
        """
        修改当前所显示的信息（先双击，再修改）
        :return:
        """
        username = self.Ui_MainWindow.lineEdit.text()
        password = self.Ui_MainWindow.lineEdit_2.text()
        place = self.Ui_MainWindow.lineEdit_3.text()

        self.my_conn.modify_record(username, password, place, self.current_id)
        self.refresh_record()

    def on_push_button3_clicked(self):
        """
        查询按钮，可传入条件place
        :param place:
        :return:
        """
        place = self.Ui_MainWindow.lineEdit_4.text()

        if place == '':
            self.refresh_record(None)
        else:
            self.refresh_record(place)
        # print(result)

    def on_push_button2_clicked(self):
        """
        删除按钮（先双击，再删除）
        :return:
        """
        self.my_conn.delete_record(self.current_id)
        self.refresh_record()

    def on_push_button4_clicked(self):
        """
        增加新纪录，弹出增加窗口
        :return:
        """

        self.add_window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    # add_window = AddWindow()
    # add_window.show()
    # main_window.on_push_button3_clicked()
    main_window.show()
    sys.exit(app.exec_())
