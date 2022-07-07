import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading
import time

def main():
  async def func():
    await asyncio.sleep(3)
    print('func exited') # 3

  thread = threading.Thread(target=lambda: asyncio.run(func()))
  thread.start()

  time.sleep(1)
  print('main exited') # 1

main()

print('exited') # 2
