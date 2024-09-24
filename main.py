from PySide6.QtWidgets import QApplication, QDialog, QPushButton
import sys
from MainPage import MyMainPage

app = QApplication(sys.argv)

window = MyMainPage()
window.show()
app.exec()