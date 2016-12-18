import sys
from PyQt4 import QtGui, QtCore

class Editor(QtGui.QMainWindow):
	def __init__(self):
		super(Editor,self).__init__()
		self.setGeometry(100,100, 300, 300)
		self.setWindowTitle("bytex")
		#self.setWindowIcon(QtGui.QIcon())
		
#--------------------File Menu Actions-------------------#

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

#------------------//File Menu Actions//-----------------#

#--------------------Edit Menu Actions-------------------#

		undoAction = QtGui.QAction("Undo",self)
		undoAction.setShortcut("Ctrl+z")
		undoAction.setStatusTip("Undo the last change.")
		undoAction.triggered.connect(self.undo_)
		
		redoAction = QtGui.QAction("Redo",self)
		redoAction.setShortcut("Ctrl+Shift+z")
		redoAction.setStatusTip("Redo the last change.")
		redoAction.triggered.connect(self.redo_)
		
		cutAction = QtGui.QAction("Cut",self)
		cutAction.setShortcut("Ctrl+x")
		cutAction.setStatusTip("Cut the selected text.")
		cutAction.triggered.connect(self.cut_)
		
		copyAction = QtGui.QAction("Copy",self)
		copyAction.setShortcut("Ctrl+c")
		copyAction.setStatusTip("Copy the selected text.")
		copyAction.triggered.connect(self.copy_)
		
		pasteAction = QtGui.QAction("Paste",self)
		pasteAction.setShortcut("Ctrl+v")
		pasteAction.setStatusTip("Paste the text on clipboard at position of cursor.")
		pasteAction.triggered.connect(self.paste_)
		
		readOnlyAction = QtGui.QAction("Read Only",self, checkable = True)
		readOnlyAction.setStatusTip("Make text read-only.")
		readOnlyAction.triggered.connect(lambda: self.readOnly_(readOnlyAction))
		
		selectAllAction = QtGui.QAction("Select All",self)
		selectAllAction.setShortcut("Ctrl+a")
		selectAllAction.setStatusTip("Select all the text.")
		selectAllAction.triggered.connect(self.selectAll_)

		clearAction = QtGui.QAction("Clear Screen",self)
		clearAction.setShortcut("Ctrl+l")
		clearAction.setStatusTip("Clear all the text from screen.")
		clearAction.triggered.connect(self.clear_)
		
		insertAction = QtGui.QAction("Inseret Mode",self, checkable = True)
		insertAction.setStatusTip("Toggle Insert Mode.")
		insertAction.triggered.connect(lambda: self.insert_(insertAction))
		
#-------------------//Edit Menu Actions//-----------------#		

#---------------------Menu Bar Creation-------------------#

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
		edit.addAction(selectAllAction)
		edit.addAction(clearAction)
		edit.addSeparator()
		edit.addAction(insertAction)

#-------------------//Menu Bar Creation//-----------------#
		
		self.statusBar()
		self.editor()
		self.view()

#-------------------Function Declarations-----------------#
	
	def view(self):
		self.show()
	def editor(self):
		self.textEdit = QtGui.QTextEdit()
		self.setCentralWidget(self.textEdit)
	
#--------------------File Menu Functions------------------#	
	
	def close_editor(self):
		sys.exit()


#------------------//File Menu Functions//----------------#

#--------------------Edit Menu Functions------------------#

	def undo_(self):
		self.textEdit.undo()
	
	def redo_(self):
		self.textEdit.redo()
	
	def cut_(self):
		self.textEdit.cut()
	
	def copy_(self):
		self.textEdit.copy()
	
	def paste_(self):
		self.textEdit.paste()
	
	def readOnly_(self, readOnlyAction):
		if readOnlyAction.isChecked() is True:
			self.textEdit.setReadOnly(True)
		else:
			self.textEdit.setReadOnly(False)
	
	def selectAll_(self):
		self.textEdit.selectAll()
	
	def clear_(self):
		self.textEdit.clear()
	
	def insert_(self, insertAction):
		if insertAction.isChecked() is True:
			self.textEdit.setOverwriteMode(True)
		else:
			self.textEdit.setOverwriteMode(False)

#------------------//Edit Menu Functions//----------------#
	
	
def run():
	app = QtGui.QApplication(sys.argv)
	new_editor = Editor()
	sys.exit(app.exec_())

run()