from setuptools import setup

setup(name='pycfslib',
      version='0.9',
      description='Library to read, write amd create CFS file and stream, now supports NEO sleep staging system.',
      url='https://github.com/neurobittechnologies/pycfslib',
      author='Amiya Patanaik',
      author_email='amiya@neurobit.io',
      license='GPL',
      packages=['pycfslib'],
      install_requires=[
          'numpy',
          'skimage',
          'scipy',
          'numba',
      ],
      zip_safe=False)
