from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

class GridScoreWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.labels = [QLabel("label") for i in range(0,12,1)]
        for label in self.labels:
            label.setStyleSheet("border: 1px solid black;") 

        # Init laout
        layout = QVBoxLayout()
        self.setLayout(layout)
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.labels[0])
        topLayout.addWidget(self.labels[1])
        topLayout.addWidget(self.labels[2])
        topLayout.addWidget(self.labels[3])
        midLayout = QHBoxLayout()
        midLayout.addWidget(self.labels[4])
        midLayout.addWidget(self.labels[5])
        midLayout.addWidget(self.labels[6])
        midLayout.addWidget(self.labels[7])
        btmLayout = QHBoxLayout()
        btmLayout.addWidget(self.labels[8])
        btmLayout.addWidget(self.labels[9])
        btmLayout.addWidget(self.labels[10])
        btmLayout.addWidget(self.labels[11])
        layout.addLayout(topLayout)
        layout.addLayout(midLayout)
        layout.addLayout(btmLayout)


    @Slot(object) 
    def update_graph(self, data):
        gridAcc = data['trackers']['accuracyTracker']['gridAcc']
        for i, label in enumerate(self.labels):
            acc = "%03.2f" % gridAcc[i] if gridAcc[i] != 'NaN' else ''
            label.setText(acc)
        