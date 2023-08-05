import numpy as np

def downsample_dataframe(df, sample_ratio=42, sample_seed=None):

  try:
    # Set the seed
    np.random.seed(sample_seed)

    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.rand.html#numpy.random.rand
    num_rows = df.shape[0]
    randoms = np.random.rand(num_rows)

    # Use percentiles to downsample df
    if 0 < sample_ratio < 1:
      perc = np.percentile(randoms, sample_ratio*100)
    elif sample_ratio < 0:
      perc = 0
    else:
      perc = 1

    sample_indices = np.argwhere(randoms <= perc)
    sample_indices = sample_indices.transpose()[0]

    # Create sampled df from indices
    df_sampled = df.iloc[ sample_indices.tolist() ]

    # We have to reset the index, otherwise downstream indexing won't work properly
    df_sampled = df_sampled.reset_index(drop=True)

    return df_sampled

  finally:
    # Reset the seed no matter what
    np.random.seed()
