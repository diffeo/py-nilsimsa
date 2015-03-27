#$Id$

from setuptools import setup

from version import get_git_version
VERSION, SOURCE_HASH = get_git_version()

setup(name='nilsimsa',
      version=VERSION,
      description="Locality-sensitive hashing",
      long_description="""\
Python port of nilsimsa.  "A nilsimsa code is something like a hash, but unlike hashes, a small change in the message results in a small change in the nilsimsa code. Such a function is called a locality-sensitive hash."  http://ixazon.dynip.com/~cmeclax/nilsimsa.html.""",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Text Processing :: Indexing",
        "License :: OSI Approved :: MIT License",
        ],
      keywords='python, nilsimsa, hash, locality-sensitive, duplicate detection',
      author='Nithin Tumma',
      maintainer='nithintumma',
      author_email='nithintumma gmail',
      url='https://github.com/diffeo/py-nilsimsa/',
      license="X/MIT http://opensource.org/licenses/MIT",
      zip_safe=False,
      install_requires=[],
      entry_points="""
      # -*- Entry points: -*-
      """,
      packages=['nilsimsa'],
      package_data = {"nilsimsa": ["test_data/*.txt", "test_data/*.p"]}
      )
