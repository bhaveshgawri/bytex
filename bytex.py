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

		cutAction = QtGui.QAction("Cut",self)
		cutAction.setShortcut("Ctrl+x")
		cutAction.setStatusTip("Cut the selected text.")
		cutAction.triggered.connect(self.close_editor)
		
		copyAction = QtGui.QAction("Copy",self)
		copyAction.setShortcut("Ctrl+c")
		copyAction.setStatusTip("Copy the selected text.")
		copyAction.triggered.connect(self.close_editor)
		
		pasteAction = QtGui.QAction("Paste",self)
		pasteAction.setShortcut("Ctrl+v")
		pasteAction.setStatusTip("Paste the text on clipboard at position of cursor.")
		pasteAction.triggered.connect(self.close_editor)
		
		undoAction = QtGui.QAction("Undo",self)
		undoAction.setShortcut("Ctrl+z")
		undoAction.setStatusTip("Undo the last change.")
		undoAction.triggered.connect(self.close_editor)
		
		redoAction = QtGui.QAction("Redo",self)
		redoAction.setShortcut("Ctrl+Shift+z")
		redoAction.setStatusTip("Redo the last change.")
		redoAction.triggered.connect(self.close_editor)
		
		deleteAction = QtGui.QAction("Delete",self)
		deleteAction.setShortcut("del")
		deleteAction.setStatusTip("Delete the selected text.")
		deleteAction.triggered.connect(self.close_editor)
		
		readOnlyAction = QtGui.QAction("Read Only",self, checkable = True)
		readOnlyAction.setStatusTip("Make text read-only.")
		readOnlyAction.triggered.connect(lambda: self.read_only(readOnlyAction))
		
		bar = self.menuBar()
		file = bar.addMenu("File")
		edit = bar.addMenu("Edit")
		
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

		edit.addAction(undoAction)
		edit.addAction(redoAction)
		edit.addSeparator()
		edit.addAction(cutAction)
		edit.addAction(copyAction)
		edit.addAction(pasteAction)
		edit.addSeparator()
		edit.addAction(readOnlyAction)
		edit.addSeparator()
		edit.addAction(deleteAction)

		self.editor()

		self.view()
	
	def view(self):
		self.show()
	
	def editor(self):
		self.textEdit = QtGui.QTextEdit()
		self.setCentralWidget(self.textEdit)
	
	def close_editor(self):
		sys.exit()
	
	def read_only(self, readOnlyAction):
		if readOnlyAction.isChecked() is True:
			self.textEdit.setReadOnly(True)
		else:
			self.textEdit.setReadOnly(False)
		
def run():
	app = QtGui.QApplication(sys.argv)
	new_editor = Editor()
	sys.exit(app.exec_())

run()