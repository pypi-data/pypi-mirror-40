import sys, os, os.path, shutil, distutils.util

# Python 3.6 check
if (sys.version_info < (3, 6)):
  raise Exception('Please install Datamode in a Python 3.6+ environment.')


from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages, setup

from setuptools.command.develop import develop as _develop
from setuptools.command.install import install as _install

# See https://mindtrove.info/4-ways-to-extend-jupyter-notebook/ for a good example on how to install/enable extensions.


# Thanks to https://stackoverflow.com/questions/17887905/python-setup-py-to-run-shell-script
class install(_install):
  def run(self):
    _install.run(self)

class develop(_develop):
  def run(self):
    # Hack to prevent data_files from executing in dev mode.
    self.distribution.data_files = []

    _develop.run(self)
    # Install the extension features_react into Jupyter Notebook
    install_jupyter_react_bridge()

    # Copy sample file to working copy
    if not os.path.exists('dev.py'):
      print ('Copied docs/dev/dev.py.sample to dev.py - edit to run your own transforms')
      shutil.copyfile('docs/dev/dev.py.sample', 'dev.py')


def install_jupyter_react_bridge():
  from notebook.nbextensions import install_nbextension

  symlink_dir = os.path.join(os.path.dirname(__file__), "js", "staticdev")
  full_dest = install_nbextension(symlink_dir, symlink=True,
                      overwrite=True, prefix=sys.prefix, user=False, destination="features_react")

  print ('Symlinked extension source={symlink_dir} to dest={full_dest}'.format(full_dest=full_dest, symlink_dir=symlink_dir))
  enable_extension_in_notebook(full_dest, symlink_dir)


def enable_extension_in_notebook(full_dest, symlink_dir):
  from notebook.services.config import ConfigManager

  cm = ConfigManager()
  cm.update('notebook', {"load_extensions": {"features_react/index": True } })
  print ('Enabled Jupyter notebook extension in {full_dest} (setup_mode=develop, symlink_dir={symlink_dir}).'.format(full_dest=full_dest, symlink_dir=symlink_dir))


# https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
# https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Distributing%20Jupyter%20Extensions%20as%20Python%20Packages.html
setup(
  name='datamode',
  cmdclass={
    'develop': develop,
    'install': install,
  },
  version='0.0.1',
  license='Apache 2.0',
  project_urls={
    'Main website': 'https://www.datamode.com',
    'Documentation': 'https://datamode.readthedocs.io/',
    'Source': 'https://github.com/datamode/datamode/',
    'Tracker': 'https://github.com/datamode/datamode/issues',
  },
  url='https://www.datamode.com',
  author='Vaughn Koch',
  author_email='code@datamode.com',
  description="A tool to quickly build data science pipelines",
  package_dir={'': 'src'},
  packages=find_packages('src'),
  py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
  include_package_data=True,  # Include everything in src/
  data_files=[
    # like `jupyter nbextension install --sys-prefix`
    ('share/jupyter/nbextensions/features_react', [
        'src/datamode/dist/index.js',
    ]),
    # like `jupyter nbextension enable --sys-prefix`
    ('etc/jupyter/nbconfig/notebook.d', [
        'src/datamode/jupyter-config/nbconfig/notebook.d/datamode.json'
    ]),
  ],

  zip_safe=False,

  setup_requires=[
    'jupyter',
  ],

  install_requires=[
    # Utilities
    'pygments',
    'colorama',
    'pytz',
    'python-dateutil',

    # Data manipulation
    'pyparsing',

    # Datastores
    'sqlalchemy',
    'mysql-connector-python==8.0.12',
    'psycopg2-binary',  # Preferred version now instead of 'psycopg2'

    # Machine learning related
    'numpy',
    'scipy',
    'pandas',

    # Dataviz
    'altair',

    ### Notebook
    'jupyter',
    'jupyter-contrib-nbextensions',

    # Core data handling
    'pyarrow',

    # Jupyter-React
    'jupyter-react',
  ],
  keywords=[
    'data science',
    'data transformation',
    'feature engineering',
    'data preparation',
    'data munging',
    'data visualization',
  ],
  classifiers=[
      "Development Status :: 4 - Beta",
      'Programming Language :: Python',
      "Programming Language :: Python :: 3 :: Only",
      "Topic :: Utilities",
      "Topic :: Software Development :: User Interfaces",
      "Topic :: Scientific/Engineering :: Visualization",
      "Topic :: Scientific/Engineering :: Artificial Intelligence",
      "Operating System :: OS Independent",
      "License :: OSI Approved :: Apache Software License",
  ]
)
