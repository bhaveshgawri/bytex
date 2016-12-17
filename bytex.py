import sys
from PyQt4 import QtGui, QtCore

class Editor(QtGui.QMainWindow):
	def __init__(self):
		super(Editor,self).__init__()
		self.setGeometry(100,100, 300, 300)
		self.setWindowTitle("bytex")
		#self.setWindowIcon(QtGui.QIcon())
		

		newTabAction = QtGui.QAction("New File",self)
		newTabAction.setShortcut("Ctrl+t")
		newTabAction.setStatusTip("Create a new Document")
		newTabAction.triggered.connect(self.close_editor)
		
		newWinAction = QtGui.QAction("New Window",self)
		newWinAction.setShortcut("Ctrl+n")
		newWinAction.setStatusTip("Open a new document in a new window")
		newWinAction.triggered.connect(self.__init__)
		
		openAction = QtGui.QAction("Open",self)
		openAction.setShortcut("Ctrl+o")
		openAction.setStatusTip("Open an existing document")
		openAction.triggered.connect(self.close_editor)
		
		saveAction = QtGui.QAction("Save",self)
		saveAction.setShortcut("Ctrl+s")
		saveAction.setStatusTip("Save this document")
		saveAction.triggered.connect(self.close_editor)
		
		saveAsAction = QtGui.QAction("Save As...",self)
		saveAsAction.setShortcut("Ctrl+Shift+s")
		saveAsAction.setStatusTip("Save this document as...")
		saveAsAction.triggered.connect(self.close_editor)
		
		closeAction = QtGui.QAction("Close",self)
		closeAction.setShortcut("Ctrl+w")
		closeAction.setStatusTip("Close the current document")
		closeAction.triggered.connect(self.close_editor)

		quitAction = QtGui.QAction("Quit",self)
		quitAction.setShortcut("Ctrl+q")
		quitAction.setStatusTip("Close all documents and EXIT.")
		quitAction.triggered.connect(self.close_editor)

		
		bar = self.menuBar()
		file = bar.addMenu("File")
		
		file.addAction(newTabAction)
		file.addSeparator()
		file.addAction(openAction)
		file.addSeparator()
		file.addAction(saveAction)
		file.addAction(saveAsAction)
		file.addSeparator()
		file.addAction(newWinAction)
		file.addSeparator()
		file.addAction(closeAction)
		file.addAction(quitAction)


		self.editor()

		self.window()
	
	def window(self):
		self.show()
	
	def close_editor(self):
		sys.exit()

	def editor(self):
		self.textEdit = QtGui.QTextEdit()
		self.setCentralWidget(self.textEdit)
		
def run():
	app = QtGui.QApplication(sys.argv)
	new_editor = Editor()
	sys.exit(app.exec_())

run()