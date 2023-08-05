import altair as alt

from pandas.api.types import is_numeric_dtype, is_bool_dtype, is_object_dtype, is_datetime64_any_dtype

from datamode.utils.utils import get_logger
log = get_logger(__name__)


def get_altair_encoding(dtype):
  # quantitative
  if is_numeric_dtype(dtype):
    return 'Q'

  # ordinal
  if is_bool_dtype(dtype):
    return 'O'

  # nominal
  if is_object_dtype(dtype):
    return 'N'

  # temporal
  if is_datetime64_any_dtype(dtype):
    return 'T'

  raise Exception('Pandas dtype not mapped for altair.')


def build_altair_spec(df, altair_options):
  # log.debug(altair_options)

  axis=alt.Axis(
    tickCount=9,
  )

  # Decorate the dataset for specific dtypes.
  for key, colname in altair_options.items():
    col = df[colname]
    altair_options[key] = colname + ':' + get_altair_encoding(col.dtype)

  encode_options = []

  # Encode
  if 'x' in altair_options:
    encode_options.append(
      alt.X(
        altair_options['x'],
        axis=axis,
        scale=alt.Scale(zero=False),
      )
    )

  if 'y' in altair_options:
    encode_options.append(
      alt.Y(
        altair_options['y'],
        axis=axis,
        scale=alt.Scale(zero=False),
      )
    )


  if 'color' in altair_options:
    encode_options.append(alt.Color(altair_options['color']))

  # dummy_url.json is intended to make Altair think we're passing in a url later.
  # Instead, we'll pass the data into vega-lite directly.
  chart = alt.Chart('dummy_url.json').mark_point().encode( *encode_options )

  chart = chart.configure(**{
    'autosize': 'fit',
  })

  chart = chart.configure_axis(**{
    'labelOverlap': 'parity',
  })

  spec = chart.to_json()
  log.debug(f'Altair spec:\n{spec}')

  return spec
