import asyncio
import threading

async def main():
  async def func():
    await asyncio.sleep(3)
    print('func exited') # 3

  thread = threading.Thread(target=lambda: asyncio.run(func()))
  thread.start()

  await asyncio.sleep(1)
  print('main exited') # 1

asyncio.run(main())

print('exited') # 2
