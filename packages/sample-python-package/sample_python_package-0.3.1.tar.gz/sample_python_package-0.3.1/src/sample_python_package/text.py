import datetime

def hello():
    current = datetime.datetime.now()
    message = 'Hey! It is now ' + str(current)
    print(message)
    return message

