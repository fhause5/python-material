import asyncio
import time


async def MR1(REPO1):
    print("REPO1 repo: " + REPO1)
    await asyncio.sleep(3)
    print("Merge repo DONE" + REPO1)


async def MR2(REPO2):
    print("REPO2 repo: " + REPO2)
    await asyncio.sleep(3)
    print("Merge repo DONE" + REPO2)


async def main():
    repo1 = "single-Tenant"
    repo2 = "multi-Tenant"
    tasks = [
        MR1(repo1),
        MR2(repo2)
    ]
    await asyncio.gather(*tasks)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_time = time.time()
    #main()
    asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
