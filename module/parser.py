import re
import pandas as pd
from dateutil.parser import parse

def parsedict(data):
    outdict = {}
    for x in data.itertuples():
        record = x.condition_pair_num.strip()
        com_searchObj = re.search(r'condition_(\d+)_vs_(\d+)', record)
        num1 = com_searchObj.group(1)
        num2 = com_searchObj.group(2)
        if num1 not in outdict:
            outdict[num1] = x.condition1.strip()
        if num2 not in outdict:
            outdict[num2] = x.condition2.strip()
    return(outdict)

def tableparse(file, exp):
    largeData = pd.read_csv(file, sep = '\t')
    data = largeData.loc[largeData['experiment']==exp, ['condition_pair_num', 'condition1', 'condition2']]
    odict = parsedict(data)
    return(odict)

def dobParser(date):
    match = re.search(r'(01\-Jan\-)(\d+)', date)
    if len(match.groups()[1])==2:
        if int(match.groups()[1])>19:
            return(match.groups()[0]+'19'+match.groups()[1])
        elif int(match.groups()[1])<19:
            return(match.groups()[0]+'20'+match.groups()[1])
    else:
        return(date)
    
def dobConverter(dobs):
    dobs = [dobParser(date) for date in dobs]
    dobs = [re.sub(r'\-Jan\-', '-01-', x) for x in dobs]
    dobs = [re.sub(r'\*','',x) for x in dobs]
    dob_correct = pd.to_datetime(dobs).astype(str)
    # dob_correct = [parse(x) for x in dob_correct]
    return(dob_correct)
