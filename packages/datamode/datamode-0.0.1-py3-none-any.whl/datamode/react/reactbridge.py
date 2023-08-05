import json, pprint
from collections import defaultdict
from IPython.display import display

import pandas as pd
import pyarrow as pa

from .altair import build_altair_spec
from .features_app import FeaturesApp
from .arrow import serialize_to_arrow
from ..utils.utils import get_sha1_hash_from_int, get_sha1_hash_from_buffer, DatamodeJsonEncoder, log_exception_with_context
from ..utils.timer import CustomTimer

from datamode.utils.utils import get_logger
log = get_logger(__name__)


class ReactBridge():
  def __init__(self, reactdata, timer, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.reactdata = reactdata
    self.timer = timer

  # Todo: not threadsafe!
  def handle_comm_msg(self, comm, msg):
    comm_data = None

    try:
      # Get the filters
      msg_data = msg['content']['data']
      msgtype = msg_data['msgtype']

      log.debug(f'\n-------------- Message {msgtype} received ---------------------------')
      self.timer = CustomTimer(log, msgtype)
      buffers = None

      if msgtype == 'transform_frame':
        transform_id = msg_data['transform_id']
        facets = msg_data.get('facets', {})  # Default to empty dict

        # Actually filter the data
        df = self.reactdata.get_filtered_df(transform_id, facets)
        table = self.reactdata.get_df_dest_at_transform_id(transform_id)

        # Send it back over the wire
        self.timer.report(f'About to marshal data for transform_id={transform_id}, table={table}')
        comm_data = self.marshal_metadata(df, transform_id, table, facets)
        comm_data['msgtype'] = 'transform_frame_response'

        compress = True
        comm_data['compress'] = compress
        buffer = serialize_to_arrow(df, compress=compress, timer=self.timer)
        buffers = [buffer]

        comm_data['snapshot_hash'] = self.create_snapshot_hash(comm_data, buffer)


      elif msgtype == 'altair':
        transform_id = msg_data['transform_id']
        facets = msg_data.get('facets', {})  # Default to empty dict
        log.debug(msg_data)

        df = self.reactdata.get_filtered_df(transform_id, facets)
        altair_options = msg_data['altair_options']
        altair_spec = build_altair_spec(df, altair_options),

        comm_data = {
          'msgtype': 'altair_response',
          'altair_spec': altair_spec,
        }


      _td_elapsed, td_total = self.timer.report()
      comm_data['elapsed'] = td_total.total_seconds()

      if comm_data:
        comm.send(comm_data, buffers=buffers)
        self.timer.end('Sent comm_data')

      else:
        self.timer.end('No comm data to send')

    except Exception as e:
      comm_str = pprint.pformat(comm)
      msg_str = pprint.pformat(msg)
      comm_data_str = 'not pprinted'
      # comm_data_str = pprint.pformat(comm_data)

      # Change print_locals to True to see details here
      log_exception_with_context(log, e, f'Exception {e.__class__.__name__} caught in handle_comm_msg:\n\ncomm:\n{comm_str}\n\nmsg:\n{msg_str}\n\ncomm_data:\n{comm_data_str}\n', print_locals=False)
      # self.timer.report('Logged exception')
      raise e


  def marshal_metadata(self, df, transform_id, table, facets={}):
    colinfos = self.reactdata.get_colinfos(transform_id, df)
    self.timer.report('Finished getting colinfos and table')

    metadata = {
      'transform_id': transform_id,
      'table': table,
      'facets': facets,
      'columns': colinfos,
    }

    return metadata


  # taglist_by_colname is a dict where key=colname, value=taglist.
  # taglist is a set of string tags that apply to the cell.
  def build_taglist_by_colname(self, record):
    taglist_by_colname = defaultdict(list)

    for colname, value in record.items():
      # Set null values
      if value is None:
        taglist_by_colname[colname].append('null')
      if value == 'home_page':
        taglist_by_colname[colname].append('invalid')

    return dict(taglist_by_colname)


  def display(self, timer=None):
    # Initial transform_id - the last transform
    transform_id = self.reactdata.tcon.ds.tstate_count - 1

    # Package everything for React
    tstates = self.reactdata.tcon.ds.tstates

    transform_entries = []
    for index, tstate in enumerate(tstates):
      entry = {
        'transform': str(tstate.transform),
        'index': index,
        'elapsed': tstate.elapsed.total_seconds()
      }

      transform_entries.append(entry)

    props = {
      'transform_entries': transform_entries,
      'initial_transform_id': transform_id,
    }


    # # Enable debugging comm data from display
    # breakpoint()
    # transform_id = 3  # If you need it. It's already defined above
    # facets = {}
    # facets = {'timestamp': None }
    # df = self.reactdata.get_filtered_df(transform_id, facets)
    # self.reactdata.get_colinfos(transform_id, df)
    # comm_data = self.marshal_metadata(df, transform_id, 'dummy_table', facets)
    # self.serialize_to_arrow(df)


    # Create the component and actually display it in the notebook
    react_features_app = FeaturesApp(handler=self.handle_comm_msg, props=props)
    display(react_features_app)
    self.timer.report('Completed Jupyter display')


  def create_snapshot_hash(self, comm_data, buffer):
    # Sort keys guarantees an ordered dict every time.
    # Not the fastest thing though, todo: investigate perf.
    comm_data_json = (json.dumps(comm_data, sort_keys=True, cls=DatamodeJsonEncoder))
    self.timer.report('Completed comm_data sha1 hash')

    buffer_reader = pa.BufferReader(buffer)
    buffer_sha1 = get_sha1_hash_from_buffer(buffer_reader)
    self.timer.report(f'Completed buffer sha1 hash')

    return get_sha1_hash_from_int( hash(comm_data_json) + hash(buffer_sha1) )
