import abc, collections, itertools
import pandas as pd
import numpy as np

from ..utils.utils import get_logger
log = get_logger(__name__)


class InvalidColumnTypeForTransform(Exception):
  pass


class TransformResult():
  def __init__(self, *args, **kwargs):
    # Working dataset and original
    self.df = None
    self.df_orig = None

    # Masks
    self.df_mask_invalids = None
    self.df_mask_drops = None

    # Data to change
    self.newcoltuples = []
    self.set_drop_idxs = set()
    self.set_drop_cols = set()

    self.set_source_cols = set()
    self.set_dest_cols = set()

  # This can't be done in the init because we don't have the data or its shape until execution time.
  def setup_data(self, df):
    self.df_orig = df
    self.df = df.copy(deep=True) if df is not None else None

    # Boolean dataframes
    self.df_mask_drops = pd.DataFrame(False, index=np.arange(df.shape[0]), columns=self.df_orig.columns)
    self.df_mask_invalids = pd.DataFrame(False, index=np.arange(df.shape[0]), columns=self.df_orig.columns)


  @property
  def list_drop_idxs(self):
    _list = list(self.set_drop_idxs)
    return sorted(_list)

  @property
  def list_drop_cols(self):
    _list = list(self.set_drop_cols)
    return sorted(_list)

  # This has to use df_orig for the col indexes to make sense.
  @property
  def list_drop_col_names(self):
    col_idxs = self.list_drop_cols
    return self.df_orig.columns[col_idxs].tolist()


  def get_new_colnames(self):
    return [coltuple.name for coltuple in self.newcoltuples]


  def add_new_col(self, name, vals, dtype):
    col = pd.Series(vals, dtype=dtype)
    coltuple = ColTuple(name=name, col=col)
    self.newcoltuples.append(coltuple)
    self.set_dest_cols.add(name)


  # Cols can be a single column or a list-like.
  def add_col_drops(self, colnames):
    col_idxs = [self.df.columns.get_loc(name) for name in colnames]
    self.set_drop_cols |= set(col_idxs)

  def remove_col_drop(self, colname):
    col_idx = self.df.columns.get_loc(colname)
    self.set_drop_cols.remove(col_idx)

  def __str__(self):
    return f'<{type(self).__name__}, newcols={self.get_new_colnames()}, list_drop_cols={self.list_drop_cols}, list_drop_idxs={self.list_drop_idxs}>'

  __repr__ = __str__



ColTuple = collections.namedtuple('ColTuple', 'name, col')

class Transform(abc.ABC):

  def __init__(self, *args, **kwargs):
    self.options = kwargs.copy()
    self.result = TransformResult()
    self.new_dtype = None

    # Can be overridden
    self.keep_original_columns = False


  def execute(self, tcon):
    self.result.setup_data(tcon.df_current)

    self.add_column_drops()
    self.set_new_dtype()

    # Some transforms don't need to process row-by-row.
    if self.do_process_table():
      self.process_table()

    self.process_result()

    return self.result


  def process_result(self):
    self.process_dataframe_changes()


  def drop_rows(self):
    drop_idxs = self.result.list_drop_idxs  # Computed, so could be expensive
    # log.debug(f'Dropping rows: {drop_idxs}')

    if not drop_idxs:
      return

    self.result.df.drop(drop_idxs, inplace=True)
    self.result.df.reset_index(drop=True, inplace=True)


  # Drop columns first, then rows.
  def process_dataframe_changes(self):
    drop_col_idxs = self.result.list_drop_cols
    coltuples = self.result.newcoltuples

    newcolnames = self.result.get_new_colnames()

    # log.debug(f'Drop columns: {drop_col_idxs}, replacements={newcolnames}')

    # Split into replacement and straight add/drop lists
    drop_cols_idxs_replace, coltuples_replace, drop_cols_idxs_simple, coltuples_simple = get_list_remainders(drop_col_idxs, coltuples)
    # log.debug(f'{drop_cols_idxs_replace}, {coltuples_replace}, {drop_cols_idxs_simple}, {coltuples_simple}')

    # If we have any matching drop/additions, perform the replacements.
    for drop_col_idx, coltuple in zip(drop_cols_idxs_replace, coltuples_replace):
      col = coltuple.col if coltuple else None
      name = coltuple.name if coltuple else None
      self.result.df = replace_dataframe_column(self.result.df, drop_col_idx, col, name)


    # Now drop any remaining drop columns (reverse order)
    drop_col_names_simple = [self.result.df.columns[idx] for idx in drop_cols_idxs_simple]
    if drop_col_names_simple:
      self.result.df.drop(drop_col_names_simple, axis='columns', inplace=True)

    # Then add any remaining new columns
    for coltuple in coltuples_simple:
      self.result.df[coltuple.name] = coltuple.col

    # After the above, dropping rows should be simple :)
    self.drop_rows()

    log.info(f'''Changes:   {type(self).__name__}
\tNew cols:\t{newcolnames}\n\tDropped cols:\t{self.result.list_drop_col_names}
\tDropped_rows:\t{len(self.result.list_drop_idxs)}.
\tColumns:\t{self.result.df.shape[1]}
\tRows:\t\t{self.result.df.shape[0]}''')


  def get_invalid_replacement(*args):
    return None

  def transform_values(self, context, index, *args):
    return args[0]

  def add_column_drops(self):
    pass

  def set_new_dtype(self):
    pass

  def process_table(self):
    pass

  def do_process_table(self):
    return True

  def __str__(self):
    return f'{type(self).__name__}, options={str(self.options)}'

  __repr__ = __str__



# Drops a single column and replaces it with the new column.
def replace_dataframe_column(df, drop_col_idx, newcol, newcol_name):
  # log.debug(f'Dropping column {drop_col_idx}: {df.columns[drop_col_idx]}')
  drop_col_name = df.columns[drop_col_idx]
  df.drop(drop_col_name, axis='columns', inplace=True)

  # log.debug(f'Inserting {newcol_name} at index {drop_col_idx}')
  df.insert(drop_col_idx, newcol_name, newcol)

  return df



# Given two lists, return two lists with the shared minimum length, then return two lists with the remainder
# E.g. given [1, 2, 3] and [a, b, c, d, e, f]:
# this will return [1, 2, 3], [a, b, c], [], [d, e, f]
def get_list_remainders(a, b):
  num_a = len(a)
  num_b = len(b)
  num_min = min(num_a, num_b)

  return a[:num_min], b[:num_min], a[num_min:], b[num_min:]


# Todo: this doesn't really work for strings
# Todo: also, need to dedupe columns if one appears multiple times
# Select columns based on Pandas dtype
def expand_dtype_columns(df, cols):
  cols_output = []

  # This supports multiple column dtypes like ['@object', '@number']
  for col in cols:
    if col in ['@object', '@number', '@datetime', '@bool']:
      dtype = col[1:]
      cols_by_dtype = df.select_dtypes(dtype).columns
      log.debug(f'Cols for dtype matching {dtype}: {cols}')
      cols_output += list(cols_by_dtype)
    else:
      cols_output += [col]

  # Remove dupes, if any
  cols_output_clean = []
  # cols_output = list(set(cols_output))
  for i in cols_output:
    if i not in cols_output_clean:
      cols_output_clean.append(i)

  return cols_output_clean
