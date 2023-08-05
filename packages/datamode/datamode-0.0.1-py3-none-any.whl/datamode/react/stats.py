import math, itertools, pprint
import pandas as pd
import numpy as np


from datamode.utils.utils import get_logger
log = get_logger(__name__)

# Currently, the Vega object expects data in this format (jsonl):
# data = {
#   'table': [
#     { label: 'Terminator', value_count: 21 },
#     { label: 'Commando', value_count: 81 },
#   ]
# }

# col is a pandas.Series object.
BARCHART_MAX_ITEMS = 10

def build_column_stats(col, colviz_type, distinct_counts):
  null_count = col.isna().sum()

  stats = {
    'table_stats': {
      'count': col.shape[0],
      'valids': col.shape[0] - null_count,
      'nulls': null_count,
    },
  }

  # If we don't have any colviz, just build summary stats.
  if colviz_type == 'summary':
    stats['summary'] = build_summary_stats(col)
  if colviz_type == 'histogram':
    stats['bins'] = build_bins(col)
  else:
    stats['distinct_counts'] = build_distinct_counts_jsonl(distinct_counts)

  # log.debug(pprint.pformat(stats))

  return stats


BIN_COUNT = 8

# https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.cut.html
# Note: Pandas extends the range by 0.1% on each side to include the entire dataset.
# This means you can have a bin starting negative if the values start close to 0.
def build_bins(col):
  # We can't work with null values, whether it's a numerical or datetime histogram.
  # If we only have null values, bail.
  if col.count() == 0:  # Count explicitly excludes nulls
    return []

  # Get rid of infinite values
  # See https://github.com/pandas-dev/pandas/issues/24314 for why this fails
  col = col.replace([np.inf, -np.inf], np.nan)

  cat = pd.cut(col, BIN_COUNT, include_lowest=True, duplicates='drop')
  counts_by_bins = cat.value_counts().sort_index() # In-place sort

  bins_jsonl = []
  for interval, count in counts_by_bins.iteritems():
    _bin = {
      'min': interval.left,
      'max': interval.right,
      'count': count,
    }

    bins_jsonl.append(_bin)

  return bins_jsonl


# See https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.describe.html
def build_summary_stats(col):
  return col.describe().to_dict()


def build_distinct_counts_jsonl(distinct_counts):
  distinct_counts_jsonl = []

  # Itertools.islice returns the first N items of the iterator.
  for label, count in itertools.islice(distinct_counts.items(), BARCHART_MAX_ITEMS):
    # Patch for NaT - neither pandas nor jupyter want to fix the NaT issue
    # Also guard against Pandas nan and Python float nan
    # breakpoint()

    if is_value_nan_equivalent(label):
      label = None

    entry = {
      'label': label,
      'count': count
    }

    distinct_counts_jsonl.append(entry)

  return distinct_counts_jsonl


def is_value_nan_equivalent(value):
  return (
    value is pd.NaT
    or isinstance(value, float) and np.isnan(value)
    or type(value) == float and math.isnan(value)
  )
