# import libs

import pandas as pd
import re
from sqlalchemy import and_, or_, not_
from module.createTable import *
from module.insertData import *
from module.parser import *
from module.createResult import *

# Connect to db
db = 'disease'
host = 'generic.pharma.com'
uname = 'user'
pword = 'test'
server = [uname, pword, host, db]
engine = createEngine(*server)
Base.metadata.create_all(engine)
session = createSession(engine)

# Read data, dedulicate
data = pd.read_csv('data_wide.txt', sep = '\t')
data = data.where((pd.notnull(data)), None)
tests = data['Test'].unique()

# Insert lab tests
insertTests(tests, session)

# Create & insert investigators
doctors_list = data[['Inv. Number', 'Investigator Name']].drop_duplicates().set_index('Investigator Name').to_dict('index')
insertInvestigators(doctors_list, session)

# Create & insert subjects
subDict = subGen(data)
insertSubjects(subDict, session)

# Create and insert status for timepoint testing status
status = ['tested', 'missing', 'commented']
timepoints = [x for x in data.columns[9:]]
insertStatus(status, session)
insertTimepoint(timepoints, session)

#Generate dictionary of available timepoints
timelist = timeGen(session)

# Convert results to pandas df
resultsObj = table2result(data, timelist, "tested")

# Set overwrite to TRUE, insert actual data
ow = True
res_not_ins = []
for res in resultsObj:
    temp = insertResult(res, session, ow)
    res_not_ins.append(temp)