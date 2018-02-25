

from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget
class Add(object):
    def __init__(self,Widget):
        super(Add, self).__init__()
        self.Widget = Widget
    def add(self):
        for i in range(0, 20):
            QTableWidget.rowCount()
            self.Widget.insertRow(self.Widget.rowCount())
            for j in range(0, 3):
                self.Widget.setItem(i, j, QTableWidgetItem('hello'))