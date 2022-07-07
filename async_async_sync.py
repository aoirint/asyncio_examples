import asyncio

async def main():
  async def func():
    await asyncio.sleep(3)
    print('func exited') # 1

  await func()

  await asyncio.sleep(1)
  print('main exited') # 2

asyncio.run(main())

print('exited') # 3
