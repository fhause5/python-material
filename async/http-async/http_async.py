import requests, json, asyncio

async def listRepositories1(githubAccount):
    try:
        url = 'https://api.github.com/users/' + githubAccount + '/repos'
        login = requests.get(url)
        answer = login.json()
        for i in answer:
            print(i['name'])
    except Exception:
        print("[ERROR] during connect to guthub, wait for 10 minutes")
        print("[WARNING] please check username")

async def listRepositories2(githubAccount):
    try:
        url = 'https://api.github.com/users/' + githubAccount + '/repos'
        login = requests.get(url)
        answer = login.json()
        for i in answer:
            print(i['name'])
    except Exception:
        print("[ERROR] during connect to guthub, wait for 10 minutes")
        print("[WARNING] please check username")

def main(args1, args2):
    ioloop = asyncio.get_event_loop()
    tasks = [
        ioloop.create_task(listRepositories1(args1)),
        ioloop.create_task(listRepositories2(args2))
    ]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()

if __name__ == '__main__':
    main("fhause5","snap032")