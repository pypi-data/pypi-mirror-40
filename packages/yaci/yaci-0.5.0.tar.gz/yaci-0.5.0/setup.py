from setuptools import find_packages
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='yaci',
      version='0.5.0',
      description='Yet Another Cache Implementation',
      author='Aquil H. Abdullah',
      author_email='aquil.abdullah@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      install_requires=['six'],
      extra_requires={
          'test': ['six', 'pytest', 'pytest-cov', 'tox', 'mock'],
          'all': ['six', 'jupyter', 'pytest', 'pytest-cov', 'tox', 'mock']
      },
      classifiers=['Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7'
                  ],
      )
