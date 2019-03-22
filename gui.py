import sys

import psutil
from PySide2.QtWidgets import QApplication, QMainWindow

from UI.dump_media_device import Ui_Dialog
from dump_memory_card import dump_card




class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
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

    progress_bar = self.ui.progressBar

    retval = dump_card(
      source_card_path=source_directory,
      destination_path=target_directory,
      backup_folder_name=target_project_name,
      qwidget_progress_bar=progress_bar
    )
    sys.exit(0)

  def reject(self, *args, **kwargs):
    sys.exit(0)


if __name__ == "__main__":
  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec_())
