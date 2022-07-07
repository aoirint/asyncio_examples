import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

async def main():
  def func():
    time.sleep(3)
    print('func exited') # 3

  loop = asyncio.get_event_loop()
  executor = ThreadPoolExecutor()
  loop.run_in_executor(executor, func)

  await asyncio.sleep(1)
  print('main exited') # 1

asyncio.run(main())

print('exited') # 2
