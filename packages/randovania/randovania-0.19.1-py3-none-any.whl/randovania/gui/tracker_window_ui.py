# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/travis/build/randovania/randovania/randovania/gui/tracker_window.ui',
# licensing of '/home/travis/build/randovania/randovania/randovania/gui/tracker_window.ui' applies.
#
# Created: Sun Jan  6 17:39:03 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_TrackerWindow(object):
    def setupUi(self, TrackerWindow):
        TrackerWindow.setObjectName("TrackerWindow")
        TrackerWindow.resize(802, 488)
        self.centralWidget = QtWidgets.QWidget(TrackerWindow)
        self.centralWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setObjectName("groupBox")
        self.items_tree_widget = QtWidgets.QTreeWidget(self.groupBox)
        self.items_tree_widget.setGeometry(QtCore.QRect(30, 70, 671, 91))
        self.items_tree_widget.setObjectName("items_tree_widget")
        self.events_list_widget = QtWidgets.QListWidget(self.groupBox)
        self.events_list_widget.setGeometry(QtCore.QRect(40, 240, 611, 91))
        self.events_list_widget.setObjectName("events_list_widget")
        self._events_list_header = QtWidgets.QLabel(self.groupBox)
        self._events_list_header.setGeometry(QtCore.QRect(50, 200, 47, 13))
        self._events_list_header.setObjectName("_events_list_header")
        self.current_location_label = QtWidgets.QLabel(self.groupBox)
        self.current_location_label.setGeometry(QtCore.QRect(30, 40, 331, 16))
        self.current_location_label.setObjectName("current_location_label")
        self.gridLayout.addWidget(self.groupBox, 1, 1, 1, 1)
        TrackerWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(TrackerWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 802, 21))
        self.menuBar.setObjectName("menuBar")
        TrackerWindow.setMenuBar(self.menuBar)

        self.retranslateUi(TrackerWindow)
        QtCore.QMetaObject.connectSlotsByName(TrackerWindow)

    def retranslateUi(self, TrackerWindow):
        TrackerWindow.setWindowTitle(QtWidgets.QApplication.translate("TrackerWindow", "Tracker", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("TrackerWindow", "GroupBox", None, -1))
        self.items_tree_widget.headerItem().setText(0, QtWidgets.QApplication.translate("TrackerWindow", "Item", None, -1))
        self.items_tree_widget.headerItem().setText(1, QtWidgets.QApplication.translate("TrackerWindow", "Quantity", None, -1))
        self.events_list_widget.setSortingEnabled(True)
        self._events_list_header.setText(QtWidgets.QApplication.translate("TrackerWindow", "Events", None, -1))
        self.current_location_label.setText(QtWidgets.QApplication.translate("TrackerWindow", "Current location:", None, -1))

