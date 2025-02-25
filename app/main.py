import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
import PySide6QtAds as QtAds
import Widgets
import pyqtgraph as pg
from qt_material import apply_stylesheet

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beat Savior Data Viewer")
        self.resize(1280, 720)
        self.init_menubar()

        # Init Widgets
        self.dataList = Widgets.DataListWidget(self)
        self.preswingGraph = Widgets.PreswingGraphWidget()
        self.postswingGraph = Widgets.PostswingGraphWidget()
        self.postswingscoreGraph = Widgets.PostswingScoreGraphWidget()
        # Init connection
        self.dataList.changed.connect(self.preswingGraph.update_graph)
        self.dataList.changed.connect(self.postswingGraph.update_graph)
        self.dataList.changed.connect(self.postswingscoreGraph.update_graph)
        # Init Docks
        self.dock_manager = QtAds.CDockManager(self)
        labels = ["DataList", "PreswingGraph", "PostswingGraph", "PostswingScoreGraph"]
        self.docks = [QtAds.CDockWidget(label) for label in labels]
        self.docks[0].setWidget(self.dataList)
        self.docks[1].setWidget(self.preswingGraph)
        self.docks[2].setWidget(self.postswingGraph)
        self.docks[3].setWidget(self.postswingscoreGraph)
        h = self.dock_manager.addDockWidget(QtAds.RightDockWidgetArea, self.docks[0])
        h = self.dock_manager.addDockWidget(QtAds.RightDockWidgetArea, self.docks[1])
        h = self.dock_manager.addDockWidget(QtAds.BottomDockWidgetArea, self.docks[2], h)
        h = self.dock_manager.addDockWidget(QtAds.BottomDockWidgetArea, self.docks[3], h)

    def init_menubar(self):
        menubar = self.menuBar()
        menu_file = menubar.addMenu("File")
        menu_view = menubar.addMenu("View")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # apply_stylesheet(app, theme='dark_teal.xml')
    sys.exit(app.exec())