#!/bin/env python3

"""
Read/Display a TSV file in a spreadsheet-like GUI application.
"""

#%% Imports
import pandas as pd
import sys

from csv import QUOTE_NONE
from functools import partial
from PyQt5.QtWidgets import QApplication, qApp, QWidget, QMainWindow, QTableView, QAbstractItemView, QHBoxLayout, QVBoxLayout, QPushButton, QAction, QFileDialog, QMenu
from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem


#%%
readTsv = partial(pd.read_csv, sep='\t', dtype=object, encoding='utf-8', quoting=QUOTE_NONE)


#%% Main Window Widget
class MainWindow(QMainWindow):
    
    def __init__(self):
        #super().__init__()
        super(QMainWindow,self).__init__()
        self.initUI()
    # end def

        
    def initUI(self):               
        self.initMenus()
        
        self.formWidget = TsvViewer()
        self.setCentralWidget(self.formWidget)
        
        self.setGeometry(300, 300, 700, 400)
        self.setWindowTitle('Main Window')
        self.show()
    # end def


    def initMenus(self):
        openAct = QAction('&Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open File...')
        openAct.triggered.connect(self.openFile)

        saveAct = QAction('&Save as...', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip('Save File...')
        saveAct.triggered.connect(self.saveFile)

        exitAct = QAction('&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAct)
        fileMenu.addAction(saveAct)
        fileMenu.addAction(exitAct)
    # end def


    def openFile(self):
        tsvFile,_ = QFileDialog.getOpenFileName(self,"Open TSV file",".","*.tsv")
        if tsvFile:
            self.formWidget.setTsvFile(tsvFile)
    # end def


    def saveFile(self):
        pass
    # end def
    
# end class
    
    
#%% Main Application 
class TsvViewer(QWidget):
    
    def __init__(self):
        super().__init__()
 
        self.tsvFile = None
    
        # CREATE THE TABLE
        self.tableView = QTableView(self)
        self.colHeader = self.tableView.horizontalHeader()
        self.btnRows = QPushButton('Resize Rows to Contents')
        self.btnCols = QPushButton('Resize Columns to Contents')
        self.showHidden = QPushButton('Show hidden columns')
        
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.colHeader.setContextMenuPolicy(Qt.CustomContextMenu)
        self.colHeader.customContextMenuRequested.connect(self.openMenu)
 
        self.setGeometry(100,100,1000,500)
        h_layout = QHBoxLayout()
        v_layout = QVBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.btnRows)
        h_layout.addWidget(self.btnCols)
        h_layout.addWidget(self.showHidden)
        h_layout.addStretch()
        v_layout.addWidget(self.tableView)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)
    
        self.btnRows.clicked.connect(self.resizeRows)
        self.btnCols.clicked.connect(self.resizeCols)
        self.showHidden.clicked.connect(self.showHiddenColumns)
        self.tableView.doubleClicked.connect(self.on_click)
    # end def


    def openMenu(self, position):
        colIndex = self.tableView.columnAt(position.x())
        menu = QMenu()
        
        hideAct = QAction('Hide', self)
        hideAct.setStatusTip('Hide column')
        hideAct.triggered.connect(lambda: self.hideColumn(colIndex))
        menu.addAction(hideAct)        

        foo = menu.exec_(self.tableView.viewport().mapToGlobal(position))
    # end def


    def hideColumn(self, colIndex):
        self.tableView.hideColumn(colIndex)
    # end def

    def headerClick(self, colIndex):
        print("Column {} header clicked".format(colIndex))
    # end def


    def resizeRows(self):
        self.tableView.resizeRowsToContents()        
    # end def
    
    
    def resizeCols(self):
        self.tableView.resizeColumnsToContents()        
    # end def
    

    def showHiddenColumns(self):
        for i in range(len(self.colHeader)):
            self.tableView.showColumn(i)
    # end def
    
    
    def setTsvFile(self, tsvFile):
        self.tsvFile = tsvFile
        self.setModel()
    # end def
    
    
    def setModel(self):
        self.model = TableModel(filename=self.tsvFile)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        self.show()
    # end def
    
    
    def on_click(self, signal):
        row = signal.row()  # RETRIEVES ROW OF CELL THAT WAS DOUBLE CLICKED
        column = signal.column()  # RETRIEVES COLUMN OF CELL THAT WAS DOUBLE CLICKED
        cell_dict = self.model.itemData(signal)  # RETURNS DICT VALUE OF SIGNAL
        cell_value = cell_dict.get(0)  # RETRIEVE VALUE FROM DICT
 
        index = signal.sibling(row, 0)
        index_dict = self.model.itemData(index)
        index_value = index_dict.get(0)
        print(
            'Row {}, Column {} clicked - value: {}\nColumn 1 contents: {}'.format(row, column, cell_value, index_value))
    # end def
    
# end class


#%%
class TableModel(QAbstractTableModel):
    
    def __init__(self, filename):
        super().__init__()
        self.df = readTsv(filename)
        self.columns = self.df.columns.tolist()
        self.colCount = len(self.columns)
        self.rowCount = len(self.df)
    # end def
    

    def rowCount(self, index):
        return self.rowCount
    # end def
    

    def columnCount(self,index):
        return self.colCount
    # end def
    
    
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            i = index.row()
            j = index.column()
            return '{}'.format(self.df.iloc[i,j])
        else:
            return QVariant()
    # end def


    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.columns[col])
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return QVariant(col+1)
        return QVariant()
    # end def

# end class
    

#%% main
def main():
    global app
    app = QApplication(sys.argv)
    ex = MainWindow()
    app.exec_()
    sys.exit(0)
# end def


#%% Call main()
if __name__ == '__main__':
    main()
