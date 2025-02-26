import sys
from PySide6.QtWidgets import QApplication, QMainWindow
import PySide6QtAds as QtAds
import pyqtgraph as pg
from datalist import *
from preswing import *
from postswing import *
from accuracy import *
from speed import *
from gridscore import *

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beat Savior Data Viewer")
        self.resize(1280, 720)
        self.init_menubar()

        # Init Widgets
        self.dataList = DataListWidget(self)
        self.graphs = [
            PreswingGraphWidget(),
            PreswingScoreGraphWidget(),
            PostswingGraphWidget(),
            PostswingScoreGraphWidget(),
            SpeedGraphWidget(),
            AccuracyGraphWidget(),
            GridScoreWidget(),
        ]
        # Init connection
        for graph in self.graphs:
            self.dataList.changed.connect(graph.update_graph)
        # Init Docks
        self.dock_manager = QtAds.CDockManager(self)
        dock = QtAds.CDockWidget("DataList")
        dock.setWidget(self.dataList)
        self.dock_manager.addDockWidget(QtAds.RightDockWidgetArea, dock)
        for i, graph in enumerate(self.graphs):
            print(type(graph))
            dock = QtAds.CDockWidget(type(graph).__name__)
            dock.setWidget(graph)
            if i == 0:
                h1 = self.dock_manager.addDockWidget(QtAds.RightDockWidgetArea, dock)
            elif i == 1:
                h2 = self.dock_manager.addDockWidget(QtAds.RightDockWidgetArea, dock)
            else:
                if i%2 == 0:
                    self.dock_manager.addDockWidget(QtAds.BottomDockWidgetArea, dock, h1)
                elif i%2 == 1:
                    self.dock_manager.addDockWidget(QtAds.BottomDockWidgetArea, dock, h2)


    def init_menubar(self):
        menubar = self.menuBar()
        menu_file = menubar.addMenu("File")
        menu_view = menubar.addMenu("View")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())