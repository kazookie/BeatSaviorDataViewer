from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg

class PostswingGraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pw = pg.PlotWidget(title="Postswing [degree]")

        # Init laout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.pw)

    @Slot(object) 
    def update_graph(self, data):
        notes = data['deepTrackers']['noteTracker']['notes']
        plot_data = [note['postswing']*60 for note in notes]

        self.pw.clear()
        self.pw.plot(plot_data, pen=(0,0,0))
        self.pw.plot([0, len(plot_data)], [60, 60], pen=(255, 0, 0))
        self.pw.setYRange(0, 270)

class PostswingScoreGraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pw = pg.PlotWidget(title="Postswing [score]")

        # Init laout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.pw)

    @Slot(object) 
    def update_graph(self, data):
        notes = data['deepTrackers']['noteTracker']['notes']
        plot_data = [note['score'][2] for note in notes]

        self.pw.clear()
        self.pw.plot(plot_data, pen=(0,0,0))
        self.pw.setYRange(0, 100)