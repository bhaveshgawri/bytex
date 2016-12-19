import sys,  os
from PyQt4 import QtGui, QtCore

class Editor(QtGui.QMainWindow):
	def __init__(self):
		super(Editor,self).__init__()
		self.setGeometry(0,0, 600, 800)
		self.setMinimumSize(600,350)
		self.setWindowTitle("bytex")		
		
		self.tabWidget = QtGui.QTabWidget(self)
		self.setCentralWidget(self.tabWidget)
		self.tabWidget.setTabsClosable(True)
		self.tabWidget.setMovable(True)
		#self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
			
#--------------------File Menu Actions-------------------#

		newTabAction = QtGui.QAction("New File",self)
		newTabAction.setShortcut("Ctrl+t")
		newTabAction.setStatusTip("Create a new Document")
		newTabAction.triggered.connect(self.newFile_)

		newWinAction = QtGui.QAction("New Window",self)
		newWinAction.setShortcut("Ctrl+n")
		newWinAction.setStatusTip("Open a new document in a new window")
		newWinAction.triggered.connect(self.__init__)
		
		openAction = QtGui.QAction("Open",self)
		openAction.setShortcut("Ctrl+o")
		openAction.setStatusTip("Open an existing document")
		openAction.triggered.connect(self.open_)
		
		saveAction = QtGui.QAction("Save",self)
		saveAction.setShortcut("Ctrl+s")
		saveAction.setStatusTip("Save this document")
		saveAction.triggered.connect(self.save_)
		
		saveAsAction = QtGui.QAction("Save As...",self)
		saveAsAction.setShortcut("Ctrl+Shift+s")
		saveAsAction.setStatusTip("Save this document as...")
		saveAsAction.triggered.connect(self.saveAs_)
		
		closeAction = QtGui.QAction("Close",self)
		closeAction.setShortcut("Ctrl+w")
		closeAction.setStatusTip("Close the current document")
		closeAction.triggered.connect(self.closeTab_)
		self.tabWidget.tabCloseRequested.connect(self.tabWidget.removeTab)
		#  ^without this line 'x' on tabs won't work.

		quitAction = QtGui.QAction("Quit",self)
		quitAction.setShortcut("Ctrl+q")
		quitAction.setStatusTip("Close all documents and EXIT.")
		quitAction.triggered.connect(self.closeEditor_)

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
		readOnlyAction.triggered.connect(lambda: self.readOnly_(readOnlyAction_))
		
		selectAllAction = QtGui.QAction("Select All",self)
		selectAllAction.setShortcut("Ctrl+a")
		selectAllAction.setStatusTip("Select all the text.")
		selectAllAction.triggered.connect(self.selectAll_)

		clearAction = QtGui.QAction("Clear Screen",self)
		clearAction.setShortcut("Ctrl+l")
		clearAction.setStatusTip("Clear all the text from screen.")
		clearAction.triggered.connect(self.clear_)
		
		insertAction = QtGui.QAction("Insert Mode",self, checkable = True)
		insertAction.setStatusTip("Toggle Insert Mode for all tabs.")
		insertAction.triggered.connect(lambda: self.insert_(insertAction))

		
#-------------------//Edit Menu Actions//-----------------#

#--------------------Format Menu Actions------------------#	

		fontAction = QtGui.QAction("Fonts", self)
		fontAction.setStatusTip("Set the font type, style and size.")
		fontAction.triggered.connect(self.setFont_)

		action_group = QtGui.QActionGroup(self, exclusive = True)
		action2 = action_group.addAction(QtGui.QAction("Tab Width:2", self, checkable=True))
		action4 = action_group.addAction(QtGui.QAction("Tab Width:4", self, checkable=True))
		action8 = action_group.addAction(QtGui.QAction("Tab Width:8", self, checkable=True))
		action_group.triggered.connect(lambda: self.setTabWidth_(action_group, action2, action4, action8))

#------------------//Format Menu Actions//----------------#

#-----------------Misc. Actions and Signals---------------#
		
		self.tabWidget.currentChanged.connect(self.nameOfWindow_)

		nextTabAction = QtGui.QAction(self)
		nextTabAction.setShortcut("Ctrl+t")
		nextTabAction.triggered.connect(self.nextTab_)
		
		prevTabAction = QtGui.QAction(self)
		prevTabAction.setShortcut("Ctrl+shift+t")
		prevTabAction.triggered.connect(self.prevTab_)

#--------------//Misc. Actions and Signals//--------------#	
		statusBar = self.statusBar()

#---------------------Menu Bar Creation-------------------#

		bar = self.menuBar()
		file = bar.addMenu("File")
		edit = bar.addMenu("Edit")
		format_ = bar.addMenu("Format") 

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

		format_.addAction(fontAction)
		tabWidth = format_.addMenu("Tab Width")
		tabWidth.addAction(action2)
		tabWidth.addAction(action4)
		tabWidth.addAction(action8)
#-------------------//Menu Bar Creation//-----------------#
		
		self.view_()
		
		self.fileList = []

#-------------------Function Declarations-----------------#
	
	def view_(self):
		self.show()
	
	def nameOfWindow_(self):
		self.tab_name = self.tabWidget.tabText(self.tabWidget.currentIndex())
		self.setWindowTitle(self.tab_name + " - bytex")	
		if self.tabWidget.count() is 0:
			sys.exit()
	
	def nextTab_(self):
		self.tabWidget.setCurrentIndex(self.tabWidget.CurrentIndex() + 1)
	
	def prevTab_(self):
		self.tabWidget.setCurrentIndex(self.tabWidget.CurrentIndex() - 1)

#--------------------File Menu Functions------------------#	
	
	def newFile_(self):
		self.textEdit = QtGui.QTextEdit(self.tabWidget)
		self.tabWidget.addTab(self.textEdit, "Untitled " + str(self.tabWidget.count()+1))

	def open_(self):
		oldFileName = QtGui.QFileDialog.getOpenFileName(self, "Open File")
		file = open(oldFileName, 'r')
		
		self.textEdit = QtGui.QTextEdit(self.tabWidget)
		self.tabWidget.addTab(self.textEdit, os.path.basename(oldFileName))
		
		self.fileList.append(oldFileName)

		data = file.read();
		self.textEdit.setText(data)

		file.close()

	def save_(self):
		baseNames = []
		for file in self.fileList:
			baseNames.append(os.path.basename(file))
		
		self.tabName = self.tabWidget.tabText(self.tabWidget.currentIndex())	
		
		if not self.tabName in baseNames:
			self.saveAs_()
		else:
			for item in self.fileList:
				if self.tabName in item:
					saveFile = open(item, 'w')
					data = self.tabWidget.currentWidget().toPlainText()					
					saveFile.write(data)
					saveFile.close()

	def saveAs_(self):
		newFileName = QtGui.QFileDialog.getSaveFileName(self, "Save File")
		file = open(newFileName, 'w')
		
		self.tabWidget.setTabText(self.tabWidget.currentIndex(), os.path.basename(newFileName))
		self.setWindowTitle(newFileName + " - bytex")
		
		self.fileList.append(newFileName)	

		data = self.tabWidget.currentWidget().toPlainText()
		file.write(data)
		
		file.close()
	
	def closeTab_(self):
		self.tabWidget.removeTab(self.tabWidget.currentIndex())
		if self.tabWidget.count() == 0:
			sys.exit()

	def closeEditor_(self):
		sys.exit()

#------------------//File Menu Functions//----------------#

#--------------------Edit Menu Functions------------------#

	def undo_(self):
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.undo()

	def redo_(self):
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.redo()
	
	def cut_(self):
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.cut()
	
	def copy_(self):
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.copy()
	
	def paste_(self):
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.paste()
	
	def readOnly_(self, readOnlyAction):
		if readOnlyAction.isChecked() is True:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:	
				text_edit.setReadOnly(True)
		else:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				text_edit.setReadOnly(False)
	
	def selectAll_(self):
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.selectAll()
	
	def clear_(self):
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.clear()
	
	def insert_(self, insertAction):
		if insertAction.isChecked() is True:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
   				text_edit.setOverwriteMode(True)
		else:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
   				text_edit.setOverwriteMode(False)

#------------------//Edit Menu Functions//----------------#

#-------------------Format Menu Functions-----------------#	

	def setFont_(self):
		font, true = QtGui.QFontDialog.getFont()
		if true:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				text_edit.setFont(font)
	
	def setTabWidth_(self,action_group, action2, action4, action8):
		if action_group.checkedAction() is action2:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				text_edit.setTabStopWidth(20)
		elif action_group.checkedAction() is action4:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				text_edit.setTabStopWidth(40)
		elif action_group.checkedAction() is action8:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				text_edit.setTabStopWidth(80)

#-----------------//Format Menu Functions//---------------#	
	
	
def run():
	app = QtGui.QApplication(sys.argv)
	new_editor = Editor()
	sys.exit(app.exec_())

run()