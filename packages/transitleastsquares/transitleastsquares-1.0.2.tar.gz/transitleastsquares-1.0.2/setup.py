from setuptools import setup

setup(name='transitleastsquares',
      version='1.0.2',
      description='An optimized transit-fitting algorithm to search for periodic transits of small planets',
      long_description='An optimized transit-fitting algorithm to search for periodic transits of small planets. We present a new method to detect planetary transits from time-series photometry, the Transit Least Squares (TLS) algorithm. While the commonly used Box Least Squares (BLS, Kovács et al. 2002) algorithm searches for rectangular signals in stellar light curves, TLS searches for transit-like features with stellar limb-darkening and including the effects of planetary ingress and egress. Moreover, TLS analyses the entire, unbinned data of the phase-folded light curve. These improvements yield a ~10 % higher detection efficiency (and similar false alarm rates) compared to BLS. The higher detection efficiency of our freely available Python implementation comes at the cost of higher computational load, which we partly compensate by applying an optimized period sampling and transit duration sampling, constrained to the physically plausible range. A typical Kepler K2 light curve, worth of 90 d of observations at a cadence of 30 min, can be searched with TLS in 10 seconds real time on a standard laptop computer, just as with BLS.',
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