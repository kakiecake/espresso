import sqlite3
from typing import List, Tuple
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sys
from pathlib import Path


UI_FILENAME = Path('./main.ui')
DB_FILENAME = Path('./coffee.sqlite')


class SqliteStorage:
    def __init__(self, filename: Path):
        self._connection = sqlite3.connect(filename)
        self._cursor = self._connection.cursor()

    def get_coffee_info(self) -> List[Tuple]:
        sql = 'select * from coffee'
        data = self._cursor.execute(sql).fetchall()
        return data


class MainWindow(QMainWindow):
    def __init__(self, storage: SqliteStorage):
        super().__init__()
        uic.loadUi(UI_FILENAME, self)
        self.storage = storage
        self.fill_table()

    def fill_table(self):
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'прожарка', "вкус", "цена", "объем", "тип"])
        data = self.storage.get_coffee_info()
        for i, coffee_info in enumerate(data):
            rows = self.table.rowCount()
            self.table.setRowCount(rows + 1)
            for j, elem in enumerate(coffee_info):
                item = QTableWidgetItem(str(elem))
                self.table.setItem(i, j, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    storage = SqliteStorage(DB_FILENAME)
    window = MainWindow(storage)
    window.show()
    sys.exit(app.exec_())
