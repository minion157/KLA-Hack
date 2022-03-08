from ast import Global
import operator
import yaml
import datetime
import time
import threading
import logging
from yaml.loader import SafeLoader
import pandas as pd
import re
filename = 'Milestone2A.txt'
Format = "%(asctime)s.%(msecs)06d;%(message)s"
logging.basicConfig(
    format=Format,
    filename=filename,
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

def getYaml(path):
    with open(path) as stream:
        data = yaml.safe_load(stream)
    return data

def parse_csv(file_name):
    df = pd.read_csv(file_name)
    return df


def DataLoad(filename):
    df = pd.read_csv(filename)
    defects = len(df.index)
    return defects
    return {'DataTable' : df,'NoOfDefects': defects}

def timeFunction(inputs):
    val = inputs['ExecutionTime']
    time.sleep(int(val))

gdefects = 0


def executeTask(function,inputs,taskName):
    global gdefects
    if function == 'TimeFunction':
        logging.info(taskName+" Entry")
        logging.info(taskName+" Executing "+function+" ("+str(inputs['FunctionInput'])+', '+str(inputs['ExecutionTime'])+")")
        timeFunction(inputs)
        logging.info(taskName+" Exit")
    elif function == 'DataLoad':
        logging.info(taskName+" Entry")
        logging.info(taskName+" Executing "+function+" ("+str(inputs['Filename'])+")")
        gdefects = DataLoad(inputs["Filename"])
        logging.info(taskName+" Exit")

def runTasks(dictionary,activityName):
    global gdefects
    if dictionary['Type'] == 'Flow':
        if dictionary['Execution'] == 'Sequential':
            logging.info(activityName+" "+"Entry")
            for key in dictionary['Activities'].keys():
                runTasks(dictionary['Activities'][key],activityName+"."+str(key))
            logging.info(activityName+" "+"Exit")
        else:
            logging.info(activityName+" "+"Entry")
            L = dictionary['Activities'].keys()
            res = []
            for i in L:
                pr = threading.Thread(target=runTasks,args=(dictionary['Activities'][i],activityName+"."+str(i)))
                res.append(pr)
                pr.start()
            for r in res:
                r.join()
            logging.info(activityName+" "+"Exit")
    elif dictionary['Type'] == 'Task':
        if 'Condition' not in dictionary.keys():
            executeTask(dictionary['Function'],dictionary['Inputs'],activityName)
        else:
            var = re.findall(r'\(.*?\)', dictionary['Condition'])[0][1:-1]
            sym = dictionary['Condition'].split(var)[1].split(' ')[1]
            val = int(dictionary['Condition'].split(var)[1].split(' ')[2])
            # print(sym,val)
            if sym == '>':
                if gdefects > int(val):
                    executeTask(dictionary['Function'],dictionary['Inputs'],activityName)
                else:
                    logging.info(activityName+" Skipped")
            elif sym == '<':
                if gdefects < int(val):
                    executeTask(dictionary['Function'],dictionary['Inputs'],activityName)
                else:
                    logging.info(activityName+" "+"Entry")
                    logging.info(activityName+" Skipped")
                    logging.info(activityName+" "+"Exit")
        

data = getYaml('Milestone2\Milestone2A.yaml')
activityName = str(list(data.keys())[0])
runTasks(data[activityName],activityName)

