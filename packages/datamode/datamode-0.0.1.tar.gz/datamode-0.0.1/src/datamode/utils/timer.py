import datetime, inspect

LOC_LENGTH = 15

class CustomTimer():
  def __init__(self, log, title, msg='Start', delay_start=False):
    self.log = log
    self.title = title
    self.start_msg = msg
    self.td_end_total = None

    if not delay_start:
      self.start()

  def start(self):
    # For inspect.stack(): https://docs.python.org/3/library/inspect.html
    caller, lineno = inspect.stack()[1].function, inspect.stack()[1].lineno
    loc = self.format_loc(caller, lineno)

    self.reset()
    self.log.debug(f'{loc} {self.title} ({self.start_msg}): current time={self.dt_start.strftime("%-I:%M:%S.%f")[:-3]}')

  def reset(self):
    self.dt_start = datetime.datetime.now()
    self.dt_last = self.dt_start

  # End is the same as report, but just marks the report as (End)
  def end(self, msg=''):
    self.report(msg, end=True)

  def timing(self):
    dt_now = datetime.datetime.now()

    # Calculate
    elapsed = dt_now - self.dt_last
    total = dt_now - self.dt_start

    # Save for the next timing calc
    self.dt_last = dt_now

    return elapsed, total

  def end_total(self):
    if not self.td_end_total:
      self.end()

    return self.td_end_total

  def format_loc(self, caller, lineno):
    loc = f'{caller}:{lineno}'
    loc = loc[:LOC_LENGTH - 2] + '..' if len(loc) > LOC_LENGTH else loc
    loc = f'[{loc: <{LOC_LENGTH}}]'
    return loc

  def report(self, msg='', end=False):
    end_str = ' (End)' if end else ''
    td_elapsed, td_total = self.timing()

    caller, lineno = inspect.stack()[1].function, inspect.stack()[1].lineno
    loc = self.format_loc(caller, lineno)

    self.log.debug(f'{loc} {self.title}{end_str}: {td_elapsed.total_seconds():0.3f}s since last step, {td_total.total_seconds():0.3f}s total. {msg}')

    # Store the results for later programmatic access
    if end:
      self.td_end_total = td_total

    return td_elapsed, td_total
