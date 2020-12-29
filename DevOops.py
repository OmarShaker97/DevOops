import json
import os
import time
import psutil
from multiprocessing import Process

# TRUE => Server up and running (Found) & FALSE => Server down (Not Found)

fileOpener = open('config.json')
data = json.load(fileOpener)
fileOpener.close()

# Initializing Trade Aggregator Servers State
currentTradeAggregatorServersState = dict()
previousTradeAggregatorServersState = dict()

# Initializing Trade Aggregator Process State
currentTradeAggregatorProcessState = dict()
previousTradeAggregatorProcessState = dict()

# Initializing Order Proxy Service State
currentOrderProxyServiceState = dict()
previousOrderProxyServiceState = dict()

# Initializing Trade Aggregator Proxy Process State
currentTradeAggregatorProxyProcessState = dict()
previousTradeAggregatorProxyProcessState = dict()

# Initializing Trade Aggregator Proxy State
currentTradeAggregatorProxyPortState = dict()
previousTradeAggregatorProxyPortState = dict()

# Trade Aggregator Servers are initially up and running
for (key, value) in data['trade-aggregator-servers'].items():
    currentTradeAggregatorServersState[key] = True
    previousTradeAggregatorServersState[key] = True

# Trade Aggregator Processes are initially up and running
for (key, value) in data['trade-aggregator-process'].items():
    currentTradeAggregatorProcessState[key] = True
    previousTradeAggregatorProcessState[key] = True

# Order Proxy Services are initially up and running
for (key, value) in data['order-proxy-service'].items():
    currentOrderProxyServiceState[key] = True
    previousOrderProxyServiceState[key] = True

# Trade Aggregator Processes are initially up and running
for (key, value) in data['trade-aggregator-proxy'].items():
    currentTradeAggregatorProxyProcessState[key] = True
    previousTradeAggregatorProxyProcessState[key] = True
    currentTradeAggregatorProxyPortState[key] = True
    previousTradeAggregatorProxyPortState[key] = True


# Monitor Trade Aggregator Servers


def monitorTradeAggregatorServers(mode):
    # Loop Over Servers
    for (key, value) in data['trade-aggregator-servers'].items():
        # Run netstat command
        cmd = 'netstat -an | findstr %s | findstr %s' % (
            value['port'], mode)  # mode = ESTABLISHED

        output = os.popen(cmd).read()
        # Check Trade Aggregator Servers State
        checkIfPortExists(key, value, output, currentTradeAggregatorServersState,
                          previousTradeAggregatorServersState)


# Monitor Trade Aggregator Processes


def monitorTradeAggregatorProcess():
    # Loop Over Processes
    for (key, value) in data['trade-aggregator-process'].items():
        # Check if each process is running
        checkIfProcessRunning(
            key, value['name'], currentTradeAggregatorProcessState, previousTradeAggregatorProcessState)

# Monitor Order Proxy Services


def monitorOrderProxyService():
    # Loop Over Services
    for (key, value) in data['order-proxy-service'].items():
        # Check if each process is running
        checkIfProcessRunning(
            key, value['name'], currentOrderProxyServiceState, previousOrderProxyServiceState)

# Monitor Trade Aggregator Proxy Processes


def monitorTradeAggregatorProxy(mode):
    # Loop Over Services
    for (key, value) in data['trade-aggregator-proxy'].items():
        # Check if each process is running
        checkIfProcessRunning(
            key, value['name'], currentTradeAggregatorProxyProcessState, previousTradeAggregatorProxyProcessState)

        # Run netstat command
        cmd = 'netstat -an | findstr %s | findstr %s' % (
            value['port'], mode)  # mode = LISTENING

        output = os.popen(cmd).read()
        # Check Trade Aggregator Servers State
        checkIfPortExists(key, value, output, currentTradeAggregatorProxyPortState,
                          previousTradeAggregatorProxyPortState)


def checkIfPortExists(key, value, output, currentState, previousState):
    # Attempts initially is set to zero
    attempts = 0
    # Checks that the server is down a couple of times before sending an email
    while(attempts < data['retryAttempts']):
        # Sleep for a given time before retrying
        time.sleep(data['waitTime'])
        # If the IP Address is found in the output of the command, then server is running
        if(value['ip-address'] in output):
            currentState[key] = True
            print('IP Address: %s was found!' % value['ip-address'])
            break
        # Otherwise, the server is not running, thus its current state is set to False
        else:
            currentState[key] = False
            print('IP Address: %s was not found!' % value['ip-address'])
            attempts += 1
    checkAndUpdateState(attempts, key, previousState, currentState)


def checkIfProcessRunning(key, processName, currentState, previousState):
    # Attempts initially is set to zero
    attempts = 0
    # Sleep for a given time before retrying
    while(attempts < data['retryAttempts']):
        time.sleep(data['waitTime'])
        # Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if processName.lower() in proc.name().lower():
                    print('Process %s was found!' % processName)
                    currentState[key] = True
                    checkAndUpdateState(
                        attempts, key, previousState, currentState)
                    return
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                print('Process %s was not found!' % processName)
                currentState[key] = False
                attempts += 1
                break
        print('Process %s was not found!' % processName)
        currentState[key] = False
        attempts += 1
    checkAndUpdateState(attempts, key, previousState, currentState)


def checkAndUpdateState(attempts, key, previousState, currentState):
    # If the number of attempts to ping the server surpasses retryAttempts from config file and the server was previously
    # running then change previous state of the server from True to False and sent email to DevOps team to notify them
    if(attempts >= data['retryAttempts'] and previousState[key]
       and not currentState[key]):
        previousState[key] = False
        print('Sending Email (Went from up to down)')
    # If the server is currently running and it was not running previously then chnage previous state to running, and
    # send email to DevOps team to notify them that server is now back and running
    elif(currentState[key] and not previousState[key]):
        previousState[key] = True
        print('Sending Email (Went from down to up)')


def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


if __name__ == '__main__':
    while(True):
        monitorTradeAggregatorServers("ESTABLISHED")
        monitorTradeAggregatorProcess()
        monitorOrderProxyService()
        monitorTradeAggregatorProxy("LISTENING")
