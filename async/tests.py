from select import select

monitor = []
def accept(text):
    print("Except:" + text)

def send(text):
    print("Sending to telegam:" + text)


devops = input("Devops: ")
develop = input("Developer: ")

def event():
    while True:
        ready_to_exept, _, _ = select(monitor, [], [])

if __name__ == '__main__':
    monitor.append(devops)
