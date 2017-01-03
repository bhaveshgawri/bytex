import sys,  os, webbrowser, subprocess
from PyQt4 import QtGui, QtCore, Qsci
from markdown_editor import web_edit

class Editor(QtGui.QMainWindow):
	def __init__(self):
		super(Editor, self).__init__()
		#print (help(lexers))
		self.setGeometry(0,0, 800, 1000)
		self.setMinimumSize(600,350)
		self.setWindowTitle("bytex")		
		self.setWindowIcon(QtGui.QIcon("./icon.jpg"))
		
		self.tabWidget = QtGui.QTabWidget(self)
		self.setCentralWidget(self.tabWidget)
		self.tabWidget.setTabsClosable(True)
		self.tabWidget.setMovable(True)
		#self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)

		self.statusBar = QtGui.QStatusBar(self)	
		self.setStatusBar(self.statusBar)
		self.cursor_position = QtGui.QLabel("")
		self.statusBar.addPermanentWidget(self.cursor_position)

#--------------------Edit Menu Actions-------------------#

		undoAction = QtGui.QAction("Undo",self)
		undoAction.setShortcut("Ctrl+z")
		undoAction.setStatusTip("Undo the last change.")
		undoAction.triggered.connect(self.undo_)
		undoAction.hovered.connect(lambda: self.toolTip_("Undo the last change."))
		
		redoAction = QtGui.QAction("Redo",self)
		redoAction.setShortcut("Ctrl+Shift+z")
		redoAction.setStatusTip("Redo the last change.")
		redoAction.triggered.connect(self.redo_)
		redoAction.hovered.connect(lambda: self.toolTip_("Redo the last change."))

		cutAction = QtGui.QAction("Cut",self)
		cutAction.setShortcut("Ctrl+x")
		cutAction.setStatusTip("Cut the selected text.")
		cutAction.triggered.connect(self.cut_)
		cutAction.hovered.connect(lambda: self.toolTip_("Cut the selected text."))
		
		copyAction = QtGui.QAction("Copy",self)
		copyAction.setShortcut("Ctrl+c")
		copyAction.setStatusTip("Copy the selected text.")
		copyAction.triggered.connect(self.copy_)
		copyAction.hovered.connect(lambda: self.toolTip_("Copy the selected text."))
		
		pasteAction = QtGui.QAction("Paste",self)
		pasteAction.setShortcut("Ctrl+v")
		pasteAction.setStatusTip("Paste the text on clipboard at position of cursor.")
		pasteAction.triggered.connect(self.paste_)
		pasteAction.hovered.connect(lambda: self.toolTip_("Paste Text"))
		
		readOnlyAction = QtGui.QAction("Read Only",self, checkable = True)
		readOnlyAction.setStatusTip("Make text read-only.")
		readOnlyAction.triggered.connect(lambda: self.readOnly_(readOnlyAction))

		selectAllAction = QtGui.QAction("Select All",self)
		selectAllAction.setShortcut("Ctrl+a")
		selectAllAction.setStatusTip("Select all the text.")
		selectAllAction.triggered.connect(self.selectAll_)
		selectAllAction.hovered.connect(lambda: self.toolTip_("Select all the text."))

		clearAction = QtGui.QAction("Clear Screen",self)
		clearAction.setShortcut("Ctrl+l")
		clearAction.setStatusTip("Clear all the text from screen.")
		clearAction.triggered.connect(self.clear_)
		clearAction.hovered.connect(lambda: self.toolTip_("Clear all the text from screen."))

		insertAction = QtGui.QAction("Insert Mode",self, checkable = True)
		insertAction.setStatusTip("Toggle Insert Mode for all tabs.")
		insertAction.triggered.connect(lambda: self.insert_(insertAction))

#-------------------//Edit Menu Actions//-----------------#

#--------------------Format Menu Actions------------------#	

		fontAction = QtGui.QAction("Fonts", self)
		fontAction.setStatusTip("Set the font type, style and size.")
		fontAction.triggered.connect(self.setFont_)
		fontAction.hovered.connect(lambda: self.toolTip_("Set the font type, style and size."))

		tab_action_group = QtGui.QActionGroup(self, exclusive = True)
		action2 = tab_action_group.addAction(QtGui.QAction("Tab Width:2", self, checkable=True))
		action4 = tab_action_group.addAction(QtGui.QAction("Tab Width:4", self, checkable=True))
		action8 = tab_action_group.addAction(QtGui.QAction("Tab Width:8", self, checkable=True))
		action12 = tab_action_group.addAction(QtGui.QAction("Tab Width:12", self, checkable=True))
		action16 = tab_action_group.addAction(QtGui.QAction("Tab Width:16", self, checkable=True))
		tab_action_group.triggered.connect(lambda: self.setTabWidth_(tab_action_group, action2,
			action4, action8, action12, action16
			))

		autoIndentAction = QtGui.QAction("Auto Indent", self, checkable = True)
		autoIndentAction.setChecked(True)
		autoIndentAction.setStatusTip("Toggle Auto Indentation")
		autoIndentAction.triggered.connect(lambda: self.setAutoIndent_(autoIndentAction))

		darkModeAction = QtGui.QAction("Dark Mode", self, checkable = True)
		darkModeAction.setStatusTip("Toggle Dark Mode")
		darkModeAction.setChecked(True)
		darkModeAction.triggered.connect(lambda: self.darkMode_(darkModeAction))

#------------------//Format Menu Actions//----------------#

#---------------------Tool Menu Actions-------------------#
		
		terminalAction = QtGui.QAction("Open bash here", self)
		terminalAction.setShortcut("shift+alt+t")
		terminalAction.setStatusTip("Open bash at the locaiton of active file.")
		terminalAction.triggered.connect(self.openBash_)
		terminalAction.hovered.connect(lambda: self.toolTip_("Open bash at the locaiton of file in current tab."))

		newMarkDownFileAction = QtGui.QAction("Try Now",self)
		newMarkDownFileAction.setShortcut("ctrl+shift+n")
		newMarkDownFileAction.setStatusTip("Try the markdown editor now.")
		newMarkDownFileAction.triggered.connect(self.openMarkEditor_)
		newMarkDownFileAction.hovered.connect(lambda: self.toolTip_("Try the markdown editor now."))

		openMarkDownFileAction = QtGui.QAction("Open File",self)
		openMarkDownFileAction.setShortcut("ctrl+shift+o")
		openMarkDownFileAction.setStatusTip("Open a file in markdown editor.")
		openMarkDownFileAction.triggered.connect(self.openMarkEditorFile_)
		openMarkDownFileAction.hovered.connect(lambda: self.toolTip_("Open a file in markdown editor."))

		selectedTextSearchAction = QtGui.QAction("DuckDuckGo selected text.", self)
		selectedTextSearchAction.setShortcut("alt+d")
		selectedTextSearchAction.triggered.connect(self.selectedTextSearch_)
		selectedTextSearchAction.hovered.connect(lambda: self.toolTip_("Select text and click to go ducky"))

		stackOverflowAction = QtGui.QAction("Search stackoverflow", self)
		stackOverflowAction.setShortcut("alt+s")
		stackOverflowAction.setStatusTip("Search questions on stackoverflow for requried word(s)")
		stackOverflowAction.triggered.connect(self.stackOverFlowSearch_)
		stackOverflowAction.hovered.connect(lambda: self.toolTip_("Search questions on stackoverflow for requried word(s)"))

		gitHubAction = QtGui.QAction("Search GitHub", self)
		gitHubAction.setShortcut("alt+g")
		openMarkDownFileAction.setStatusTip("Search for code or user on GitHub")
		gitHubAction.triggered.connect(self.gitHubSearch_)
		gitHubAction.hovered.connect(lambda: self.toolTip_("Search for code or user on GitHub"))

#-------------------//Tool Menu Actions//-----------------#	

#----------------------bytex Actions----------------------#
		
		helpAction = QtGui.QAction("Help?",self)
		helpAction.setStatusTip("Need Some Help")
		helpAction.triggered.connect(self.help_)
		helpAction.hovered.connect(lambda: self.toolTip_("Need some help?"))

		contributeAction = QtGui.QAction("Contribute!",self)
		contributeAction.setStatusTip("Make bytex better.")
		contributeAction.triggered.connect(self.contribute_)
		contributeAction.hovered.connect(lambda: self.toolTip_("Make bytex better."))

#--------------------//bytex Actions//--------------------#	

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
		newTabAction.setStatusTip("Create a new file")
		newTabAction.triggered.connect(lambda: self.newFile_(insertAction, readOnlyAction,
			autoIndentAction,tab_action_group, action2, action4, action8, action12, action16,
			darkModeAction
			))
		newTabAction.hovered.connect(lambda: self.toolTip_("Create a new file"))

		XTerminalAction = QtGui.QAction("New xTab", self)
		XTerminalAction.setShortcut("shift+alt+x")
		XTerminalAction.setStatusTip("Open XTerm in a new tab.")
		XTerminalAction.triggered.connect(self.xTab_)
		XTerminalAction.hovered.connect(lambda: self.toolTip_("Open XTerm"))

		newWinAction = QtGui.QAction("New Window",self)
		newWinAction.setShortcut("Ctrl+n")
		newWinAction.setStatusTip("Open a new bytex Window")
		newWinAction.triggered.connect(self.newWindow_)
		newWinAction.hovered.connect(lambda: self.toolTip_("Open a new bytex Window"))
		
		openAction = QtGui.QAction("Open",self)
		openAction.setShortcut("Ctrl+o")
		openAction.setStatusTip("Open an existing file")
		openAction.triggered.connect(lambda: self.open_(insertAction, readOnlyAction, 
			autoIndentAction,tab_action_group, action2, action4, action8, action12, action16,
			darkModeAction
			))
		openAction.hovered.connect(lambda: self.toolTip_("Open other file"))
		
		saveAction = QtGui.QAction("Save",self)
		saveAction.setShortcut("Ctrl+s")
		saveAction.setStatusTip("Save this file")
		saveAction.triggered.connect(lambda: self.save_(darkModeAction))
		saveAction.hovered.connect(lambda: self.toolTip_("Save this file"))
		
		saveAsAction = QtGui.QAction("Save As...",self)
		saveAsAction.setShortcut("Ctrl+Shift+s")
		saveAsAction.setStatusTip("Save this file as...")
		saveAsAction.triggered.connect(lambda: self.saveAs_(darkModeAction))
		saveAsAction.hovered.connect(lambda: self.toolTip_("Save currennt file with different name"))
		
		closeAction = QtGui.QAction("Close",self)
		closeAction.setShortcut("Ctrl+w")
		closeAction.setStatusTip("Close the current tab")
		closeAction.triggered.connect(self.closeTab_)
		self.tabWidget.tabCloseRequested.connect(self.tabWidget.removeTab)
		#  ^without this line 'x' on tabs won't work.
		closeAction.hovered.connect(lambda: self.toolTip_("Close the current tab"))

		quitAction = QtGui.QAction("Quit",self)
		quitAction.setShortcut("Ctrl+q")
		quitAction.setStatusTip("Close all tabs and EXIT.")
		quitAction.triggered.connect(self.closeEditor_)
		quitAction.hovered.connect(lambda: self.toolTip_("Close all tabs"))

#------------------//File Menu Actions//-----------------#


#---------------------Menu Bar Creation-------------------#

		bar = self.menuBar()
		file = bar.addMenu("File")
		edit = bar.addMenu("Edit")
		format_ = bar.addMenu("Format")
		tools = bar.addMenu("Tools") 
		bytex = bar.addMenu("bytex")

		file.addAction(newTabAction)
		file.addAction(XTerminalAction)
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
		format_.addSeparator()
		format_.addAction(darkModeAction)

		tools.addAction(terminalAction)
		tools.addSeparator()
		markDown = tools.addMenu("Markdown Editor")
		markDown.addAction(newMarkDownFileAction)
		markDown.addAction(openMarkDownFileAction)
		tools.addSeparator()
		tools.addAction(selectedTextSearchAction)
		tools.addAction(stackOverflowAction)
		tools.addAction(gitHubAction)

		bytex.addAction(helpAction)
		bytex.addAction(contributeAction)

#-------------------//Menu Bar Creation//-----------------#
		
		self.view_(insertAction, readOnlyAction, autoIndentAction,
			tab_action_group, action2, action4, action8, action12, action16,
			darkModeAction
			)
		
		self.fileList = []

#===================Function Declarations=================#


#----------------------MISC. Functions--------------------#
	
	def view_(self, insertAction, readOnlyAction, autoIndentAction
		,tab_action_group, action2, action4, action8, action12, action16,
		darkModeAction
		):
		#these args are supplied for the sake of function 'newAndOpenFuncs_' 
		
		#to createt a new file as soon as the editor is opened
		self.newFile_(insertAction, readOnlyAction, autoIndentAction,
			tab_action_group, action2, action4, action8, action12, action16,
			darkModeAction
			)
		
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
		
		if type(self.tabWidget.currentWidget()) == Qsci.QsciScintilla:
			#changing the width of margin where numbersa are displayed
			textEdit = self.tabWidget.currentWidget()
			if self.tabWidget.count() > 0:
				textEdit.cursorPositionChanged.connect(self.marginWidth_)
				self.marginWidth_()#when tab changes

				#update the cursor position
				textEdit.cursorPositionChanged.connect(self.cursorPosition_)
				self.cursorPosition_()#when tab changes
		else:
			self.cursor_position.setText("Line: - Index: -")

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
		textEdit = self.tabWidget.currentWidget()
		selectedString = textEdit.selectedText()
		return selectedString

	def setDefaultFont_(self, textEdit):
		"""
			this fucntion set the default font
			for the current tab and number margin 
		"""
		try:
			font = QtGui.QFont("ubuntu", 14)
		except:
			font = QtGui.QFont("calibri", 14)
		
		textEdit.setFont(font)
		textEdit.setMarginsFont(font)

	def cursorPosition_(self):
		"""
			this function sets the current position
			of the cursor on status bar
			connected with 'cursorPositionChanged' signal
			in nameOfWindow_ function and is called when cursor 
			position changes
		"""
		
		#setting cursor position on status bar
		if type(self.tabWidget.currentWidget()) == Qsci.QsciScintilla:
			textEdit = self.tabWidget.currentWidget()
			line_, index_ = textEdit.getCursorPosition()
			self.cursor_position.setText("Line: {} Index: {}".format(line_, index_))
		else:
			pass
			#this part is written in nameOfWindow_() function

	def marginWidth_(self):
		"""
			this funciton sets the width of the numbers margin
			in all the tabs
			connected with 'cursorPositionChanged' signal
			in nameOfWindow_ function
		"""
		textEdit = self.tabWidget.currentWidget()
		try:
			font = QtGui.QFont("ubuntu", 14)
		except:
			font = QtGui.QFont("calibri", 14)
		#l is the number of lines in the current tab
		l = textEdit.lines()
		if l < 10:
			margin = QtGui.QFontMetrics(font).width("0")
		elif l < 100:
			margin = QtGui.QFontMetrics(font).width("00")
		elif l < 1000:
			margin = QtGui.QFontMetrics(font).width("000")
		elif l < 10000:
			margin = QtGui.QFontMetrics(font).width("0000")
		elif l < 100000:
			margin = QtGui.QFontMetrics(font).width("00000")
		elif l < 1000000:
			margin = QtGui.QFontMetrics(font).width("000000")
		elif l < 10000000:
			margin = QtGui.QFontMetrics(font).width("0000000")
		else:
			margin = QtGui.QFontMetrics(font).width("000000000")
		
		text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
		for text_edit in text_edit_s:
			if type(text_edit) == Qsci.QsciScintilla:
				text_edit.setMarginWidth(1, margin + 10)

		#PROBLEM in this function BUT the output is correct
		#try printing something and see output no console
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
			if type(text_edit) == Qsci.QsciScintilla:
				text_edit.setMarginLineNumbers(1, True)

	def newAndOpenFuncs_(self, textEdit, insertAction, readOnlyAction, autoIndentAction,
		tab_action_group, action2, action4, action8, action12, action16,
		darkModeAction
		):
		"""
			these funcs are to be called every time for each
			new tab so that previously active properties may 
			apply to those tabs also 
		"""
		#some default values
		textEdit.setUtf8(True)
		self.setDefaultFont_(textEdit)
		self.setMarginNumbers_()
		self.insert_(insertAction)
		self.readOnly_(readOnlyAction)
		self.setTabWidth_(tab_action_group, action2, action4, action8, action12, action16)
		self.setAutoIndent_(autoIndentAction)
		textEdit.setIndentationGuides(True)
		textEdit.setCaretLineVisible(True)
		textEdit.setFolding(Qsci.QsciScintilla.BoxedTreeFoldStyle, 2)
		textEdit.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)
		self.genColorProps_(textEdit, darkModeAction)
		
		#auto completion
		textEdit.setAutoCompletionSource(Qsci.QsciScintilla.AcsDocument)
		textEdit.setAutoCompletionThreshold(2)
		textEdit.setAutoCompletionReplaceWord(True)
		textEdit.setAutoCompletionFillupsEnabled(True)
		textEdit.setAutoCompletionCaseSensitivity(True)

	def toolTip_(self, s):
		"""
			this function shows the tooltips 
			when menubar items are hovered
		"""

		QtGui.QToolTip.showText(QtGui.QCursor.pos(), s)

#--------------------//MISC. Functions//-------------------#

#--------------------lexers and lexfuncs-------------------#

	def genColorProps_(self, textEdit, darkModeAction):
		"""
			This function gives color to different elements
			of the text editor in :

		"""
		# the dark mode
		if darkModeAction.isChecked() is True:
			textEdit.setMarginsForegroundColor(QtGui.QColor("white"))
			textEdit.setMarginsBackgroundColor(QtGui.QColor("#333333"))

			textEdit.setPaper(QtGui.QColor("#333333"))
			textEdit.setColor(QtGui.QColor("white"))

			textEdit.setIndentationGuidesBackgroundColor(QtGui.QColor("#666666"))
			#textEdit.setIndentationGuidesForegroundcolor(QtGui.QColor())

			textEdit.setCaretLineBackgroundColor(QtGui.QColor("#444444"))
			textEdit.setFoldMarginColors(QtGui.QColor("#444444"),QtGui.QColor("#444444"))

			textEdit.setMatchedBraceBackgroundColor(QtGui.QColor("#444444"))
			textEdit.setMatchedBraceForegroundColor(QtGui.QColor("red"))
			textEdit.setUnmatchedBraceBackgroundColor(QtGui.QColor("#444444"))
			textEdit.setUnmatchedBraceForegroundColor(QtGui.QColor("white"))

		# in light mode
		elif darkModeAction.isChecked() is False:
			textEdit.setMarginsForegroundColor(QtGui.QColor("black"))
			textEdit.setMarginsBackgroundColor(QtGui.QColor("#dddddd"))

			textEdit.setPaper(QtGui.QColor("white"))
			textEdit.setColor(QtGui.QColor("black"))

			textEdit.setIndentationGuidesBackgroundColor(QtGui.QColor("#eeeeee"))

			textEdit.setCaretLineBackgroundColor(QtGui.QColor("#eeeeee"))
			textEdit.setFoldMarginColors(QtGui.QColor("#eeeeee"),QtGui.QColor("#eeeeee"))

			textEdit.setMatchedBraceBackgroundColor(QtGui.QColor("#eeeeee"))
			textEdit.setMatchedBraceForegroundColor(QtGui.QColor("red"))
			textEdit.setUnmatchedBraceBackgroundColor(QtGui.QColor("#eeeeee"))
			textEdit.setUnmatchedBraceForegroundColor(QtGui.QColor("black"))


	def darkMode_(self, darkModeAction):
		"""
			Activated by darkModeAction
			responsible for change in colors when 
			Dark Mode gets checked.
		"""

		text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
		for text_edit in text_edit_s:
			if type(text_edit) == Qsci.QsciScintilla:
				self.callLexers_(text_edit, self.tabWidget.indexOf(text_edit), darkModeAction)
				self.genColorProps_(text_edit, darkModeAction)

	def callLexers_(self, textEdit, text_edit_index, darkModeAction):
		#calling lexers of different languages
		self.pyLexer_(textEdit, text_edit_index, darkModeAction)
		self.cLexer_(textEdit, text_edit_index, darkModeAction)
		self.javaLexer_(textEdit, text_edit_index, darkModeAction)
		self.jsLexer_(textEdit, text_edit_index, darkModeAction)
		self.htmlLexer_(textEdit, text_edit_index, darkModeAction)
		self.cssLexer_(textEdit, text_edit_index, darkModeAction)
		self.xmlLexer_(textEdit, text_edit_index, darkModeAction)

	def lex_ex_(self, text_edit_index, ex):
		"""
			returns true if extension of tab
			with index 'text_edit_index' is equal
			to ex else returns false
		"""
		
		if self.tabWidget.tabText(text_edit_index).endswith("."+ex):
			return True
		else:
			return False

	#python lexer
	def pyLexer_(self, text_edit, text_edit_index, darkModeAction):
		lexer = Qsci.QsciLexerPython()
		lexer.setFont(QtGui.QFont("ubuntu", 13))
		if darkModeAction.isChecked() is True:
			lexer.setPaper(QtGui.QColor("#333333"))
			lexer.setColor(QtGui.QColor("#000000"), 1)   #comment
			lexer.setColor(QtGui.QColor("orange"), 2) 	 #number
			lexer.setColor(QtGui.QColor("#FFFF47"), 3) 	 #  ' '
			lexer.setColor(QtGui.QColor("#FFFF47"), 4) 	 #  " "
			lexer.setColor(QtGui.QColor("cyan"), 5)		 #keyword
			lexer.setColor(QtGui.QColor("#000000"), 6)   #  '''
			lexer.setColor(QtGui.QColor("#000000"), 7)	 #  """
			lexer.setColor(QtGui.QColor("#ADFF2F"), 8) 	 #class
			lexer.setColor(QtGui.QColor("#ADFF2F"), 9) 	 #function
			lexer.setColor(QtGui.QColor("#C0C0C0"), 10)	 #operator
			lexer.setColor(QtGui.QColor("white"), 11)	 #identifier
		

		if self.lex_ex_( text_edit_index,"py") or self.lex_ex_(text_edit_index,"py3"):
			text_edit.setLexer(lexer)

	#c and cpp lexer
	def cLexer_(self, text_edit, text_edit_index, darkModeAction):
		lexer = Qsci.QsciLexerCPP()
		try:
			font = QtGui.QFont("ubuntu", 14)
		except:
			font = QtGui.QFont("calibri", 14)
		lexer.setFont(font)
		if darkModeAction.isChecked() is True:
			lexer.setPaper(QtGui.QColor("#333333"))
			lexer.setColor(QtGui.QColor("#000000"), 1)   #comment
			lexer.setColor(QtGui.QColor("orange"), 4) 	 #number
			lexer.setColor(QtGui.QColor("#FFFF47"), 6)	 #  " "
			lexer.setColor(QtGui.QColor("#FFFF47"), 7) 	 #  ' '
			lexer.setColor(QtGui.QColor("red"), 12)	 	 #  '... or "...  
			lexer.setColor(QtGui.QColor("#FFFF47"), 20)	 #raw string
			lexer.setColor(QtGui.QColor("cyan"), 5)		 #keyword
			lexer.setColor(QtGui.QColor("#000000"), 2)   #comment line
			lexer.setColor(QtGui.QColor("#000000"), 3)	 #comment doc
			lexer.setColor(QtGui.QColor("#ADFF2F"),19) 	 #global class
			lexer.setColor(QtGui.QColor("#ADFF2F"), 9) 	 #preprocessor
			lexer.setColor(QtGui.QColor("#C0C0C0"), 10)	 #operator
			lexer.setColor(QtGui.QColor("white"), 11)	 #identifier
			lexer.setColor(QtGui.QColor("purple"), 27)	 #escape seq

		if self.lex_ex_(text_edit_index,"c") or self.lex_ex_(text_edit_index,"cpp") or self.lex_ex_(text_edit_index,"h"):
			text_edit.setLexer(lexer)

	#java lexer
	def javaLexer_(self, text_edit, text_edit_index, darkModeAction):
		lexer = Qsci.QsciLexerJava()
		try:
			font = QtGui.QFont("ubuntu", 14)
		except:
			font = QtGui.QFont("calibri", 14)
		lexer.setFont(font)
		if darkModeAction.isChecked() is True:
			lexer.setPaper(QtGui.QColor("#333333"))
			lexer.setColor(QtGui.QColor("#000000"), 1)   #comment
			lexer.setColor(QtGui.QColor("orange"), 4) 	 #number
			lexer.setColor(QtGui.QColor("#FFFF47"), 6)	 #  " "
			lexer.setColor(QtGui.QColor("#FFFF47"), 7) 	 #  ' '
			lexer.setColor(QtGui.QColor("red"), 12)		 #  '... or "...  
			lexer.setColor(QtGui.QColor("#FFFF47"), 20)	 #raw string
			lexer.setColor(QtGui.QColor("cyan"), 5)		 #keyword
			lexer.setColor(QtGui.QColor("#000000"), 2)   #comment line
			lexer.setColor(QtGui.QColor("#000000"), 3)	 #comment doc
			lexer.setColor(QtGui.QColor("#ADFF2F"),19) 	 #global class
			lexer.setColor(QtGui.QColor("#ADFF2F"), 9) 	 #preprocessor
			lexer.setColor(QtGui.QColor("#C0C0C0"), 10)	 #operator
			lexer.setColor(QtGui.QColor("white"), 11)	 #identifier
			lexer.setColor(QtGui.QColor("purple"), 27)	 #escape seq

		if self.lex_ex_(text_edit_index,"java"):
			text_edit.setLexer(lexer)

	#javaScript lexer
	def jsLexer_(self, text_edit, text_edit_index, darkModeAction):
		lexer = Qsci.QsciLexerJavaScript()
		try:
			font = QtGui.QFont("ubuntu", 14)
		except:
			font = QtGui.QFont("calibri", 14)
		lexer.setFont(font)
		if darkModeAction.isChecked() is True:
			lexer.setPaper(QtGui.QColor("#333333"))
			lexer.setColor(QtGui.QColor("orange"), 4) 	 #number
			lexer.setColor(QtGui.QColor("#FFFF47"), 6)	 #  " "
			lexer.setColor(QtGui.QColor("#FFFF47"), 7) 	 #  ' '
			lexer.setColor(QtGui.QColor("red"), 12)	 	 #  '... or "...  
			lexer.setColor(QtGui.QColor("#FFFF47"), 20)	 #raw string
			lexer.setColor(QtGui.QColor("cyan"), 5)		 #keyword
			lexer.setColor(QtGui.QColor("#000000"), 2)   #comment line
			lexer.setColor(QtGui.QColor("#000000"), 3)	 #comment doc
			lexer.setColor(QtGui.QColor("#ADFF2F"),19) 	 #global class
			lexer.setColor(QtGui.QColor("#ADFF2F"), 9) 	 #preprocessor
			lexer.setColor(QtGui.QColor("#C0C0C0"), 10)	 #operator
			lexer.setColor(QtGui.QColor("white"), 11)	 #identifier
			lexer.setColor(QtGui.QColor("purple"), 27)	 #escape seq

		if self.lex_ex_(text_edit_index,"js"):
			text_edit.setLexer(lexer)

	#html lexer
	def htmlLexer_(self, text_edit, text_edit_index, darkModeAction):
		lexer = Qsci.QsciLexerHTML()
		try:
			font = QtGui.QFont("ubuntu", 14)
		except:
			font = QtGui.QFont("calibri", 14)
		lexer.setFont(font)
		if darkModeAction.isChecked() is True:
			lexer.setPaper(QtGui.QColor("#333333"))
			lexer.setColor(QtGui.QColor("white"), 1)				
			"""
			visit:

			http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciLexerHTML.html
			
			and fill your own values acc. to your choice OR
			use light mode.
			"""

		if self.lex_ex_(text_edit_index,"htm") or self.lex_ex_(text_edit_index,"html"):
			text_edit.setLexer(lexer)

	#css lexer
	def cssLexer_(self, text_edit, text_edit_index, darkModeAction):
		lexer = Qsci.QsciLexerCSS()
		try:
			font = QtGui.QFont("ubuntu", 14)
		except:
			font = QtGui.QFont("calibri", 14)
		lexer.setFont(font)
		if darkModeAction.isChecked() is True:
			lexer.setPaper(QtGui.QColor("#333333"))
			"""
			visit:

			http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciLexerCSS.html
			
			and fill your own values acc. to your choice OR
			use light mode.
			"""

		if self.lex_ex_(text_edit_index,"css"):
			text_edit.setLexer(lexer)

	#xml lexer
	def xmlLexer_(self, text_edit, text_edit_index, darkModeAction):
		lexer = Qsci.QsciLexerXML()
		try:
			font = QtGui.QFont("ubuntu", 14)
		except:
			font = QtGui.QFont("calibri", 14)
		lexer.setFont(font)
		if darkModeAction.isChecked() is True:
			lexer.setPaper(QtGui.QColor("#333333"))
			lexer.setColor(QtGui.QColor("white"), 1)
			"""
			visit:

			http://pyqt.sourceforge.net/Docs/QScintilla2/classQsciLexerHTML.html
			
			yes enum values types are same as HTML
			and fill your own values acc. to your choice OR
			use light mode.
			"""

		if self.lex_ex_(text_edit_index,"xml"):
			text_edit.setLexer(lexer)

#-----------------//lexers and lexfuncs//-----------------#

#--------------------File Menu Functions------------------#	
	
	def xTab_(self):
		"""
			Starts XTerm in the tab
			Press Ctrl + Right Click while hovering
			on XTerm for more options

		"""

		process  = QtCore.QProcess(self.tabWidget)
		self.xterm = QtGui.QWidget(self.tabWidget)
		self.tabWidget.addTab(self.xterm, "xTerm")
		self.tabWidget.setCurrentWidget(self.xterm)
		process.start('xterm',['-into', str(self.tabWidget.currentWidget().winId())])

	def newFile_(self, insertAction, readOnlyAction, autoIndentAction
		,tab_action_group, action2, action4, action8, action12, action16,
		darkModeAction
		):
		"""
			this function is connected to 'newTabAction'
		"""

		#adds a new tab and set it to current tab
		textEdit = Qsci.QsciScintilla(self.tabWidget)
		self.tabWidget.addTab(textEdit, "Untitled " + str(self.tabWidget.count()+1))
		self.tabWidget.setCurrentWidget	(textEdit)

		#to apply prev. active props to newly opened tabs
		self.newAndOpenFuncs_(textEdit, insertAction, readOnlyAction, autoIndentAction
			,tab_action_group, action2, action4, action8, action12, action16,
			darkModeAction
			)


	def open_(self, insertAction, readOnlyAction, autoIndentAction
		,tab_action_group, action2, action4, action8, action12, action16,
		darkModeAction
		):
		"""
			this function is connnected to 'openAction'
		"""
		
		try:
			#open a file from local storage
			oldFileName = QtGui.QFileDialog.getOpenFileName(self, "Open File")
			file = open(oldFileName, 'r')
		except:
			print("Err... FileNotFoundError.")
			return

		#add a new tab to editor and set it to current tab
		textEdit = Qsci.QsciScintilla(self.tabWidget)
		self.tabWidget.addTab(textEdit, os.path.basename(oldFileName))
		self.tabWidget.setCurrentWidget	(textEdit)

		#append path of this file to a list
		self.fileList.append(oldFileName)

		#calling lexers ion current tab
		text_edit_index = self.tabWidget.currentIndex()
		self.callLexers_(textEdit, text_edit_index, darkModeAction)

		#read the data from file and set it to editor and close the file
		data = file.read();
		textEdit.setText(data)
		file.close()

		#to apply prev. active props to newly opened tabs
		self.newAndOpenFuncs_(textEdit, insertAction, readOnlyAction, autoIndentAction
			,tab_action_group, action2, action4, action8, action12, action16,
			darkModeAction
			)

	def save_(self, darkModeAction):
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
			self.saveAs_(darkModeAction)
		#save it to the path from where it was opened
		else:
			for file_path in self.fileList:
				if self.tabName == os.path.basename(file_path):
					saveFile = open(file_path, 'w')
					data = self.tabWidget.currentWidget().text()					
					saveFile.write(data)
					saveFile.close()

	def saveAs_(self, darkModeAction):
		"""
			this funciton is connected to 'saveAsAction'
		"""

		if type(self.tabWidget.currentWidget()) == Qsci.QsciScintilla:
			
			try:
				#open a file from local storage
				newFileName = QtGui.QFileDialog.getSaveFileName(self, "Save File")
				file = open(newFileName, 'w')
			except:
				print("Err... FileNotFoundError.")
				return

			self.tabWidget.setTabText(self.tabWidget.currentIndex(), os.path.basename(newFileName))
			self.setWindowTitle(newFileName + " - bytex")
			
			#append path of this file to a list
			self.fileList.append(newFileName)	
			
			#get the data from editor and write it to file and close the file
			data = self.tabWidget.currentWidget().text()
			file.write(data)
			file.close()
			
			#calling lexers on current tab
			text_edit = self.tabWidget.currentWidget()
			text_edit_index = self.tabWidget.currentIndex()
			self.callLexers_(text_edit, text_edit_index, darkModeAction)
			self.genColorProps_(text_edit, darkModeAction)

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
		text_edit = self.tabWidget.currentWidget()
		if type(text_edit) == Qsci.QsciScintilla:	
			text_edit.undo()

	def redo_(self):
		"""
			this function is connected to 'redoAction'
		"""
		
		#redo the last change
		text_edit = self.tabWidget.currentWidget()
		if type(text_edit) == Qsci.QsciScintilla:
			text_edit.redo()
	
	def cut_(self):
		"""
			this function is connected to 'cutAction'
		"""
		
		#cut the selected text from the current tab
		text_edit = self.tabWidget.currentWidget()
		if type(text_edit) == Qsci.QsciScintilla:
			text_edit.cut()
	
	def copy_(self):
		"""
			this function is connected to 'copyAction'
		"""
		
		#copy the selected text from the current tab
		text_edit = self.tabWidget.currentWidget()
		if type(text_edit) == Qsci.QsciScintilla:
			text_edit.copy()
	
	def paste_(self):
		"""
			this function is connected to 'pasteAction'
		"""
		
		#paste the selected text from the current tab
		text_edit = self.tabWidget.currentWidget()
		if type(text_edit) == Qsci.QsciScintilla:
			text_edit.paste()
	
	def readOnly_(self, readOnlyAction):
		"""
			this function is connected to 'readOnlyAction'
		"""
		
		#set the text in all tabs to readOnly
		if readOnlyAction.isChecked() is True:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:	
				if type(text_edit) == Qsci.QsciScintilla:
					text_edit.setReadOnly(True)
		#undo the readOnly action
		else:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				if type(text_edit) == Qsci.QsciScintilla:
					text_edit.setReadOnly(False)
	
	def selectAll_(self):
		"""
			this function is connected to 'selectAllAction'
		"""
		
		#select all the text from the current tab
		text_edit = self.tabWidget.currentWidget()
		if type(text_edit) == Qsci.QsciScintilla:
			text_edit.selectAll()
	
	def clear_(self):
		"""
			this function is connected to 'clearAction'
		"""
		
		#clear all the text from the current tab
		text_edit = self.tabWidget.currentWidget()
		if type(text_edit) == Qsci.QsciScintilla:
			text_edit.clear()
	
	def insert_(self, insertAction):
		"""
			this function is connected to 'insertAction'
		"""
		
		#enable the insert mode in all the tabs
		if insertAction.isChecked() is True:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				if type(text_edit) == Qsci.QsciScintilla:	
					text_edit.setOverwriteMode(True)
		#disable the insert mode in all tabs
		else:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				if type(text_edit) == Qsci.QsciScintilla:
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
			text_edit = self.tabWidget.currentWidget()
			if type(text_edit) == Qsci.QsciScintilla:
				text_edit.setFont(font)

	def setTabWidth_(self,tab_action_group, action2, action4, action8, action12, action16):
		"""
			this function is connected to 'tab_action_group'
		"""

		#set the tab width and indentation width
		if tab_action_group.checkedAction() is action2:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				if type(text_edit) == Qsci.QsciScintilla:
					text_edit.setTabWidth(2)
					text_edit.setIndentationWidth(2)
		elif tab_action_group.checkedAction() is action4:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				if type(text_edit) == Qsci.QsciScintilla:
					text_edit.setTabWidth(4)
					text_edit.setIndentationWidth(4)
		elif tab_action_group.checkedAction() is action8:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				if type(text_edit) == Qsci.QsciScintilla:
					text_edit.setTabWidth(8)
					text_edit.setIndentationWidth(8)
		elif tab_action_group.checkedAction() is action12:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				if type(text_edit) == Qsci.QsciScintilla:
					text_edit.setTabWidth(12)
					text_edit.setIndentationWidth(12)
		elif tab_action_group.checkedAction() is action16:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				if type(text_edit) == Qsci.QsciScintilla:
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
				if type(text_edit) == Qsci.QsciScintilla:
					text_edit.setAutoIndent(True)
		#disables the auto indentation
		else:
			text_edit_s = (self.tabWidget.widget(i) for i in range(self.tabWidget.count())) 
			for text_edit in text_edit_s:
				if type(text_edit) == Qsci.QsciScintilla:
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
				os.system("gnome-terminal -e 'bash -c \"cd {}; exec bash\"'".format(
					path_[0:len(path_)-len(os.path.basename(path_))]
					))
				
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

		searchString, true = QtGui.QInputDialog.getText(self, 'stackOverflow.com', 'Search questions on stackoverflow tagged with word(s):')
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

		searchString, true = QtGui.QInputDialog.getText(self, 'github.com', 'Enter of repository or user:')
		if true:
			webbrowser.open("https://github.com/search?utf8=✓&q={}".format(searchString))
		else:
			pass
#------------------//Tool Menu Functions//----------------#

#----------------------bytex Functions--------------------#
	
	def help_(self):
		webbrowser.open("https://github.com/bhaveshgawri/bytex")
	
	def contribute_(self):
		webbrowser.open("https://github.com/bhaveshgawri/bytex")

#--------------------//bytex Functions//------------------#

def run():
	app = QtGui.QApplication(sys.argv)
	new_editor = Editor()
	sys.exit(app.exec_())

run()