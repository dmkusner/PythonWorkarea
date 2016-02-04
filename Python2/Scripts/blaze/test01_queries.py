#!/usr/bin/env python2.7

import blaze as bz
import odo

db = bz.Data("sqlite:///test01.db::data")

# active users
au = bz.by(db.date,active_users=db.name.count())
odo.odo(au,"test01.active_users.csv")

# new users
r1 = bz.by(db.name,date=db.date.min())
nu = bz.by(r1.date,new_users=r1.name.count())
odo.odo(nu,"test01.new_users.csv")
