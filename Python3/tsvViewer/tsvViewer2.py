#!/bin/env python3

"""
"""

#%% Imports
import os
import pandas as pd
import re
import sys
import random

from csv import QUOTE_NONE
from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget, QTableView, QAbstractItemView, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem


#%%
readTsv = partial(pd.read_csv, sep='\t', dtype=object, encoding='utf-8', quoting=QUOTE_NONE)


#%%
class Table(QWidget):
    def __init__(self):
        super().__init__()
 
        self.tsvFile = 'data.tsv'
    
        # CREATE THE TABLE
        self.table = QTableView(self)
        self.btnRows = QPushButton('Resize Rows to Contents')
        self.btnCols = QPushButton('Resize Columns to Contents')
        
        self.setGeometry(100,100,1000,500)
        h_layout = QHBoxLayout()
        v_layout = QVBoxLayout()
        
        h_layout.addStretch()
        h_layout.addWidget(self.btnRows)
        h_layout.addWidget(self.btnCols)
        h_layout.addStretch()
        
        v_layout.addWidget(self.table)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)
        
        self.model = TableModel(filename=self.tsvFile)  # SELECTING THE MODEL - FRAMEWORK THAT HANDLES QUERIES AND EDITS
        self.table.setModel(self.model)  # SETTING THE MODEL
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.show()
    
        self.btnRows.clicked.connect(self.resizeRows)
        self.btnCols.clicked.connect(self.resizeCols)
        self.table.doubleClicked.connect(self.on_click)
    # end def


    def resizeRows(self):
        self.table.resizeRowsToContents()        
    # end def
    
    
    def resizeCols(self):
        self.table.resizeColumnsToContents()        
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
    app = QApplication(sys.argv)
    ex = Table()
    sys.exit(app.exec_())
# end def


#%% Call main()
if __name__ == '__main__':
    main()
