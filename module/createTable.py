import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Numeric, String, Text, DateTime, Date, Boolean, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import DatabaseError

# from sqlalchemy import create_engine
# from sqlalchemy import Table, Column, Integer, Numeric, String, Text, DateTime, Boolean, ForeignKey, Float
# from sqlalchemy.orm import sessionmaker, relationship, backref
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.exc import DatabaseError

# Return an engine 
def createEngine(user, password, ip, database):
    """Function to return engine instance to interact with database.
    
    Arguments:
        user {string} -- database credentials
        password {string} -- database credentials
        ip {string} -- database credentials
        database {string} -- database credentials
    
    Returns:
        sqlalchemy engine -- engine instance 
    """

    query = 'mysql+pymysql://' + user + ':' + str(password) + '@' + str(ip) + '/' + database
    try:
        engine = create_engine(query)
    except DatabaseError:
        print("DB Error, can't connect to database")
    return engine

Base = declarative_base()

# Tables classes

class Result(Base):
    """class to create disease results table
    
    Arguments:
        Base {declarative_base} -- Inherits declarative base from sqlalchemy lib
    """

    __tablename__ = 'result'
    id = Column(Integer, primary_key=True)
    results = Column(String(500), nullable = True)
    timepoint_id = Column(Integer, ForeignKey('timepoint.id'), nullable = False)
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable = False)
    status_id = Column(Integer, ForeignKey('status.id'), nullable = False)
    test_id = Column(Integer, ForeignKey('test.id'), nullable = False)
    range = Column(String(500), nullable = True)
    snapshot_id = Column(Integer, ForeignKey('snapshot.id'), nullable = False)
    # reference_id = Column(Integer, ForeignKey('reference.id'), nullable = False)
    # old_p = Column(Float, nullable = False)
    # old_p_adj = Column(Float, nullable = False)
    # z_score = Column(Float, nullable = False)
    # combined = Column(Float, nullable = False)
    # genes = Column(Text, nullable = False)
    # experiment_id = Column(Integer, ForeignKey('experiment.id'), nullable = False)
    # condition1_id = Column(Integer, ForeignKey('condition.id'), nullable = False)
    # condition2_id = Column(Integer, ForeignKey('condition.id'), nullable = False)
    # # comp = Column(Integer, ForeignKey('enrichr_table'), nullable = False)
    # db_id = Column(Integer, ForeignKey('enrichr_database.id'), nullable = False)
    mysql_engine = "InnoDB"

class Subject(Base):
    """class to create disease subject table 
    
    Arguments:
        Base {declarative_base} -- Inherits declarative base from sqlalchemy lib
    """

    __tablename__='subject'
    id = Column(Integer, primary_key = True)
    study_id = Column(String(500), nullable = False)
    # investigator_id = Column(String(100), nullable = False)
    investigator_id = Column(Integer, ForeignKey('investigator.id'), nullable = False)
    sex = Column(String(50), nullable = False)
    dob = Column(Date(), nullable = False)
    # geneCoverage = Column(Integer, nullable = False)
    # genesPerTerm = Column(Integer, nullable = False)
    # link = Column(String(500), nullable = False)
    mysql_engine = "InnoDB"
# class EnrichrTable:
#     __tablename__ = 'enrichr_table'
#     id = Column(Integer, primary_key=True)
#     experiment_id = Column(Integer, ForeignKey('experiment.id'), nullable = False)
#     condition_pair = Column(String(50), nullable = False)
#     condition_pair_num = Column(String(50), nullable = False)
#     condition1_id = Column(Integer, ForeignKey('condition.id'), nullable = False)
#     condition2_id = Column(Integer, ForeignKey('condition.id'), nullable = False)

class Timepoint(Base):
    """class to create disease timepoint table
    
    Arguments:
        Base {declarative_base} -- Inherits declarative base from sqlalchemy lib
    """

    __tablename__ = 'timepoint'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    # experiment_id = Column(Integer, ForeignKey('experiment.id'), nullable=False)
    mysql_engine = "InnoDB"

class Status(Base):
    """class to create disease status table
    
    Arguments:
        Base {declarative_base} -- Inherits declarative base from sqlalchemy lib
    """
    __tablename__ = 'status'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    # date = Column(DateTime(), nullable=False)
    # tech = Column(String(100), nullable=False)
    # mim_read_length = Column(Integer, nullable= False)
    # species_id = Column(Integer, ForeignKey('species.id'))
    # comments = Column(Text)
    # scientist_id = Column(Integer, ForeignKey('scientist.id'))
    mysql_engine = "InnoDB"

class Investigator(Base):
    """class to create disease investigator table
    
    Arguments:
        Base {declarative_base} -- Inherits declarative base from sqlalchemy lib
    """
    __tablename__ = 'investigator'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    number = Column(String(50), nullable = False)
    mysql_engine = "InnoDB"

class Test(Base):
    """class to create disease test table
    
    Arguments:
        Base {declarative_base} -- Inherits declarative base from sqlalchemy lib
    """
    __tablename__ = 'test'
  
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
#     ref_range = Column(String(50), nullable=False)
    # scientist_type_id = Column(Integer, ForeignKey('scientist_type.id'))
    mysql_engine = "InnoDB"

class Snapshot(Base):
    """class to create disease snapshot table
    
    Arguments:
        Base {declarative_base} -- Inherits declarative base from sqlalchemy lib
    """
    __tablename__ = 'snapshot'
  
    id = Column(Integer, primary_key=True)
    description = Column(String(100), nullable=False)
    date_created = Column(DateTime(), nullable = False)
    mysql_engine = "InnoDB"

# Don't insert references separate, insert as it in the results table.
# class Reference(Base):
#     __tablename__ = 'reference'
    
#     id = Column(Integer, primary_key = True)
#     test_id = Column(Integer, ForeignKey('test.id'), nullable = False)
#     range = Column(String(100), nullable = False)
#     mysql_engine = "InnoDB"

# class ScientistType(Base):
#     __tablename__ = 'scientist_type'
  
#     id = Column(Integer, primary_key=True)
#     type = Column(String(50), nullable=False)