from asyncio import create_subprocess_exec
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import time

async def main(
  input_video_path: Path,
  output_video_path: Path,
):
  output_video_path.parent.mkdir(exist_ok=True, parents=True)

  vcodec: str = 'libx264'
  acodec: str = 'aac'

  report_tempfile = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8')
  report_loglevel = 32 # 32: info, 48: debug
  report = f'file={report_tempfile.name}:level={report_loglevel}'

  command = [
    'ffmpeg',
    '-nostdin',
    '-i',
    str(input_video_path),
    '-vcodec',
    vcodec,
    '-acodec',
    acodec,
    '-map',
    '0',
    '-report',
    str(output_video_path),
  ]

  proc = await create_subprocess_exec(
    command[0],
    *command[1:],
    env={
      'FFREPORT': report,
    },
  )

  loop = asyncio.new_event_loop()
  executor = ThreadPoolExecutor()

  report_lines = []
  def read_report(report_file):
    report_file.seek(0)
    while True:
        line = report_file.readline()
        if len(line) == 0: # EOF
          if proc.returncode is not None: # process closed and EOF
            break
          time.sleep(0.1)
          continue # for next line written
        if line.endswith('\n'):
          line = line[:-1] # strip linebreak
        report_lines.append(line)
        print(f'REPORT: {line}', flush=True)
    print('report closed') # closed when process exited

  loop.run_in_executor(executor, read_report, report_tempfile)

  returncode = await proc.wait()
  # stdout, stderr may be not closed
  print(f'exited {returncode}')

  # here, report_lines: ffmpeg log

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('input', type=str)
  parser.add_argument('output', type=str)
  args = parser.parse_args()

  input_video_path = Path(args.input)
  output_video_path = Path(args.output)

  asyncio.run(main(
    input_video_path=input_video_path,
    output_video_path=output_video_path,
  ))
