"""
Defines the PyQt6 UI for the main application window after login.
Sets up widgets such as the feature list, instruction box, progress box, and user info label.
Applies a dark theme and disables editing for certain widgets.
"""

from PyQt6 import QtCore, QtGui, QtWidgets 

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 450)
        MainWindow.setFixedSize(600, 450)  # Set fixed size for the window
        MainWindow.setWindowIcon(QtGui.QIcon("UurWaresLogo.ico"))

        # Koyu Tema Stili
        MainWindow.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
                font-size: 14px;
                border-radius: 10px;
            }
            QListView {
                background-color: #3C3F41;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #555555;
                border: 1px solid #777;
                padding: 5px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QTextEdit {
                background-color: #3C3F41;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 5px;
            }
            QLabel {
                font-weight: bold;
                font-size: 12px;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.applist = QtWidgets.QListView(parent=self.centralwidget)
        self.applist.setGeometry(QtCore.QRect(10, 10, 256, 291))
        self.applist.setObjectName("applist")
        self.applist.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)  # Disable editing

        self.btnstart = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnstart.setGeometry(QtCore.QRect(320, 240, 261, 28))
        self.btnstart.setObjectName("btnstart")

        self.instructionBox = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.instructionBox.setGeometry(QtCore.QRect(320, 10, 261, 221))
        self.instructionBox.setObjectName("instructionBox")
        self.instructionBox.setReadOnly(True)  # Prevent user from editing

        self.progressBox = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.progressBox.setGeometry(QtCore.QRect(320, 280, 261, 80))
        self.progressBox.setObjectName("progressBox")
        self.progressBox.setReadOnly(True)

        self.formLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 310, 160, 80))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        
        self.label = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        
        self.lblusername = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.lblusername.setText("")
        self.lblusername.setObjectName("lblusername")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lblusername)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ana Sayfa"))
        self.btnstart.setText(_translate("MainWindow", "Start"))
        self.label.setText(_translate("MainWindow", "Username:"))
