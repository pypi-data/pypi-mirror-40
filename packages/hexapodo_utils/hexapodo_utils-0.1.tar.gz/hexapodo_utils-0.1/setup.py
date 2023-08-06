from setuptools import setup

setup(name='hexapodo_utils',
      version='0.1',
      description="Hexapodo's functions",
      url='https://github.com/datankai/hexapodo-utils',
      author='juandatank',
      author_email='juan@datank.ai',
      license='MIT',
      packages=['hexapodo_utils', 'text_utils'],
      install_requires=[
          'smart_open',
          'stringdist',
          'numpy',
          'pandas',
          'networkx',
          'dask',
          'jellyfish',
          'toolz',
          'cloudpickle'
      ],
      zip_safe=True)
    
