# bytex

>**a text editor in pyqt4**


##Prerequisites and Installing

It will work with most of the linux distros and may also work for Windows[not checked].			
Instructions for `apt` based distributions:

You need to have `python3` and `pip3` installed.
```
$ sudo apt update
$ sudo apt install python3-pip
```

Then install `PyQt4` and `PyQy4.Qsci` as:
```
$ sudo apt update
$ sudo apt install python3-pyqt4
$ sudo apt install python3-pyqt4.qsci
```
After that install rest from requirements using pip3:
```
$ sudo pip3 install -r requirements.txt
```
and you are ready to go.

[If your OS does not have `gnome-terminal` and `XTerm` some functions will not work properly.]

## Usage

To start the editor:
```
$ cd path_to_bytex.py
$ python3 bytex.py
```
but more preferrably after installing the requirements download the executable file of bytex from 
[here](https://drive.google.com/open?id=0B1o2cfjSr08fQjJPeEROZUprMDA).

Give it executing permissions if it does not have it.
```
$ chmod 755 path_to_bytex
```

Copy the file to /bin to access it from terminal. 
```
$ sudo cp path_to_bytex /bin
$ bytex
```

and boom...

## Features

* Basic open, save, save as, cut, copy, paste.
* Modes: Read only, Insert, Light-Dark.
* Multiple tab and window support.
* XTerm embedded in tabs to access command line from editor itself (Ctrl+ Right Click on XTerm for more options).
It will work if OS has XTerm.
* Markdown editor to edit and create markdown files with side by side live preview.
* Line numbering, auto-indentation, code-folding, auto-completion, syntax-highlighting[currently for python, c, cpp, java, javascript, HTML, XML, CSS]
* Search GitHub, stackoverflow or any selected text in a tab from editor itself.

## Preview*
######New Tab
[![newTab.png](https://s28.postimg.org/qk1o6za99/new_Tab.png)](https://postimg.org/image/4kv9jrtex/)

######Code Preview
[![codePreview.png](https://s28.postimg.org/iq12ll2gd/code_Preview.png)](https://postimg.org/image/7doh3strd)

######Embedded XTerm
[![XTerm.png](https://s28.postimg.org/t2ryleld9/XTerm.png)](https://postimg.org/image/v7cbmhmzt/)

*[NOTE: Tabs and Menubar may look different in other Operating Systems.]

## Built With

* [PyQt4.QtGui](http://pyqt.sourceforge.net/Docs/PyQt4/qtgui.html) - For the GUI of the text editor
* [PyQt4.Qsci](http://pyqt.sourceforge.net/Docs/QScintilla2/annotated.html) - For lexers and other syntax feature
* [Markdown-Editor](https://github.com/ncornette/Python-Markdown-Editor) - For the markdown editor
