import yaml
import datetime as dt
import time
from yaml.loader import SafeLoader

def timeFunction(t):
    time.sleep(t)

def logFunction(log_str):
    string = str(dt.datetime.now()) + ';'
    for x in range(len(log_str)):
        string += log_str[x]
        if x < (len(log_str) - 1):
            string += '.'
    return string
    
def recursiveActivities(activity, log_str, textStrings):

    list_tasks = list(activity.keys())
    for x in list_tasks:
        task = activity[x]
        log_str.append(x)
        line = logFunction(log_str) + " Entry\n"
        textStrings.append(line)
        task_attr = list(task.keys())
        condition = 1
        if "Execution" in task_attr:
            sub_flow = task['Activities']
            recursiveActivities(sub_flow, log_str, textStrings)
        else:
            if task['Function'] == 'TimeFunction' and condition:
                op_str = logFunction(log_str)
                task_input = task['Inputs']
                exec_time = int(task_input['ExecutionTime'])
                op_str += " Executing TimeFunction("
                op_str += task_input['FunctionInput'] + ","
                op_str += str(exec_time) + ")\n"
                textStrings.append(op_str)
                timeFunction(exec_time)
        line = logFunction(log_str) + " Exit\n"
        textStrings.append(line)
        log_str.pop(-1)


    
stream = open("Milestone1\Milestone1A.yaml", 'r')
dictionary = yaml.load(stream, Loader=SafeLoader)

log_file = open("Milestone1A.txt", "a+")
workflow_keys = list(dictionary.keys())
for key in workflow_keys:
    textStrings = []
    keyName = [key]
    taskName = logFunction(keyName) + " Entry\n"
    textStrings.append(taskName)
    workflow = dictionary['M1A_Workflow']
    activities = workflow['Activities']
    recursiveActivities(activities, keyName, textStrings)
    taskName = logFunction(keyName) + " Exit\n"
    textStrings.append(taskName)
    log_file.writelines(textStrings)
print("End")
log_file.close()

