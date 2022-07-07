import asyncio
import time

async def main():
  def func():
    time.sleep(3)
    print('func exited') # 1

  func()

  await asyncio.sleep(1)
  print('main exited') # 2

asyncio.run(main())

print('exited') # 3
