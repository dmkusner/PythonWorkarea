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
from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, qApp, QApplication, QFileDialog, QHBoxLayout, QListWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QAbstractScrollArea


#%%
readTsv = partial(pd.read_csv, sep='\t', dtype=object, encoding='utf-8', quoting=QUOTE_NONE)


#%% Table Widget
class TableWidget(QTableWidget):

    def __init__(self,r,c,tsvFile):
        super().__init__(r,c)

        self.initUI()
        
        self.df = readTsv(tsvFile)
        self.displayDataFrame()        
    # end def


    def initUI(self):
        self.setGeometry(300, 300, 1000, 400)
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
        self.resizeRowsToContents()
    # end def

# end class

#%% main
def main():
    app = QApplication(sys.argv)
    ex = TableWidget(0,0,'data.tsv')
    sys.exit(app.exec_())
# end def


#%% Call main()
if __name__ == '__main__':
    main()
