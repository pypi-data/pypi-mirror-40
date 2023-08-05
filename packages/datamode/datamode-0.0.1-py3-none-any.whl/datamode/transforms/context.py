# Wrapper class for multiple dataframes and metadata.
class Dataset():
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # An ordered list of TransformStates, one for each transform step.
    self.tstates = []

  @property
  def tstate_first(self):
    return self.tstates[0] if self.tstates else None

  @property
  def tstate_last(self):
    return self.tstates[-1] if self.tstates else None

  @property
  def tstate_count(self):
    return len(self.tstates)

  def has_df(self, name):
    tstate = self.tstate_last
    return tstate.has_df(name) if tstate else False

  def add_tstate(self, tstate):
    self.tstates.append(tstate)

  # Pass in the transform_id that you want - defaults to the last state.
  def summary(self, transform_id=-1):
    if not self.tstates:
      return 'Empty dataset'

    tstate = self.tstates[transform_id]
    return tstate.summary()

  def __str__(self):
    transforms = [str(tstate.transform.__class__.__name__) for tstate in self.tstates]
    return ', '.join(transforms)

  def __repr__(self):
    return f'<{type(self).__name__}: {str(self)} ({len(self.tstates)})>'

  def debug_summary(self):
    transforms = [f'{index}: {str(tstate.transform)}' for index, tstate in enumerate(self.tstates) ]
    return '\n'.join(transforms)

  def dump(self):
    dump = f'*** {type(self).__name__} - {len(self.tstates)} tstates ***\n'
    dump += self.debug_summary() + '\n'
    for tstate in self.tstates:
      dump += tstate.dump() + '\n'

    return dump


class TransformState():
  def __init__(self, transform=None, result=None, tstate_orig=None, elapsed=None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.dfs = {}  # Dict of dataframes
    self.transform = transform
    self.result = result  # Legacy until we can refactor this
    self.source_tables = []
    self.dest_tables = []
    self.working_table = None
    self.elapsed = elapsed

    if tstate_orig:
      self.copy_dataframes_from_other(tstate_orig)

  def set_df(self, name, df):
    self.working_table = name
    self.dfs[name] = df

    # Todo: this will have to be refactored when we actually work with multiple tables.
    self.source_tables.append(name)
    self.dest_tables.append(name)

  def get_working_df(self):
    return self.get_df(self.working_table)

  def get_df(self, name):
    return self.dfs[name] if name in self.dfs else None

  def has_df(self, name):
    return name in self.dfs

  def copy_dataframes_from_other(self, other_tstate):
    # Intentional shallow copy.
    # We want to keep refs to dataframes but not dupe them unless necessary
    self.dfs = other_tstate.dfs.copy()

  @property
  def table_names(self):
    return self.dfs.keys()

  def summary(self):
    summary = ''
    for name, df in self.dfs.items():
      summary += f'{name}:\n'
      summary += str(df.head()) + '\n\n'

    return summary

  def __str__(self):
    return f'tables ({len(self.dfs)}): '+ ', '.join(self.dfs.keys())

  def __repr__(self):
    return f'<{type(self).__name__}: {str(self)}>'

  def dump(self):
    dump = self.__repr__() + '\n'
    for name, df in self.dfs.items():
      dump += f'{name}:\n'
      dump += str(df.head()) + '\n\n'

    return dump

class TransformContext():
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.conn_context = {
        '_meta': {
          'cnt': 0,
          'current_conn': None,
          'default_conn': None,
        },
        '_context': {},
      }
    self.yaml_config = {}
    self.protected_sinks = []
    self.ds = Dataset()  # Working dataset
    self.current_table = ''

  def add_result(self, transform, result, elapsed):
    # Copy the latest tstate into the new one.
    tstate = TransformState(transform, result, self.ds.tstate_last, elapsed)  # tstate_last can be None
    tstate.set_df(self.current_table, result.df)

    self.ds.add_tstate(tstate)

  def summary(self):
    summary = '------------------------ Output ----------------------------\n\n '
    return summary + self.ds.summary()

  # Can be None
  @property
  def df_current(self):
    tstate = self.ds.tstate_last

    if not tstate or not self.current_table:
      return None

    return tstate.get_df(self.current_table)

  @property
  def transforms(self):
    return [tstate.transform for tstate in self.ds.tstates]

  def get_conn_meta(self, key=None):
    if key:
      return self.conn_context['_meta'][key]
    else:
      return self.conn_context.get('_meta', {})

  def set_conn_meta(self, key, data):
    self.conn_context['_meta'][key] = data

  def get_conn_config(self, conn_name, default_return=None):
    return self.conn_context.get('_context', {}).get(conn_name, default_return)

  def integrate_conn_config(self, conn_name, conn_config={}):
    if not conn_config.get('type', None):
      raise Exception(f'The connection named {conn_name} must specify `type` but received {conn_config}.')
    # if config with same name exists - replace it entirely
    self.conn_context['_context'].update({conn_name: conn_config})
    self.conn_context['_meta']['cnt'] = len(self.conn_context['_context'].keys())

  def close_conns(self):
    for conn, conn_config in self.conn_context['_context'].items():
      if conn_config.get('__conn', None):
        conn_config['__conn'].close()
        conn_config['__engine'].dispose()

  def __str__(self):
    return f'current_table={self.current_table}, ds={self.ds}'

  def __repr__(self):
    return f'<{type(self).__name__}: {str(self)}>'
