import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PySide6.QtCore import (
    Slot, QFile, QIODevice,
    QTextStream, QCoreApplication,
    QSettings, QDir
)

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


    def setTheme(self):
        styleFile = QFile(u":/theme/resources/PicPax.qss")
        if styleFile.open(QIODevice.ReadOnly | QIODevice.Text):
            inStream = QTextStream(styleFile)
            _style = inStream.readAll()
            self.setStyleSheet(_style)

    @Slot()
    def about(self):
        QMessageBox.about(self, 'About Swf2Exe', 'Convert your SWF files to EXE files using the Adobe Flash Player Projector.')

    @Slot()
    def addSwfFile(self):
        fileList = self.openFileNamesDialog()
        self.ui.swfList.addItems(fileList)

    def openFileNamesDialog(self):
        DEFAULT_DIR_KEY = "default_dir"
        settings = QSettings()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,
            "Select file(s)",
            settings.value(DEFAULT_DIR_KEY),
            "Shockwave Flash (*.swf);;All Files (*)",
            options=options)
        if files:
            currentDir = QDir()
            settings.setValue(DEFAULT_DIR_KEY, currentDir.absoluteFilePath(files[-1]));
        return files

# Set up info for using with QSettings
# https://stackoverflow.com/a/3598245/3049315
# https://srinikom.github.io/pyside-docs/PySide/QtCore/QSettings.html
def setAppInfo() -> None:
    QCoreApplication.setApplicationName("Swf2Exe")
    QCoreApplication.setApplicationVersion("1.0.0.0")
    QCoreApplication.setOrganizationName("swf2exe")
    QCoreApplication.setOrganizationDomain("mangad.github.io/swf2exe")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    setAppInfo()
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
