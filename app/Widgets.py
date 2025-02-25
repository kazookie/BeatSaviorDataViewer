import os
import glob
import json
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QVBoxLayout, QLineEdit, QAbstractItemView
import pyqtgraph as pg

class SideBar(QWidget):
    def __init__(self, main_window):
        super().__init__()

        # Init widgets
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Search Text")
        self.dataListWidget = DataListWidget(main_window)
        # Init laout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.dataListWidget)

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
                item.setText(data['songName'] + ' by ' + data['songArtist'] + ' Mapped by '+ data['songMapper'])
                self.addItem(item)
    
    def currentChanged(self, current, previous):
        index = current.row()
        self.scrollToItem(self.currentItem(), QAbstractItemView.ScrollHint.EnsureVisible)

        data = self.play_datas[index]
        notes = data['deepTrackers']['noteTracker']['notes']
        graph_data = {
            "preswing": [],
            "preswing_score": [],
            "postswing": [],
            "postswing_score": []
        }
        for note in notes:
            graph_data["preswing"].append(note['preswing'])
            graph_data["preswing_score"].append(note['score'][0])
            graph_data["postswing"].append(note['postswing'])
            graph_data["postswing_score"].append(note['score'][2])
        
        self.changed.emit(graph_data)

class PreswingGraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pw = pg.PlotWidget(title="プレスイング")

        # Init laout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.pw)

    @Slot(object) 
    def update_graph(self, data):
        self.pw.clear()
        self.pw.plot([d*100 for d in data['preswing']], pen=(0,0,0))
        self.pw.plot([0, len(data['preswing'])], [100, 100], pen=(255, 0, 0))
        self.pw.getAxis('left').setLabel('deg')
        self.pw.setYRange(30, 300)
        self.update()

class PostswingGraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pw = pg.PlotWidget(title="ポストスイング")

        # Init laout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.pw)

    @Slot(object) 
    def update_graph(self, data):
        self.pw.clear()
        self.pw.plot([d*60 for d in data['postswing']], pen=(0,0,0))
        self.pw.plot([0, len(data['postswing'])], [60, 60], pen=(255, 0, 0))
        self.pw.getAxis('left').setLabel('deg')
        self.pw.setYRange(0, 270)

class PostswingScoreGraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pw = pg.PlotWidget(title="ポストスイング")

        # Init laout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.pw)

    @Slot(object) 
    def update_graph(self, data):
        self.pw.clear()
        self.pw.plot(data['postswing_score'], pen=(0,0,0))
        # self.pw.plot([0, len(data['postswing'])], [60, 60], pen=(255, 0, 0))
        self.pw.getAxis('left').setLabel('point')
        # self.pw.setYRange(0, 270)