import datetime

def hello():
    current = datetime.datetime.now()
    return print('Hey. It is now ' + str(current))