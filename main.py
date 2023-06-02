import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Slot, QFile, QIODevice, QTextStream

from forms.ui_form import Ui_MainWindow

import rc_PicPax

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionExit.triggered.connect(lambda self_ : sys.exit())
        self.ui.actionAbout.triggered.connect(self.about)
        self.setTheme()

    @Slot()
    def about(self):
        QMessageBox.about(self, 'About Swf2Exe', 'Convert your SWF files to EXE files using the Adobe Flash Player Projector.')

    def setTheme(self):
        styleFile = QFile(u":/theme/resources/PicPax.qss")
        if styleFile.open(QIODevice.ReadOnly | QIODevice.Text):
            inStream = QTextStream(styleFile)
            _style = inStream.readAll()
            self.setStyleSheet(_style)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
