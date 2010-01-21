from setuptools import find_packages, setup

setup(name='solvertools',
      version='2010.1', # When we "release", it will of course be 2011.0
      description='Manic Sages Solver Tools',
      packages=find_packages(),
      package_data={
        # Unfortunately, you have to update this if you add a new kind of data
        '': ['data/dict/*.txt', 'data/pickle/*.pickle', 'data/answers/*.dat']
      },
      zip_safe=False,   # dear Setuptools, please don't fuck with my files
     )

