from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'smurves',
  packages = ['smurves'],
  version = '1.0.1',
  description = 'The triple-random constrainable curve generator for smooth function perturbation',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  author = 'Ben Moews',
  author_email = 'ben.moews@protonmail.com',
  url = 'https://github.com/moews/smurves',
  keywords = ['astronomy',
              'astrophysics',
              'cosmology',
              'randomized algorithms',
              'function perturbation'],
  classifiers = ['Programming Language :: Python :: 3 :: Only',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License'],
  install_requires = ['numpy'],
)
