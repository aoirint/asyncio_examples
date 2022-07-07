import time
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor
import schedule
from fastapi import FastAPI

app = FastAPI()
schedule_event = threading.Event()

@app.on_event('startup')
async def startup_schedule():
  loop = asyncio.new_event_loop()
  executor = ThreadPoolExecutor()

  def loop_schedule(event):
    while True:
      if event.is_set():
        break
      schedule.run_pending()
      time.sleep(1)

    print('run all existing scheduled jobs')
    schedule.run_all()

    print('exit schedule')

  loop.run_in_executor(executor, loop_schedule, schedule_event)

  schedule.every(1).second.do(lambda: print('tick'))

@app.on_event('shutdown')
async def shutdown_schedule():
  schedule_event.set()
