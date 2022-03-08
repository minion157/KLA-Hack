import yaml
import datetime as dt
import time
import threading
import logging
from yaml.loader import SafeLoader

filename = 'Milestone1B.txt'
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


def timeFunction(inputs):
    val = inputs['ExecutionTime']
    time.sleep(int(val))


def executeTask(function,inputs,taskName):
    if function == 'TimeFunction':
        logging.info(taskName+" Entry")
        logging.info(taskName+" Executing "+function+" ("+str(inputs['FunctionInput'])+', '+str(inputs['ExecutionTime'])+")")
        timeFunction(inputs)
        logging.info(taskName+" Exit")

def runTasks(dictionary,activityName):
    if dictionary['Type'] == 'Task':
        executeTask(dictionary['Function'],dictionary['Inputs'],activityName)
    elif dictionary['Type'] == 'Flow':
        if dictionary['Execution'] == 'Sequential':
            logging.info(activityName+" "+"Entry")
            for key in dictionary['Activities'].keys():
                runTasks(dictionary['Activities'][key],activityName+"."+str(key))
            logging.info(activityName+" "+"Exit")
        else:
            logging.info(activityName+" "+"Entry")
            keys = dictionary['Activities'].keys()
            proc = []
            for i in keys:
                t = threading.Thread(target=runTasks,args=(dictionary['Activities'][i],activityName+"."+str(i)))
                proc.append(t)
                t.start()
            for j in proc:
                j.join()
            logging.info(activityName+" "+"Exit")
        

data = getYaml('Milestone1\Milestone1B.yaml')
activityName = str(list(data.keys())[0])
runTasks(data[activityName],activityName)

