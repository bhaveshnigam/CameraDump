import sys

import psutil
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QMainWindow

from UI.dump_media_device import Ui_Dialog
from utils import dump_card




class MainWindow(QMainWindow):
  def __init__(self, app):
    super(MainWindow, self).__init__()
    self.app = app
    self.ui = Ui_Dialog()
    self.ui.setupUi(self)

    self.ui.progressBar.setProperty('value', 0)

    partitions = psutil.disk_partitions()
    for partition in partitions:
      mountpoint = partition.mountpoint
      if (('private' in mountpoint) or
          (mountpoint == '/')
      ):
        continue
      self.ui.comboBox.addItem(mountpoint)
      self.ui.comboBox_2.addItem(mountpoint)

  def accept(self, *args, **kwargs):
    target_project_name = self.ui.lineEdit.text()
    source_directory = self.ui.comboBox.currentText()
    target_directory = self.ui.comboBox_2.currentText()
    self.ui.okButton.setEnabled(False)

    progress_update = QtCore.Signal(int)


    retval = dump_card(
      source_card_path=source_directory,
      destination_path=target_directory,
      backup_folder_name=target_project_name,
      skip_file_types=[],
      qt_application=self.app,
      progress_bar=self.ui.progressBar
    )
    sys.exit(0)

  def update_progress_bar(self, progress_value):
    self.ui.progressBar.setValue(progress_value)

  def reject(self, *args, **kwargs):
    sys.exit(0)


if __name__ == "__main__":
  app = QApplication(sys.argv)

  window = MainWindow(app=app)
  window.show()

  sys.exit(app.exec_())
