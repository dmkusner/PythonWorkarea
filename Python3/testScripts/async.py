import asyncio
from random import randint


async def task(name, work_queue):
    while not work_queue.empty():
        delay = randint(1,10)
        data = await work_queue.get()
        print("Task {} item {} sleeping for {} secs".format(name, data, delay))
        await asyncio.sleep(delay)


async def main():
    """
    This is the main entry point for the program
    """

    # Create the queue of work
    work_queue = asyncio.Queue()

    # Put some work in the queue
    for work in range(50):
        await work_queue.put(work)

    # Run the tasks
    await asyncio.gather(
        asyncio.create_task(task("1", work_queue)),
        asyncio.create_task(task("2", work_queue)),
        asyncio.create_task(task("3", work_queue)),
        asyncio.create_task(task("4", work_queue)),
        asyncio.create_task(task("5", work_queue)),
    )


if __name__ == "__main__":
    asyncio.run(main())
