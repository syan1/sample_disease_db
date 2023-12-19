# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% [markdown]
# Insert tests from sc_wide.txt table

#%%
import os
import pandas as pd
import re


#%%
data = pd.read_csv('sc_wide.txt', sep = '\t')


#%%
data['Test'].unique()

#%%
import re
from sqlalchemy import and_, or_, not_
from module.createTable import *
from module.insertData import *

#%%
db = 'disease'
host = 'ec2-34-227-100-116.compute-1.amazonaws.com'
uname = 'ironwood'
pword = 'irtest'
server = [uname, pword, host, db]
engine = createEngine(*server)
Base.metadata.create_all(engine)
session = createSession(engine)

#%%
tests = data['Test'].unique()
insertTests(tests, session)


#%%
