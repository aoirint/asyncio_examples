import asyncio
import time

def main():
  async def func():
    await asyncio.sleep(3)
    print('func exited') # 1

  asyncio.run(func())

  time.sleep(1)
  print('main exited') # 2

main()

print('exited') # 3
