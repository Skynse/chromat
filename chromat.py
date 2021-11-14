from krita import *
from PyQt5.QtWidgets import *

KI = Krita.instance()

class Docker(DockWidget):
    def __init__(self):
        # This is initialising the parent, always important when subclassing.
        super().__init__()
        self.setWindowTitle("Post Processing")
        main = QWidget(self)
        self.setWidget(main)
        #lock the dock widget
        self.setFeatures(QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable)

        start = QPushButton("run", main)
        start.clicked.connect(self.chroma)
        main.setLayout(QVBoxLayout())
        main.layout().addWidget(start)

    def canvasChanged(self, canvas):
        pass


    def chroma(self):
        doc = KI.activeDocument()
        #get active node
        node = doc.activeNode()

        chromaGroup = doc.createGroupLayer("Chroma Group")
        doc.rootNode().addChildNode(chromaGroup, None)

        red = node.duplicate()
        blue = node.duplicate()
        green = node.duplicate()

        red.setName("red")
        blue.setName("blue")
        green.setName("green")

        root_node =  doc.rootNode()
        #set only green channel for green node

        blue.channels()[0].setVisible(True)
        blue.channels()[1].setVisible(False)
        blue.channels()[2].setVisible(False)

        #set only red channel for red node

        red.channels()[0].setVisible(False)
        red.channels()[1].setVisible(False)
        red.channels()[2].setVisible(True)

        #set only blue channel for green node

        green.channels()[0].setVisible(False)
        green.channels()[1].setVisible(True)
        green.channels()[2].setVisible(False)

        #move nodes by offset

        red.move(3, 3)
        blue.move(-5, 5)
        green.move(-7, -7)

        chromaGroup.addChildNode(green, None)
        chromaGroup.addChildNode(blue, None)
        chromaGroup.addChildNode(red, None)

    def setup(self):
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("Chromat", DockWidgetFactoryBase.DockRight, Docker))
