from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg

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
        notes = data['deepTrackers']['noteTracker']['notes']
        plot_data = [note['preswing']*100 for note in notes]

        self.pw.clear()
        self.pw.plot(plot_data)
        self.pw.plot([0, len(plot_data)], [100, 100], pen=(255, 0, 0))
        self.pw.getAxis('left').setLabel('deg')
        self.pw.setYRange(30, 300)
        self.update()