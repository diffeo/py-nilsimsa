#$Id:$

from setuptools import setup

version = '0.1'

setup(name='nilsimsa',
      version=version,
      description="Locality-sensitive hashing",
      long_description="""\
Python port of nilsimsa.  "A nilsimsa code is something like a hash, but unlike hashes, a small change in the message results in a small change in the nilsimsa code. Such a function is called a locality-sensitive hash."  http://ixazon.dynip.com/~cmeclax/nilsimsa.html.""",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Text Processing :: Indexing",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        ],
      keywords='python, nilsimsa, hash, locality-sensitive, duplicate detection',
      author='',
      author_email='',
      url='http://code.google.com/p/py-nilsimsa/',
      license="GPL",
      zip_safe=False,
      install_requires=[],
      entry_points="""
      # -*- Entry points: -*-
      """,
      scripts=['nilsimsa.py'],
      )
