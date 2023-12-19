from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Numeric, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import func
from module.createTable import Timepoint
from module.parser import dobParser, dobConverter
from dateutil.parser import parse
import pandas as pd
from itertools import chain
import numpy as np
import re

class resultRecord(object):
    def __init__(self, result, subject, timepoint, status, test, range, snapshot, comment):
        self.result = result
        self.subject = subject
        self.timepoint = timepoint
        self.status = status
        self.test = test
        self.range = range
        self.snapshot = snapshot
        self.comment = comment

def createResult(record_row, timepoints, status, snapshot):
    out = []
    for t in timepoints:
        if record_row[t] == None:
            temp_status = "missing"
        else:
            temp_status = status
        val_com = diseaseParser(record_row[t])
        rec = resultRecord(
            # result = record_row[t], 
            result = val_com[0],
            comment = val_com[1],
            timepoint = t,
            subject = record_row['Subject ID'],
            status = temp_status,
            test = record_row['Test'],
            range = record_row['Reference Range'],
            snapshot = snapshot)
        out.append(rec)
    return(out)

def diseaseParser(string):
    value = np.nan
    comment = np.nan
    if pd.isnull(string):    
        return((value, comment))
    s = string.split("/")
    if len(s) == 1:
        if re.search(r'(\d+)(\.)?(\d+)?', s[0]):
            value = s[0].strip()
        else:
            comment = s[0].strip()
    elif len(s) > 1:
        value = s[0].strip(); comment = s[1].strip()
    return((value, comment))

def table2result(data, timepoint_list, status, snapshot):
    """function to convert pandas DataFrame of disease result into a list of list of resultRecord objects.
    
    Arguments:
        data {[pd.DataFrame]} -- [pandas DataFrame read from csv, !!WIDE FORMAT!!]
        timepoint_list {[list]} -- [List of timepoint names either from database or entered manually]
        status {[string]} -- [status type of the current pandas DataFrame, either missing, missing, commented]
    """
    out = []
    for i,r in data.iterrows():
        res = createResult(r, timepoints = timepoint_list, status = status, snapshot = snapshot)
        out.append(res)
    return(out)

def singlecreator(result, subject, timepoint, status, test, rang, snapshot):
    if result == None:
        status = "missing"
    rec = resultRecord(result = result, 
                       subject = subject, 
                       timepoint = timepoint, 
                       status = status, 
                       test = test, 
                       range = rang,
                       snapshot = snapshot)
    return(rec)

def deduper(resultsList, status, snapshot):
    res_flat = list(chain.from_iterable(resultsList))
    tuplelist = [{(r.subject, r.test, r.timepoint, r.range): r.result} for r in res_flat]
    newdict = {}
    nochangedict = {}
    changedict ={}
    olddict = {}
    for d in tuplelist:
        for k in d:
            if k not in newdict:
                newdict[k] = d[k]
            elif k in newdict:
                if newdict[k] == None:
                    olddict[k] = newdict[k]
                    newdict[k] = d[k]
                    changedict[k] = d[k]
                elif newdict[k] != None:
                    nochangedict[k] = d[k]
    newlist = []
    for k in newdict:
        sub = k[0]
        test = k[1]
        timepoint = k[2]
        rang = k[3]
        result = newdict[k]
        resultobj = singlecreator(result = result, subject = sub, timepoint = timepoint, status = status, test = test, rang = rang, snapshot = snapshot)
        newlist.append(resultobj)
    out = [newlist, nochangedict, changedict, olddict]
    return(out)

def table2result2(data, timepoint_list, status, snapshot):
    """function to convert pandas DataFrame of disease result into a list of list of resultRecord objects.
    
    Arguments:
        data {[pd.DataFrame]} -- [pandas DataFrame read from csv, !!WIDE FORMAT!!]
        timepoint_list {[list]} -- [List of timepoint names either from database or entered manually]
        status {[string]} -- [status type of the current pandas DataFrame, either missing, missing, commented]
    """
    out = []
    for i,r in data.iterrows():
        res = createResult(r, timepoints = timepoint_list, status = status, snapshot = snapshot)
        out.append(res)
    newout = deduper(out, status, snapshot)
    return(newout[0])

def results2table(list):
    """Function to convert list of resultRecord objects into a pd.DataFrame
    
    Arguments:
        list {[type]} -- [description]

    Returns:
        df {DataFrame} -- pd.DataFrame with the columns: result, subject, timepoint, status, test, range
    """
    temp = [vars(x) for x in list]
    df = pd.DataFrame(temp)
    return(df)

def timeGen(session):
    """function to generate a list of timepoints within disease db
    
    Arguments:
        session {[sqlalchem.Session]} -- [sqlalchemy session with disease db]
    """
    q = session.query(Timepoint.id, Timepoint.name).all()
    return([x[1] for x in q])

def subGen(data):
    sub = data[['Subject ID', 'Inv. Number', 'Sex', 'Birthdate']]
    sub = sub.drop_duplicates()
    sub['Birthdate'] = dobConverter(sub['Birthdate'])
    subDict = sub.set_index('Subject ID').to_dict('index')
    for x in subDict:
        subDict[x]['Birthdate'] = parse(subDict[x]['Birthdate'])
    return(subDict)

    # for r in record_row[1:]:
    #     timepoint = record_row.index[r]

    #     timepoint_id = timepoint_dict[timepoint]
    #     subject_id = subject_dict[subject_id]
        
        