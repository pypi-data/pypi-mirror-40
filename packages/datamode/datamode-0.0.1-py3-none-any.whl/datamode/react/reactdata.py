# https://pandas.pydata.org/pandas-docs/stable/api.html#data-types-related-functionality
from pandas.api.types import is_datetime64_any_dtype
from pandas.api.types import is_numeric_dtype

from .stats import build_column_stats, BARCHART_MAX_ITEMS
from ..utils.utils import is_basic_type

from datamode.utils.utils import get_logger
log = get_logger(__name__)

# Data management class to pick subsets of the existing dataset, especially for showing to React code.
class ReactData():
  def __init__(self, tcon, timer, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.tcon = tcon
    self.transforms = tcon.transforms
    self.timer = timer

  def get_source_dataframe(self, transform_id):
    return self.tcon.ds.tstates[transform_id].get_working_df()

  def get_df_dest_at_transform_id(self, transform_id):
    return self.tcon.ds.tstates[transform_id].dest_tables[0]

  def get_filtered_df(self, transform_id, facets):
    df_source = self.get_source_dataframe(transform_id)
    df = df_source.copy(deep=True)

    # Build a new faceted dataframe - facets are ANDed together
    # Each facet can be:
    #   None -> show all Nones  (nulls in JS of course)
    #   List of two items -> filter by range
    #   Single value - filter the single value only.
    for colname, entry in facets.items():
      # Special handling for a raw None value (null in JS)
      if entry is None:
        df = df.loc[ df[colname].isnull() ]  # Filter by null values

      # Dictionary - later on, can be used for explicit NOT filters as well
      elif type(entry) is dict and 'isnull' in entry:
        if entry['isnull']:
          df = df.loc[ df[colname].isnull() ]  # Filter by null values
        else:
          df = df.loc[ df[colname].notnull() ]  # Filter by nonnull values

      # Range
      elif type(entry) is list:
        mask_start = df[colname] > entry[0]
        mask_end = df[colname] <= entry[1]
        df = df.loc[ mask_start & mask_end ]

      # Single value
      elif is_basic_type(entry):
        df = df.loc[ df[colname] == entry ]  # Filter by basic type

      # Unsupported
      else:
        raise Exception(f'Facet colname={colname}, entry={entry} has unsupported type.' )

    return df


  def get_colinfos(self, transform_id, df):
    colnames = df.columns.tolist()
    source_cols, dest_cols = self.get_source_and_dest_cols(transform_id)

    colinfos = []
    for colname in colnames:
      col = df[colname]

      # Dictionary: dict keys are the unique dataset values; dict values are the counts.
      distinct_counts = col.value_counts(dropna=False)
      # self.timer.report('unique counts: {distinct_counts.shape[0]}')

      colviz_type = self.determine_colviz_type(col, distinct_counts)
      # self.timer.report('colviz_type: {colviz_type}')

      stats = build_column_stats(col, colviz_type, distinct_counts)
      # self.timer.report('stats built: {distinct_counts.shape[0]}')


      dtype = df[colname].dtype

      colinfo = {
        'colname': colname,
        'colviz_type': colviz_type,
        'dtype': str(dtype),
        'is_datetime': is_datetime64_any_dtype(dtype), # This could probably be computed higher up and cached
        'stats': stats,
        'source_col': colname in source_cols,
        'dest_col': colname in dest_cols,
      }

      colinfos.append(colinfo)

    return colinfos


  def get_source_and_dest_cols(self, transform_id):
    tresult = self.tcon.ds.tstates[transform_id].result
    return list(tresult.set_source_cols), list(tresult.set_dest_cols)


  def get_distinct_nonnulls(self, distinct_counts):
    has_nulls = distinct_counts.index.isnull().any()
    counts = distinct_counts.shape[0]

    # Strip one from the total if it has nulls.
    return (counts - 1) if has_nulls else counts


  def determine_colviz_type(self, col, distinct_counts):
    # aak hack just for demo
    # TODO: REMOVE
    if col.name.lower() == 'state':
      return 'geo'

    # Datetimes will always get a histogram.
    if is_datetime64_any_dtype(col):
      return 'histogram'

    # If the values are all unique (except nulls), don't bother showing a histogram, just give the stats.
    # pandas .count() explicitly excludes nulls and null-equivalents
    if self.get_distinct_nonnulls(distinct_counts) == col.count():
      return 'summary'

    # If we have a categorical variable (including low-ordinal numerics and bools), just use a barchart.
    if distinct_counts.shape[0] <= BARCHART_MAX_ITEMS:
      return 'barchart'

    if is_numeric_dtype(col.dtype):
      return 'histogram'

    elif col.dtype == 'object':
      return 'barchart'

    else:
      raise Exception(f'Couldn\'t determine colviz type, locals={locals()}')
