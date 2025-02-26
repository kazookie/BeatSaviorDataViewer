import os
import glob
import json
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView

class DataListWidget(QListWidget):
    changed = Signal(object)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.create_file_list()

    def create_file_list(self):
        data_dir = os.getenv("APPDATA") + "\\Beat Savior Data\\"
        files = reversed(glob.glob(data_dir + "\\20*"))

        self.play_datas = []
        for file in files:
            # Read file
            fp = open(file, 'r', encoding='utf-8')
            lines = fp.readlines()
            fp.close()

            for line in lines[1:-1]:
                data = json.loads(line)
                self.play_datas.append(data)
                item = QListWidgetItem()
                item_text = data['songName'] + ' by ' + data['songArtist'] + ' Mapped by '+ data['songMapper']
                item.setText(data['songName'] + ' by ' + data['songArtist'] + ' Mapped by '+ data['songMapper'])
                item.setToolTip(item_text)
                self.addItem(item)
    
    def currentChanged(self, current, previous):
        index = current.row()
        self.scrollToItem(self.currentItem(), QAbstractItemView.ScrollHint.EnsureVisible)

        data = self.play_datas[index]        
        self.changed.emit(data)