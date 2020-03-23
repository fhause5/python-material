from pythonping import ping
import asyncio
import time


async def google():
    print('ping google')
    #yield  from asyncio.sleep(1)
    ping('8.8.8.8', verbose=True)
    task = asyncio.create_task(google())

async def local():
    print("ping local")
    ping('localhost', verbose=True)
    task = asyncio.create_task(local())

# событийный цикл
event = asyncio.get_event_loop()
tasks = [event.create_task(google()), event.create_task(local())]
event.run_until_complete(asyncio.wait(tasks))
event.close

if __name__ == '__main__':
    main()