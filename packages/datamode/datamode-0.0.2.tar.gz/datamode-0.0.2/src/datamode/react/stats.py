import math, itertools, pprint
import pandas as pd
import numpy as np

from datamode.utils.data import is_value_nan_equivalent, is_col_vector, pad_csr_matrix

from sklearn.feature_extraction.text import TfidfVectorizer

# https://pandas.pydata.org/pandas-docs/stable/api.html#data-types-related-functionality
from pandas.api.types import is_datetime64_any_dtype
from pandas.api.types import is_numeric_dtype



from datamode.utils.utils import get_logger
log = get_logger(__name__)

# Currently, the Vega object expects data in this format (jsonl):
# data = {
#   'table': [
#     { label: 'Terminator', value_count: 21 },
#     { label: 'Commando', value_count: 81 },
#   ]
# }

BIN_COUNT = 8
BARCHART_MAX_ITEMS = 10

class StatsBuilder():
  def __init__(self, col, colname, timer, *args, **kwargs):
    super(*args, **kwargs)
    self.col = col
    self.colname = colname
    self.colviz_type = None
    self.distinct_counts = None
    self.timer = timer

  def build_column_stats(self):
    self.get_distinct_counts()
    self.colviz_type = self.determine_colviz_type()

    null_count = self.col.isna().sum()

    stats = {
      'col_stats': {
        'count': self.col.shape[0],
        'valids': self.col.shape[0] - null_count,
        'nulls': null_count,
      },
    }

    # If we don't have any colviz, just build summary stats.
    if self.colviz_type == 'summary':
      stats['summary'] = self.build_summary_stats()
    elif self.colviz_type == 'histogram':
      stats['bins'] = self.build_bins()
    elif self.colviz_type == 'vector':
      stats['vector_stats'] = self.build_vector_stats()
    elif self.colviz_type == 'wordcloud':
      stats['wordcounts'] = self.build_wordcloud_stats()

    if self.distinct_counts is not None:
      stats['distinct_counts'] = self.build_distinct_counts_jsonl()

    # log.debug(pprint.pformat(stats))

    # self.timer.report(f'col={colname} stats built: {self.distinct_counts.shape[0]}')
    # self.timer.report(f'col={colname} colviz_type={colviz_type}')

    return stats


  # https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.cut.html
  # Note: Pandas extends the range by 0.1% on each side to include the entire dataset.
  # This means you can have a bin starting negative if the values start close to 0.
  def build_bins(self):
    # We can't work with null values, whether it's a numerical or datetime histogram.
    # If we only have null values, bail.
    if self.col.count() == 0:  # Count explicitly excludes nulls
      return []

    # Get rid of infinite values
    # See https://github.com/pandas-dev/pandas/issues/24314 for why this fails
    self.col = self.col.replace([np.inf, -np.inf], np.nan)

    cat = pd.cut(self.col, BIN_COUNT, include_lowest=True, duplicates='drop')
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
  def build_summary_stats(self):
    return self.col.describe().to_dict()


  def build_distinct_counts_jsonl(self):
    distinct_counts_jsonl = []

    # Itertools.islice returns the first N items of the iterator.
    for label, count in itertools.islice(self.distinct_counts.items(), BARCHART_MAX_ITEMS):
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



  def determine_colviz_type(self):
    # aak hack just for demo
    # TODO: REMOVE
    if self.col.name.lower() == 'state':
      return 'geo'

    if is_col_vector(self.col):
      return 'vector'

    # Datetimes will always get a histogram.
    if is_datetime64_any_dtype(self.col):
      return 'histogram'

    if is_numeric_dtype(self.col.dtype):
      return 'histogram'


    # if self.colname == 'reviewText_':
    #   return 'wordcloud'

    # If the values are all unique (except nulls), don't bother showing a histogram, just give the stats.
    # pandas .count() explicitly excludes nulls and null-equivalents
    if self.distinct_counts is not None:
      if self.get_distinct_nonnulls() == self.col.count():
        return 'summary'

      # If we have a categorical variable (including low-ordinal numerics and bools), just use a barchart.
      if self.distinct_counts.shape[0] <= BARCHART_MAX_ITEMS:
        return 'barchart'


    if self.col.dtype == 'object':
      # todo: avoid nulls for this check
      # if type(self.col.iloc[0]) == str:
      #   return 'wordcloud'

      return 'barchart'
    else:
      raise Exception(f'Couldn\'t determine colviz type, locals={locals()}')


  # Dictionary: dict keys are the unique dataset values; dict values are the counts.
  def get_distinct_counts(self):
    # Don't calculate distinct counts for vectors.
    if is_col_vector(self.col):
      return

    try:
      self.distinct_counts = self.col.value_counts(dropna=False)
    except TypeError:
      # This means we can't calculate distinct_counts, which is fine.
      pass

    # self.timer.report(f'col={colname} distinct counts: {self.distinct_counts.shape[0]}')


  # Output format:
  # {text: "foo", count: 10 }


  # Todo: change back to countvectorizer.
  def build_wordcloud_stats(self):
    valids = self.col.dropna()
    vectorizer = TfidfVectorizer()
    wordcount_vectors = vectorizer.fit_transform(valids)
    squashed = wordcount_vectors.toarray().sum(axis=0)
    words = vectorizer.get_feature_names()

    wordcounts = [{'text': word, 'count': count} for (word, count) in zip(words, squashed.tolist() ) if count > 0.2]
    return wordcounts


  def get_distinct_nonnulls(self):
    has_nulls = self.distinct_counts.index.isnull().any()
    counts = self.distinct_counts.shape[0]

    # Strip one from the total if it has nulls.
    return (counts - 1) if has_nulls else counts

  def build_vector_stats(self):
    dims = 0

    # breakpoint()
    valids = self.col.dropna()
    if valids.shape[0] > 0:
      dims = valids.iloc[0].shape[0]

    vector_stats = {
      'dims': dims
    }

    return vector_stats
