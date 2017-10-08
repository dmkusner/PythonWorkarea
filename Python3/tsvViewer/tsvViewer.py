#!/bin/env python3

"""
"""

#%% Imports
import os
import pandas as pd
import re
import sys

from csv import QUOTE_NONE
from functools import partial
from PyQt5.QtWidgets import QWidget, QPushButton, QDialog, QMainWindow, QCheckBox, QAction, qApp, QApplication, QFileDialog, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, QAbstractScrollArea


#%%
readTsv = partial(pd.read_csv, sep='\t', dtype=object, encoding='utf-8', quoting=QUOTE_NONE)


#%%
class TablePlus(QWidget):
    
    def __init__(self, r, c, tsvFile):
        super().__init__()
        
        self.btnRows = QPushButton('Resize Rows to Contents')
        self.btnCols = QPushButton('Resize Columns to Contents')
        self.btnHideShow = QPushButton('Show/Hide Columns')
        self.table = TableWidget(r, c, tsvFile)
        self.initUI()
        
        
    def initUI(self):
        self.setGeometry(100,100,1000,500)
        h_layout = QHBoxLayout()
        v_layout = QVBoxLayout()
        
        h_layout.addStretch()
        h_layout.addWidget(self.btnRows)
        h_layout.addWidget(self.btnCols)
        h_layout.addWidget(self.btnHideShow)
        h_layout.addStretch()
        
        v_layout.addWidget(self.table)
        v_layout.addLayout(h_layout)
        
        self.btnRows.clicked.connect(self.resizeRows)
        self.btnCols.clicked.connect(self.resizeCols)
        self.btnHideShow.clicked.connect(self.table.selectDisplayCols)
        
        self.setLayout(v_layout)
        self.show()
    # end def


    def resizeRows(self):
        self.table.resizeRowsToContents()        
    # end def
    
    
    def resizeCols(self):
        self.table.resizeColumnsToContents()        
    # end def
    
# end class
        
    

#%% Table Widget
class TableWidget(QTableWidget):

    def __init__(self,r,c,tsvFile):
        super().__init__(r,c)

        self.initUI()
        
        self.df = readTsv(tsvFile)
        self.displayDataFrame()        
    # end def


    def initUI(self):
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)  
        self.cellDoubleClicked.connect(self.cellDblClk)
        self.show()
    # end def


    def cellDblClk(self, a,b):
        print(a,b)
    # end def


    def setDataFrame(self,df):
        self.df = df
    # end def
        
    
    def displayDataFrame(self):
        self.clear()
        self.setColumnCount(len(self.df.columns))
        self.setHorizontalHeaderLabels(self.df.columns)
        self.setRowCount(len(self.df))
        for i,row in enumerate(self.df.itertuples(index=False)):
            for j,item in enumerate(row):
                self.setItem(i,j,QTableWidgetItem(item))
        self.setColumnHidden(2,True)
        self.setColumnHidden(2,False)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
    # end def


    def selectDisplayCols(self):
        d = QDialog()
        d.setWindowTitle("Select Display Columns")
        d.setGeometry(100,100,200,200)
        d.setModal(True)
    
        v_layout = QVBoxLayout()
        
        boxes = []
        for i,colName in enumerate(self.df.columns.tolist()):
            box = QCheckBox(colName)
            boxes.append(box)
            v_layout.addWidget(box)
        
        d.setLayout(v_layout)
            
        d.exec_()
    # end def
    
# end class


#%% main
def main():
    app = QApplication(sys.argv)
    ex = TablePlus(0,0,'data.tsv')
    sys.exit(app.exec_())
# end def


#%% Call main()
if __name__ == '__main__':
    main()
