import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PySide6.QtCore import (
    Slot, QFile, QIODevice,
    QTextStream, QCoreApplication,
    QSettings, QDir, QEvent
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
        self.ui.addSwfBtn.clicked.connect(self.addSwfFiles)
        self.ui.removeSwfBtn.clicked.connect(self.removeSwfFiles)
        self.ui.saFileBtn.clicked.connect(self.addSAFile)

        # https://stackoverflow.com/a/38860594/3049315
        self.ui.swfList.installEventFilter(self)

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
    def addSwfFiles(self):
        fileList = self.openSwfFileNamesDialog()
        self.ui.swfList.addItems(fileList)

    @Slot()
    def removeSwfFiles(self):
        for item in self.ui.swfList.selectedItems():
            self.ui.swfList.takeItem(self.ui.swfList.row(item))

    @Slot()
    def addSAFile(self):
        file = self.openSaFileNameDialog()
        print(file)
        self.ui.saLineEdit.setText(file)

    def openSwfFileNamesDialog(self):
        DEFAULT_SWF_DIR_KEY = "default_swf_dir"
        settings = QSettings()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,
            "Select file(s)",
            settings.value(DEFAULT_SWF_DIR_KEY),
            "Shockwave Flash (*.swf);;All Files (*)",
            options=options)
        if files:
            currentDir = QDir()
            settings.setValue(DEFAULT_SWF_DIR_KEY, currentDir.absoluteFilePath(files[-1]));
        return files

    def openSaFileNameDialog(self):
        DEFAULT_SA_DIR_KEY = "default_sa_dir"
        settings = QSettings()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self,
            "Select file",
            settings.value(DEFAULT_SA_DIR_KEY),
            "EXE files (*.exe);;All Files (*)",
            options=options)
        if file:
            currentDir = QDir()
            settings.setValue(DEFAULT_SA_DIR_KEY, currentDir.absoluteFilePath(file));
        return file

    def eventFilter(self, object, event):
        if object.objectName() == "swfList":
            if event.type() == QEvent.DragEnter:
                #print("DragEnter")
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                return True
            if event.type() == QEvent.Drop:
                #print("Drop")
                # https://stackoverflow.com/a/45672412/3049315
                for url in event.mimeData().urls():
                    self.ui.swfList.addItem(str(url.toLocalFile()))
                return True
        return False


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
