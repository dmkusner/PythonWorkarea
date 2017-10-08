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
from PyQt5.QtWidgets import QApplication, QWidget, QTableView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem


#%%
readTsv = partial(pd.read_csv, sep='\t', dtype=object, encoding='utf-8', quoting=QUOTE_NONE)


#%%
class Table(QWidget):
    def __init__(self):
        super().__init__()
 
        self.tsvFile = 'data.tsv'
    
        # CREATE THE TABLE
        self.table = QTableView(self)  # SELECTING THE VIEW
        self.table.setGeometry(0, 0, 575, 575)
        self.model = QStandardItemModel(self)  # SELECTING THE MODEL - FRAMEWORK THAT HANDLES QUERIES AND EDITS
        self.table.setModel(self.model)  # SETTING THE MODEL
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.populate()
        self.show()
    
        self.table.doubleClicked.connect(self.on_click)
 
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
    
    
    def populate(self):
        df = readTsv(self.tsvFile)
        self.model.setColumnCount(len(df.columns))
        for tsvRow in df.itertuples(index=False):
            tableRow = [QStandardItem(x) for x in tsvRow]
            self.model.appendRow(tableRow)
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
