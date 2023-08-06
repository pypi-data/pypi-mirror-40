import os

from .data_context import DataContext
from .core.transform_core import Transform
from .load import get_dataframe_from_sql, get_dataframe_from_csv, get_dataframe_from_json
from ..utils import dbutils

from datamode.utils.utils import get_logger
log = get_logger(__name__)

DEFAULT_SAMPLE_SEED = 42

class SourceData(Transform):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.dc = DataContext(options=kwargs)

  def source_sql(self, current_context):
    get_from_sql = None

    if self.options.get('query', None):
      get_from_sql = self.options['query']
    elif self.options.get('queryfile', None):
      with open(self.options['queryfile'], 'r') as f:
        get_from_sql = f.read()
    elif self.options.get('table', None):
      get_from_sql = self.options['table']

    df = get_dataframe_from_sql(current_context['__conn'], get_from_sql)

    return df

  def execute(self, tcon):
    dfname = self.options.get('dfname', None)
    data_type = self.dc.discover_data_type(tcon)

    # Filetype sourcing
    if data_type.upper() in dbutils.ALL_FILE_TYPES:
      source_path = self.options['path']
      tcon.protected_sinks.append(source_path)

      if data_type.upper() in dbutils.CSV_TYPES:
        df = get_dataframe_from_csv(source_path, self.options.get('sample_ratio'), self.options.get('sample_seed', DEFAULT_SAMPLE_SEED))
      elif data_type.upper() in dbutils.JSON_TYPES:
        df = get_dataframe_from_json(source_path, self.options.get('sample_ratio'), self.options.get('sample_seed', DEFAULT_SAMPLE_SEED))
      if not dfname:
        _fname = os.path.split(source_path)[1]
        dfname = os.path.splitext(_fname)[0]

    # Dataframe sourcing
    elif data_type.upper() in dbutils.ALL_DATAFRAME_TYPES:
      df = self.options['df']

      # Fix for column names that aren't strings:
      df.rename(columns=lambda x: str(x), inplace=True)

      if not dfname:
        dfname = 'my_df'

    # SQL sourcing
    elif data_type.upper() in dbutils.ALL_SQL_TYPES:
      table = self.options.get('table', None)
      if not dfname:
        dfname = table if table else 'my_source_sql_df'
      if table:
        tcon.protected_sinks.append(table)

      self.dc.ensure_sql_conn(tcon)
      current_conn_name = tcon.get_conn_meta('current_conn')
      current_context = tcon.get_conn_config(current_conn_name)
      df = self.source_sql(current_context)
    else:
      raise TypeError(f'Type `{data_type}` is not recognized or supported at this time.')

    if tcon.ds.has_df(dfname):
      raise ValueError(f'SourceData: Dataset named `{dfname}` already exists.')  # Todo: create custom exception?

    tcon.current_table = dfname

    self.result.df = df
    log.info(f'Loaded table {dfname}')

    return self.result


class SinkData(Transform):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.dc = DataContext(options=kwargs)

  def execute(self, tcon):
    log.debug(f'Protected table names and file paths: {tcon.protected_sinks}')
    dfname = self.options.get('dfname', None)
    data_type = self.dc.discover_data_type(tcon)

    df = tcon.df_current

    if data_type.upper() in dbutils.ALL_FILE_TYPES:
      sink_path = self.options['path']
      if sink_path in tcon.protected_sinks:
        raise ValueError(f'The path `{sink_path}` was used to source data thus cannot be used to sink.')

      if data_type.upper() in dbutils.CSV_TYPES:
        df.to_csv(sink_path)
      elif data_type.upper() in dbutils.JSON_TYPES:
        df.to_json(sink_path, orient='records', lines=True)

    elif data_type.upper() in dbutils.ALL_SQL_TYPES:
      table = self.options.get('table', None)
      dfname = table if table else 'my_sink_sql_df'
      if table in tcon.protected_sinks:
        raise ValueError(f'The table `{table}` was used to source data and thus cannot be used to sink.')

      self.dc.ensure_sql_conn(tcon)
      current_conn_name = tcon.get_conn_meta('current_conn')
      current_context = tcon.get_conn_config(current_conn_name)
      df.to_sql(table, current_context['__conn'], if_exists=self.options.get('if_exists', 'replace'))
      log.info(f'Wrote data `{dfname}` to SQL table `{table}`.')
    else:
      raise TypeError(f'Type `{data_type}` is not recognized or supported at this time.')

    self.result.df = df

    return self.result


###########################
### Convenience classes ###
###########################

## Sources ##
# Source SQL
class SourceSql(SourceData):
  def __init__(self, table, dfname=None, query=None, queryfile=None, *args, **kwargs):
    super().__init__(table=table, dfname=dfname, query=query, queryfile=queryfile, *args, **kwargs)


class SourceQueryFile(SourceData):
  def __init__(self, queryfile, dfname='my_query_file', *args, **kwargs):
    super().__init__(queryfile=queryfile, dfname=dfname, *args, **kwargs)


class SourceInline(SourceData):
  def __init__(self, query, dfname='my_inline_query', *args, **kwargs):
    super().__init__(query=query, dfname=dfname, *args, **kwargs)


class SourceTable(SourceData):
  def __init__(self, table, *args, **kwargs):
    super().__init__(table=table, *args, **kwargs)


# Source File
class SourceFile(SourceData):
  def __init__(self, path, *args, **kwargs):
    super().__init__(path=path, *args, **kwargs)


# Source Dataframe
class SourceDF(SourceData):
  def __init__(self, df, dfname='my_dataframe', *args, **kwargs):
    super().__init__(df=df, dfname=dfname, *args, **kwargs)


## Sinks ##
# Sink SQL
class SinkTable(SinkData):
  def __init__(self, table, *args, **kwargs):
    super().__init__(table=table, *args, **kwargs)


# Sink File
class SinkFile(SinkData):
  def __init__(self, path, *args, **kwargs):
    super().__init__(path=path, *args, **kwargs)


## Switching/Setting ##
class SetWorkingTable(Transform):
  def __init__(self, dfname, *args, **kwargs):
    super().__init__(dfname=dfname, *args, **kwargs)

  def execute(self, tcon):
    dfname = self.options['dfname'] # Required

    tdf = tcon.ds.tstate_last
    df = tdf.get_df(dfname)

    if df is not None:
      tcon.current_table = dfname
      self.result.df = df
    else:
      raise Exception(f'The table name {dfname} could not be found')

    return self.result
