import pymysql
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Numeric, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import func
from sqlalchemy import and_, or_, not_
from datetime import date
import sys
# import os.path
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module.createTable import Test, Investigator, Subject, Timepoint, Status, Result, Snapshot
import pandas as pd
import re
# from collections import defaultdict
# from fileParser.fileParser import *
# from progress.bar import Bar

# from module.getCond2 import getCond2

def createSession(engine):
    conn = engine.connect()
    Session = sessionmaker(bind=conn, autoflush=False)
    session = Session()
    return session

def insertTests(tests, session):
    """insert tests from LIST of tests
    
    Arguments:
        tests {list} -- unique tests from disease data table
        session {sqlalchemy session object} -- disease db session
    """
    for t in tests:
        isExist = session.query(Test.id).filter(Test.name == t).scalar()
        if isExist:
            print("{} test already exists, did not insert".format(t))
        elif not isExist:
            test = Test(name = t)
            session.add(test)
        else:
            continue
    session.commit()

def insertInvestigators(doctors, session):
    """insert doctors from DICTIONARY of doctors with name and id
    
    Arguments:
        doctors {[type]} -- [description]
        session {[type]} -- [description]
    """
    for d in doctors:
        isExist = session.query(Investigator.id).filter(Investigator.name == d).scalar()
        if isExist:
            print("Doctor {} already exists, did not insert".format(d))
        elif not isExist:
            doc = Investigator(name = d, number = doctors[d]['Inv. Number'])
            session.add(doc)
        else:
            continue
    session.commit()

def insertSubjects(subjects, session):
    """insert subjects from DICTIONARY of subjects with id, sex, birthdate 
    
    Arguments:
        subjects {[type]} -- [description]
        session {[type]} -- [description]
    """
    for s in subjects:
        isExist = session.query(Subject.id).filter(Subject.study_id == s).scalar()
        if isExist:
            print("{} already exists, did not insert".format(s))
        elif not isExist:
            investigator_id = session.query(Investigator.id).filter(Investigator.number == subjects[s]['Inv. Number'])
            sub = Subject(study_id = s, investigator_id = investigator_id, sex = subjects[s]['Sex'], dob = subjects[s]['Birthdate'].date())
            session.add(sub)
        else:
            continue
        session.commit()

def insertStatus(status, session):
    """Insert status list into database, should only be performed once
    
    Arguments:
        status {[type]} -- [description]
        session {[type]} -- [description]
    """
    for s in status:
        isExist = session.query(Status.id).filter(Status.name == s).scalar()
        if isExist:
            print("{} already exists, did not insert".format(s))
        elif not isExist:
            stat = Status(name = s)
            session.add(stat)
        else:
            continue
        session.commit()

def insertTimepoint(timepoints, session):
    """Insert timepoints list into database, should only be performed once
    
    Arguments:
        status {[type]} -- [description]
        session {[type]} -- [description]
    """
    for t in timepoints:
        isExist = session.query(Timepoint.id).filter(Timepoint.name == t).scalar()
        if isExist:
            print("{} already exists, did not insert".format(t))
        elif not isExist:
            time = Timepoint(name = t)
            session.add(time)
        else:
            continue
        session.commit()

def insertSnapshot(description, session):
    """Insert snapshot description into database
    
    Arguments:
        description {[type]} -- [description]
        session {[type]} -- [description]
    """
    isExist = session.query.filter(Snapshot.description == description).scalar()
    if isExist:
        print("Snapshot called {} already exists in database, did not insert")
    else:
        snap = Snapshot(description = description, date_created = date.today())
        session.add(snap)
    session.commit

def insertResult(results, overwrite, session):
    # overwrite deleted at first, then use later to flag if function should overwrite
    """Function to insert result objects into disease db.
    
    Arguments:
        results {list} -- list of results object
        session {session object} -- sqlalchemy session object
        overwrite {boolean} -- flag to cause overwrite or not

    Returns:
        non_insert {List} -- list of duplicated records that were not inserted.
    """
    non_insert = []
    for r in results:
        timepoint_id = session.query(Timepoint.id).filter(Timepoint.name == r.timepoint).scalar()
        subject_id = session.query(Subject.id).filter(Subject.study_id == r.subject).scalar()
        status_id = session.query(Status.id).filter(Status.name == r.status).scalar()
        test_id = session.query(Test.id).filter(Test.name == r.test).scalar()
        isExist = session.query(Result.id).filter(and_(Result.timepoint_id == timepoint_id, 
                                                        Result.subject_id == subject_id, 
                                                        Result.status_id == status_id,
                                                        Result.test_id == test_id,
                                                        Result.range == r.range)).scalar()
        if isExist and overwrite == False:
            print("Result for {} at {} for test type: {} already exists, did not insert".format(r.subject, r.timepoint, r.test))
            non_insert.append(r)
        elif (overwrite == True and isExist) or (not isExist):
            res = Result(results = r.result,
                        timepoint_id = timepoint_id,
                        subject_id = subject_id,
                        status_id  = status_id,
                        test_id = test_id,
                        range = r.range)
            session.add(res)
        else:
            non_insert.append(r)
        session.commit()
        return(non_insert)
