from setuptools import setup, find_packages

from pybmrb.csviz import __version__
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pybmrb',
      version=__version__,
      packages = ['pybmrb'],
      author='Kumaran Baskaran',
      author_email='kbaskaran@bmrb.wisc.edu',
      description='PyBMRB provides tools to visualize chemical shift data in BMRB',
      long_description=long_description,
      keywords=['bmrb', 'hsqc', 'chemical shift', 'nmrstar', 'biomagresbank', 'biological magnetic resonance bank'],
      url='https://github.com/uwbmrb/PyBMRB',
      package_data = {'pybmrb':['data/*','examples/*']},
      install_requires = [
            'pynmrstar',
            'plotly',
            'numpy'],
      license='MIT')
