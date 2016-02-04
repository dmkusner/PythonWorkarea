#!/usr/bin/env python2.7

import odo
import datashape

# make date a string, by default it becomes a 
# datetime and this causes problems currently
# since odo doesn't know how to parse it
ds = datashape.dshape("var * {date: ?string, name: ?string}")

data = odo.CSV("test01_data.csv",has_header=True)
odo.odo(data,"sqlite:///test01.db::data",dshape=ds)

