import os
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PySide6.QtCore import (
    Slot, QFile, QIODevice,
    QTextStream, QCoreApplication,
    QSettings, QDir, QEvent
)

from forms.ui_form import Ui_MainWindow

from lib.swflib import swf2exe_win

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
        self.ui.chooseDirBtn.clicked.connect(self.selectOutputDirectory)
        self.ui.convertBtn.clicked.connect(self.convertAll)

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
        fileList = self.openSwfFileNamesDialog("default_swf_dir", "Select SWF file(s)")
        self.ui.swfList.addItems(fileList)

    @Slot()
    def removeSwfFiles(self):
        for item in self.ui.swfList.selectedItems():
            self.ui.swfList.takeItem(self.ui.swfList.row(item))

    @Slot()
    def addSAFile(self):
        file = self.openExeFileNameDialog("default_sa_dir", "Select Adobe Flash Player SA file")
        self.ui.saLineEdit.setText(file)

    @Slot()
    def selectOutputDirectory(self):
        dir = self.getSaveDirDialog("default_out_dir", "Choose output directory")
        self.ui.outFileLineEdit.setText(dir)

    @Slot()
    def convertAll(self):
        saFile = self.ui.saLineEdit.text()
        if not saFile:
            QMessageBox.information(
                self,
                QCoreApplication.applicationName(),
                "You must select an Adobe Flash Player SA file.")
            return
        if self.ui.swfList.count() == 0:
            QMessageBox.information(
                self,
                QCoreApplication.applicationName(),
                "You must select at least one SWF file to convert.")
            return
        for i in range(self.ui.swfList.count()):
            swfFile = self.ui.swfList.item(i).text()
            outFile = os.path.join(self.ui.outFileLineEdit.text(), os.path.basename(swfFile))
            outFile = os.path.splitext(outFile)[0]+'.exe'
            print(f"Converting:\n-{swfFile}\n-{outFile}")
            swf2exe_win(swfFile, outFile, saFile)

    def openSwfFileNamesDialog(self, default_dir, caption):
        settings = QSettings()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,
            caption,
            settings.value(default_dir),
            "Shockwave Flash (*.swf);;All Files (*)",
            options=options)
        if files:
            currentDir = QDir()
            settings.setValue(default_dir, currentDir.absoluteFilePath(files[-1]));
        return files

    def openExeFileNameDialog(self, default_dir, caption):
        settings = QSettings()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self,
            caption,
            settings.value(default_dir),
            "EXE files (*.exe);;All Files (*)",
            options=options)
        if file:
            currentDir = QDir()
            settings.setValue(default_dir, currentDir.absoluteFilePath(file));
        return file

    def getSaveDirDialog(self, default_dir, caption):
        settings = QSettings()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.DontResolveSymlinks
        dir = QFileDialog.getExistingDirectory(self,
            caption,
            settings.value(default_dir),
            options=options)
        if dir:
            settings.setValue(default_dir, dir);
        return dir

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
