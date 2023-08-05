from setuptools import setup

setup(name='transitleastsquares',
      version='1.0',
      description='An optimized transit-fitting algorithm to search for periodic transits of small planets',
      url='https://github.com/hippke/tls',
      author='Michael Hippke',
      author_email='michael@hippke.org',
      license='MIT',
      packages=['transitleastsquares'],
      include_package_data=True,
      package_data={
      '': ['*.csv']
      },
      install_requires=[
          'numpy',
          'scipy',
          'numba',
          'tqdm',
          'batman-package',
          'argparse'
      ]
)