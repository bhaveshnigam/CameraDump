import pathlib
import sys

import psutil
from PyQt6 import QtWidgets
from PyQt6.QtCore import QStringListModel, Qt

from UI.dump_media_device import Ui_Dialog
from utils import dump_card, get_child_folder_names


def set_auto_complete_data(auto_complete_model, target_path=''):
    autocomplete_data = get_child_folder_names(target_path + '/Photo/')
    auto_complete_model.setStringList(autocomplete_data)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.progressBar.setProperty('value', 0)

        self.completer = QtWidgets.QCompleter()
        self.ui.lineEdit.setCompleter(self.completer)

        self.autoCompleteModel = QStringListModel()
        # set_auto_complete_data(self.autoCompleteModel)

        self.completer.setModel(self.autoCompleteModel)

        self.ui.comboBox_2.currentIndexChanged.connect(self.updateDataModel, type=Qt.ConnectionType.AutoConnection)

        partitions = psutil.disk_partitions(all=True)
        for partition in partitions:
            mountpoint = partition.mountpoint
            if (('private' in mountpoint) or
                    (mountpoint == '/') or
                    (mountpoint.startswith('/boot'))
            ):
                continue
            self.ui.comboBox.addItem(mountpoint)
            self.ui.comboBox_2.addItem(mountpoint)
        home_directory = str(pathlib.Path('~').expanduser())
        self.ui.comboBox.addItem(home_directory)
        self.ui.comboBox_2.addItem(home_directory)

    def updateDataModel(self, value):
        set_auto_complete_data(self.autoCompleteModel, self.ui.comboBox_2.currentText())

    def accept(self, *args, **kwargs):
        target_project_name = self.ui.lineEdit.text()
        source_directory = self.ui.comboBox.currentText()
        target_directory = self.ui.comboBox_2.currentText()
        self.ui.okButton.setEnabled(False)

        retval = dump_card(
            source_card_path=source_directory,
            destination_path=target_directory,
            backup_folder_name=target_project_name,
            qt_application=self.app,
            progress_bar=self.ui.progressBar,
            do_create_premiere_folders=self.ui.checkBox_2.isChecked(),
            clear_files_after_copy=self.ui.checkBox_3.isChecked()
        )

        # if self.ui.checkBox_2.isChecked():
        #   create_premiere_folders(
        #     target_directory, target_project_name
        #   )
        sys.exit(0)

    def update_progress_bar(self, progress_value):
        self.ui.progressBar.setValue(progress_value)

    def reject(self, *args, **kwargs):
        sys.exit(0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(app=app)
    window.show()

    sys.exit(app.exec())
