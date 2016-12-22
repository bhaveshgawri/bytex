import sys,  os, webbrowser, subprocess
from PyQt4 import QtGui, QtCore, Qsci
from markdown_editor import web_edit

class Editor(QtGui.QMainWindow):
	def __init__(self):
		super(Editor, self).__init__()
		#print (help(Editor))
		self.setGeometry(0,0, 600, 800)
		self.setMinimumSize(600,350)
		self.setWindowTitle("bytex")		
		
		self.tabWidget = QtGui.QTabWidget(self)
		self.setCentralWidget(self.tabWidget)
		self.tabWidget.setTabsClosable(True)
		self.tabWidget.setMovable(True)
		#self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)

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
		
		insertAction = QtGui.QAction("Insert Mode",self, checkable = True)
		insertAction.setStatusTip("Toggle Insert Mode for all tabs.")
		insertAction.triggered.connect(lambda: self.insert_(insertAction))
		
#-------------------//Edit Menu Actions//-----------------#

#--------------------Format Menu Actions------------------#	

		fontAction = QtGui.QAction("Fonts", self)
		fontAction.setStatusTip("Set the font type, style and size.")
		fontAction.triggered.connect(self.setFont_)

		tab_action_group = QtGui.QActionGroup(self, exclusive = True)
		action2 = tab_action_group.addAction(QtGui.QAction("Tab Width:2", self, checkable=True))
		action4 = tab_action_group.addAction(QtGui.QAction("Tab Width:4", self, checkable=True))
		action8 = tab_action_group.addAction(QtGui.QAction("Tab Width:8", self, checkable=True))
		action12 = tab_action_group.addAction(QtGui.QAction("Tab Width:12", self, checkable=True))
		action16 = tab_action_group.addAction(QtGui.QAction("Tab Width:16", self, checkable=True))
		tab_action_group.triggered.connect(lambda: self.setTabWidth_(tab_action_group, action2, action4, action8, action12, action16))

		autoIndentAction = QtGui.QAction("Auto Indent", self, checkable = True)
		autoIndentAction.setChecked(True)
		autoIndentAction.setStatusTip("Toggle Auto Indentation")
		autoIndentAction.triggered.connect(lambda: self.setAutoIndent_(autoIndentAction))

#------------------//Format Menu Actions//----------------#

#---------------------Tool Menu Actions-------------------#
		
		terminalAction = QtGui.QAction("Open bash here", self)
		terminalAction.setShortcut("shift+alt+t")
		terminalAction.setToolTip("Open bash at the locaiton of file in current tab.")
		terminalAction.triggered.connect(self.openBash_)

		newMarkDownFileAction = QtGui.QAction("Try Now",self)
		newMarkDownFileAction.setShortcut("ctrl+shift+n")
		newMarkDownFileAction.setStatusTip("Try the markdown editor now.")
		newMarkDownFileAction.triggered.connect(self.openMarkEditor_)

		openMarkDownFileAction = QtGui.QAction("Open File",self)
		openMarkDownFileAction.setShortcut("ctrl+shift+o")
		openMarkDownFileAction.setStatusTip("Open a file in markdown editor.")
		openMarkDownFileAction.triggered.connect(self.openMarkEditorFile_)

		selectedTextSearchAction = QtGui.QAction("DuckDuckGo selected text.", self)
		selectedTextSearchAction.setShortcut("alt+d")
		selectedTextSearchAction.triggered.connect(self.selectedTextSearch_)
		
		stackOverflowAction = QtGui.QAction("Search stackOverflow", self)
		stackOverflowAction.setShortcut("alt+s")
		stackOverflowAction.triggered.connect(self.stackOverFlowSearch_)

		gitHubAction = QtGui.QAction("Search GitHub", self)
		gitHubAction.setShortcut("alt+g")
		gitHubAction.triggered.connect(self.gitHubSearch_)

#-------------------//Tool Menu Actions//-----------------#	

#-----------------Misc. Actions and Signals---------------#
		
		self.tabWidget.currentChanged.connect(self.nameOfWindow_)

		nextTabAction = QtGui.QAction(self)
		nextTabAction.setShortcut("Ctrl+t")
		nextTabAction.triggered.connect(self.nextTab_)
		
		prevTabAction = QtGui.QAction(self)
		prevTabAction.setShortcut("Ctrl+shift+t")
		prevTabAction.triggered.connect(self.prevTab_)

#--------------//Misc. Actions and Signals//--------------#	

#--------------------File Menu Actions-------------------#

		newTabAction = QtGui.QAction("New File",self)
		newTabAction.setShortcut("Ctrl+e")
		newTabAction.setStatusTip("Create a new Document")
		newTabAction.triggered.connect(lambda: self.newFile_(insertAction, readOnlyAction, autoIndentAction))

		newWinAction = QtGui.QAction("New Window",self)
		newWinAction.setShortcut("Ctrl+n")
		newWinAction.setStatusTip("Open a new document in a new window")
		newWinAction.triggered.connect(self.newWindow_)
		
		openAction = QtGui.QAction("Open",self)
		openAction.setShortcut("Ctrl+o")
		openAction.setStatusTip("Open an existing document")
		openAction.triggered.connect(lambda: self.open_(insertAction, readOnlyAction, autoIndentAction))
		
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

		
		statusBar = self.statusBar()

#---------------------Menu Bar Creation-------------------#

		bar = self.menuBar()
		file = bar.addMenu("File")
		edit = bar.addMenu("Edit")
		format_ = bar.addMenu("Format")
		tools = bar.addMenu("Tools") 

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
		format_.addSeparator()
		tabWidth = format_.addMenu("Tab Width")
		tabWidth.addAction(action2)
		tabWidth.addAction(action4)
		tabWidth.addAction(action8)
		tabWidth.addAction(action12)
		tabWidth.addAction(action16)
		format_.addSeparator()
		format_.addAction(autoIndentAction)

		tools.addAction(terminalAction)
		tools.addSeparator()
		markDown = tools.addMenu("Markdown Editor")
		markDown.addAction(newMarkDownFileAction)
		markDown.addAction(openMarkDownFileAction)
		tools.addSeparator()
		tools.addAction(selectedTextSearchAction)
		tools.addAction(stackOverflowAction)
		tools.addAction(gitHubAction)

#-------------------//Menu Bar Creation//-----------------#
		
		self.view_(insertAction, readOnlyAction, autoIndentAction)

		self.fileList = []

#-------------------Function Declarations-----------------#
	
	def view_(self, insertAction, readOnlyAction, autoIndentAction):
		#these args are supplied for the sake of function 'newAndOpenFuncs_' 
		
		#to createt a new file as soon as the editor is opened
		self.newFile_(insertAction, readOnlyAction, autoIndentAction)
		
		#to show the editor on the screen
		self.show()
	
	def nameOfWindow_(self): 
		"""
			called from the 'currentChanged' signal
			works when the current tab changes

		"""

		#sets the name of the currnt file as title of the window
		self.tab_name = self.tabWidget.tabText(self.tabWidget.currentIndex())
		self.setWindowTitle(self.tab_name + " - bytex")

		#changing the width of margin where numbersa are displayed
		text__edit = self.tabWidget.currentWidget()
		if self.tabWidget.count() > 0:
			text__edit.cursorPositionChanged.connect(self.marginWidth_)

			self.marginWidth_()
			#causes some errors which does not affect the functioning
			#if removed margin size will not automatically dec/inc immediately
			#after the tab change 

		#closes the editor if number of tabs is zero
		if self.tabWidget.count() is 0:
			sys.exit()

	def nextTab_(self):
		"""
			connected to nextTabAction
			to set the next tab active
		"""
		self.tabWidget.setCurrentIndex(self.tabWidget.CurrentIndex() + 1)
	
	def prevTab_(self):
		"""
			connected to prevTabAction
			to set the previous tab active
		"""
		self.tabWidget.setCurrentIndex(self.tabWidget.CurrentIndex() - 1)

	def selectedText_(self):
		"""
			this function returns the selected text
			in the current tab
		"""
		text__edit = self.tabWidget.currentWidget()
		selectedString = text__edit.selectedText()
		return selectedString

	def setDefaultFont_(self, textEdit):
		"""
			this fucntion set the default font
			for the current tab and number margin 
		"""
		try:
			self.font = QtGui.QFont("Ubuntu", 14)
		except:
			self.font = QtGui.QFont("Sans Serif", 14)
		
		textEdit.setFont(self.font)
		textEdit.setMarginsFont(self.font)

	def cursorPosition_(self):
		"""
			this function returns the current position
			of the cursor
		"""
		text__edit = self.tabWidget.currentWidget()
		self.line_, self.index_ = text__edit.getCursorPosition()
		return self.line_, self.index_
	
	def marginWidth_(self):
		"""
			this funciton sets the width of the numbers margin
			in all the tabs
		"""
		text__edit = self.tabWidget.currentWidget()

		#l is the number of lines in the current tab
		l = text__edit.lines()
		if l < 10:
			margin = QtGui.QFontMetrics(self.font).width("0")
		elif l < 100:
			margin = QtGui.QFontMetrics(self.font).width("00")
		elif l < 1000:
			margin = QtGui.QFontMetrics(self.font).width("000")
		elif l < 10000:
			margin = QtGui.QFontMetrics(self.font).width("0000")
		elif l < 100000:
			margin = QtGui.QFontMetrics(self.font).width("00000")
		else:
			margin = QtGui.QFontMetrics(self.font).width("000000000")
		
		text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
		for text_edit in text_edit_s:
   			text_edit.setMarginWidth(1, margin + 5)				

		#PROBLEM in this function BUT the output is correct
		#print(_line, _index) #after commenting the return statement
		#dont know why this function is getting called the no of times
		#that tab has been visited
		#if a tab is visited 3 times this func is getting called 3 times
		#for that tab
		#signal is coming from fucntion 'nameOfWindow_'

	def setMarginNumbers_(self):
		"""
			this functiion set the numbers in the margin
			in all the tabs
		"""
		text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
		for text_edit in text_edit_s:
			text_edit.setMarginLineNumbers(1, True)

	def newAndOpenFuncs_(self, textEdit, insertAction, readOnlyAction, autoIndentAction):
		"""
			these funcs are to be called every time for each
			new tab so that previously active properties may 
			apply to those tabs also 
		"""
		self.setDefaultFont_(textEdit)
		self.setMarginNumbers_()
		self.insert_(insertAction)
		self.readOnly_(readOnlyAction)
		self.setAutoIndent_(autoIndentAction) 

#--------------------File Menu Functions------------------#	
	
	def newFile_(self, insertAction, readOnlyAction, autoIndentAction):
		"""
			this function is connected to 'newTabAction'
		"""

		#adds a new tab
		self.textEdit = Qsci.QsciScintilla(self.tabWidget)
		self.tabWidget.addTab(self.textEdit, "Untitled " + str(self.tabWidget.count()+1))
		
		#to apply prev. active props to newly opened tabs
		self.newAndOpenFuncs_(self.textEdit, insertAction, readOnlyAction, autoIndentAction)


	def open_(self, insertAction, readOnlyAction, autoIndentAction):
		"""
			this function is connnected to 'openAction'
		"""

		#open a file from local storage
		oldFileName = QtGui.QFileDialog.getOpenFileName(self, "Open File")
		file = open(oldFileName, 'r')
		
		#add a new tab to editor
		self.textEdit = Qsci.QsciScintilla(self.tabWidget)
		self.tabWidget.addTab(self.textEdit, os.path.basename(oldFileName))
		
		#append path of this file to a list
		self.fileList.append(oldFileName)

		#read the data from file and set it to editor and close the file
		data = file.read();
		self.textEdit.setText(data)
		file.close()

		#to apply prev. active props to newly opened tabs
		self.newAndOpenFuncs_(self.textEdit, insertAction, readOnlyAction, autoIndentAction)

	def save_(self):
		"""
			this function is connected to 'saveAction'
		"""
		baseNames = []
		
		#storing the names of all open documens
		for file in self.fileList:
			baseNames.append(os.path.basename(file))
		
		#set the name of the tab as the currently opened document
		self.tabName = self.tabWidget.tabText(self.tabWidget.currentIndex())
		
		#save the file with a new name if it does not exist
		if not self.tabName in baseNames:
			self.saveAs_()
		#save it to the path from where it was opened
		else:
			for file_path in self.fileList:
				if self.tabName == os.path.basename(file_path):
					saveFile = open(file_path, 'w')
					data = self.tabWidget.currentWidget().text()					
					saveFile.write(data)
					saveFile.close()

	def saveAs_(self):
		"""
			this funciton is connected to 'saveAsAction'
		"""

		#open a file from local storage
		newFileName = QtGui.QFileDialog.getSaveFileName(self, "Save File")
		file = open(newFileName, 'w')
		
		self.tabWidget.setTabText(self.tabWidget.currentIndex(), os.path.basename(newFileName))
		self.setWindowTitle(newFileName + " - bytex")
		
		#append path of this file to a list
		self.fileList.append(newFileName)	

		#get the data from editor and write it to file and close the file
		data = self.tabWidget.currentWidget().text()
		file.write(data)
		file.close()
	
	def newWindow_(self):
		"""
			this function is connected to 'newWinAction'
		"""
		# call a new Editor object to create a new window
		Editor()

	def closeTab_(self):
		"""
			this fucntion is connected to 'closeAction'
		"""

		#removes the current tab
		self.tabWidget.removeTab(self.tabWidget.currentIndex())

		#if tab count is zero close the editor
		if self.tabWidget.count() == 0:
			sys.exit()

	def closeEditor_(self):
		"""
			this function is connected to 'closeAction'
		"""
		
		#close the editor
		sys.exit()

#------------------//File Menu Functions//----------------#

#--------------------Edit Menu Functions------------------#

	def undo_(self):
		"""
			this function is connected to 'undoAction'
		"""
		
		#undo the current change
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.undo()

	def redo_(self):
		"""
			this function is connected to 'redoAction'
		"""
		
		#redo the last change
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.redo()
	
	def cut_(self):
		"""
			this function is connected to 'cutAction'
		"""
		
		#cut the selected text from the current tab
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.cut()
	
	def copy_(self):
		"""
			this function is connected to 'copyAction'
		"""
		
		#copy the selected text from the current tab
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.copy()
	
	def paste_(self):
		"""
			this function is connected to 'pasteAction'
		"""
		
		#paste the selected text from the current tab
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.paste()
	
	def readOnly_(self, readOnlyAction):
		"""
			this function is connected to 'readOnlyAction'
		"""
		
		#set the text in all tabs to readOnly
		if readOnlyAction.isChecked() is True:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:	
				text_edit.setReadOnly(True)
		#undo the readOnly action
		else:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				text_edit.setReadOnly(False)
	
	def selectAll_(self):
		"""
			this function is connected to 'selectAllAction'
		"""
		
		#select all the text from the current tab
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.selectAll()
	
	def clear_(self):
		"""
			this function is connected to 'clearAction'
		"""
		
		#clear all the text from the current tab
		self.text_edit = self.tabWidget.currentWidget()
		self.text_edit.clear()
	
	def insert_(self, insertAction):
		"""
			this function is connected to 'insertAction'
		"""
		
		#enable the insert mode in all the tabs
		if insertAction.isChecked() is True:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
   				text_edit.setOverwriteMode(True)
		#disable the insert mode in all tabs
		else:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
   				text_edit.setOverwriteMode(False)

#------------------//Edit Menu Functions//----------------#

#-------------------Format Menu Functions-----------------#	

	def setFont_(self):
		"""
			this function is connected to fontAciton
		"""

		#opens a dialog to choose font, font-style and font-size from
		font, true = QtGui.QFontDialog.getFont()
		if true:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				text_edit.setFont(font)
	
	def setTabWidth_(self,tab_action_group, action2, action4, action8, action12, action16):
		"""
			this function is connected to 'tab_action_group'
		"""

		#set the tab width and indentation width
		if tab_action_group.checkedAction() is action2:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				text_edit.setTabWidth(2)
				text_edit.setIndentationWidth(2)
		elif tab_action_group.checkedAction() is action4:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				text_edit.setTabWidth(4)
				text_edit.setIndentationWidth(4)
		elif tab_action_group.checkedAction() is action8:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				text_edit.setTabWidth(8)
				text_edit.setIndentationWidth(8)
		elif tab_action_group.checkedAction() is action12:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				text_edit.setTabWidth(12)
				text_edit.setIndentationWidth(12)
		elif tab_action_group.checkedAction() is action16:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				text_edit.setTabWidth(16)
				text_edit.setIndentationWidth(16)
	
	def setAutoIndent_(self, autoIndentAction):
		"""
			this function is connected to 'autoIndentAction'
		"""

		#enables the auto indentation
		if autoIndentAction.isChecked() is True:
				text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
				for text_edit in text_edit_s:
					text_edit.setAutoIndent(True)
		#disables the auto indentation
		else:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				text_edit.setAutoIndent(False)

#-----------------//Format Menu Functions//---------------#	
		
#--------------------Tool Menu Functions------------------#
	
	def openBash_(self):
		"""
			this function is connected to 'terminalAction'
			it opens the bash with the current directioy set 
			to the location of the file if it exists else in the home
		"""

		self.tabName = self.tabWidget.tabText(self.tabWidget.currentIndex())
		
		flag=0

		#if file name exists in the path list, open bash in the path
		for path_ in self.fileList:
			if self.tabName == os.path.basename(path_):
				os.system("gnome-terminal -e 'bash -c \"cd {}; exec bash\"'".format(path_[0:len(path_)-len(os.path.basename(path_))]))
				flag=1
				break
		#else in the home directory
		if flag == 0:
			os.system("gnome-terminal -e 'bash -c \"cd ~/; exec bash\"'")

	def openMarkEditor_(self):
		"""
			this function is connected to 'newMarkDownFileAction'
			it opens a markdown editor with an empty screen in the 
			webbrowser
		"""

		#os.system("gnome-terminal -e 'bash -c \"markdown_edit; exec bash\"'")
		#either ^ or v
		subprocess.Popen("markdown_edit")

	def openMarkEditorFile_(self):
		"""
			this function is connected to 'openMarkDownFileAction'
			it opens a file to edit in the markdown editor
		"""
		mFilePath = QtGui.QFileDialog.getOpenFileName(self, "Open File")
		os.system("gnome-terminal -e 'bash -c \"markdown_edit {}; exec bash\"'".format(mFilePath))
		

	def selectedTextSearch_(self):
		"""
			this function is connected to 'selectedTextSearchAction'
			it searches the selected text on the screen on DuckDuckGo
		"""
		searchString = self.selectedText_()
		if searchString == "":
			pass
		else:
			webbrowser.open("https://duckduckgo.com/?q={}&t=hs&ia=web".format(searchString))			

	def stackOverFlowSearch_(self):
		"""
			this function is connected to 'stackOverflowAction'
			this function opens a input dialog box in you can 
			write relevnt keywords to dearch on stackoverflow 
		"""

		searchString, true = QtGui.QInputDialog.getText(self, 'stackOverflow.com', 'Enter query')
		if true:
			webbrowser.open("http://stackoverflow.com/search?q={}".format(searchString))
		else:
			pass
	def gitHubSearch_(self):
		"""
			this function is connected to 'gitHubAction'
			this function opens a input dialog box from which you 
			can seach anything on github 
		"""

		searchString, true = QtGui.QInputDialog.getText(self, 'github.com', 'Enter query')
		if true:
			webbrowser.open("https://github.com/search?utf8=✓&q={}".format(searchString))
		else:
			pass
#------------------//Tool Menu Functions//----------------#

def run():
	app = QtGui.QApplication(sys.argv)
	new_editor = Editor()
	sys.exit(app.exec_())

run()