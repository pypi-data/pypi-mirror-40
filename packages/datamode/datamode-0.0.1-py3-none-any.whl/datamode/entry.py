import pprint, logging, threading
import pandas as pd

from .transforms.core.context import TransformContext
from .transforms.db_transforms import SourceFile, SourceDF
from .react.reactbridge import ReactBridge
from .react.reactdata import ReactData
from .utils.timer import CustomTimer
from .utils.notebook import in_ipynb
from .utils.yamlutils import load_yaml
from .utils.validator import validate_yaml_data_connections
from .utils.usageutils import send_anonymous_usage
from .settings import DEFAULT_CONFIG_DIR, CONFIG_DIR, AUID

from datamode.utils.utils import get_logger
log = get_logger(__name__)

class Executor():

  def __init__(self, tcon, timer=None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.tcon = tcon
    self.timer = timer

  def cute_transforms(self, trs):
    tr_names = [str(tr) for tr in trs]
    tr_names_str = pprint.pformat(tr_names)
    log.info(f'Transforms:\n{tr_names_str}')

    for tr in trs:
      result = tr.execute(self.tcon)
      if self.timer:
        elapsed, _total = self.timer.report(f'Completed {str(tr)}.')

      # Save the result to our context.
      if result:
        self.tcon.add_result(tr, result, elapsed)


def execute_transforms(tcon, trs, timer=None):
  exe = Executor(tcon, timer)
  exe.cute_transforms(trs)


# Main entry point
# tcon is a TransformContext obj. The caller can add raw datasets to it,
# or it can have an engine/conn defined to read data from one or more source transforms.
# For typical usage, see __main__.py.

# Logging defaults to DEBUG but can be turned off by passing loglevel=None.
def run_transforms(transforms, display_results='notebook', loglevel=logging.DEBUG, usage_type='direct'):
  if loglevel:
    set_loglevel(loglevel)

  tcon = TransformContext()
  send_anon_usage = True
  # loading config
  yaml_filepath, yaml_config = load_yaml(DEFAULT_CONFIG_DIR)
  if yaml_config:
    validate_yaml_data_connections(yaml_config)
    tcon.yaml_config = yaml_config['connections']
    log.debug(f'Using YAML from {yaml_filepath}')

    # anon usage: permissions
    if yaml_config.get('config', None):
      send_anon_usage = yaml_config['config'].get('send_anonymous_usage', True)

    # add conns to conn_context and assign default if explicitly named or only 1 conn exists
    for conn_name, conn_config in tcon.yaml_config.items():
      tcon.integrate_conn_config(conn_name, conn_config)
      if conn_config.get('default', False) == True or len(tcon.yaml_config) == 1:
        tcon.set_conn_meta('default_conn', conn_name)
  else:
    log.warning('A YAML file was not found. If this is expected please ignore this warning.')

  timer = CustomTimer(log, f'Execute transforms')
  execute_transforms(tcon, transforms, timer)
  tcon.close_conns()
  timer.end()

  log.info('\n' + tcon.summary())

  # anon usage: send
  if send_anon_usage:
    thr = threading.Thread(target=send_anonymous_usage, args=([AUID]), kwargs={'usage_type': usage_type})
    thr.start()

  if display_results == 'notebook' and in_ipynb():
    show_results(tcon)

  return tcon

# Run this in Jupyter notebook to display the GUI.
def show_results(tcon):
  timer = CustomTimer(log, f'Display results')
  rdata = ReactData(tcon, timer=timer)
  bridge = ReactBridge(rdata, timer=timer)
  bridge.display()
  timer.end()


def set_loglevel(loglevel=logging.DEBUG):
  logger = logging.getLogger()
  logger.setLevel(loglevel)


# Super simple way to display a DataFrame or csv file in the UI.
def quickshow(input_data):
  transform = None

  if isinstance(input_data, pd.DataFrame):
    transform = SourceDF(input_data)
  elif type(input_data) == str:
    transform = SourceFile(input_data)
  else:
    print ('quickshow() supports a pandas DataFrame or a string with the name/path of a local csv file.')

  _tcon = run_transforms( [transform], usage_type='quickshow' )
