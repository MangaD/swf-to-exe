import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
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
        self.ui.addSwfBtn.clicked.connect(self.addSwfFile)
        self.setTheme()

    @Slot()
    def about(self):
        QMessageBox.about(self, 'About Swf2Exe', 'Convert your SWF files to EXE files using the Adobe Flash Player Projector.')

    @Slot()
    def addSwfFile(self):
        fileList = self.openFileNamesDialog()
        self.ui.swfList.addItems(fileList)

    def setTheme(self):
        styleFile = QFile(u":/theme/resources/PicPax.qss")
        if styleFile.open(QIODevice.ReadOnly | QIODevice.Text):
            inStream = QTextStream(styleFile)
            _style = inStream.readAll()
            self.setStyleSheet(_style)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Shockwave Flash (*.swf);;All Files (*)", options=options)
        if fileName:
            print(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","Shockwave Flash (*.swf);;All Files (*)", options=options)
        return files

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","EXE Files (*.txt)", options=options)
        if fileName:
            print(fileName)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
