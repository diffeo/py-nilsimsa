"""
Purpose: Set of unit tests for nilsimsa package.

Test data consists of 20 randomly selected documents from a Diffeo corpus.

This software is released under an MIT/X11 open source license.

Copyright 2012-2014 Diffeo, Inc.
"""
import cPickle as pickle
import dircache
import os
import pytest
import random

from deprecated._deprecated_nilsimsa import Nilsimsa as orig_Nilsimsa
from nilsimsa import Nilsimsa, compare_digests


test_data_dir = "test_data/"
sid_to_nil = pickle.load(open("test_data/test_dict.p", "rb"))

def test_nilsimsa():
    """
    tests the nilsimsa hash by choosing a random test file
    computes the nilsimsa digest and compares to the true
    value stored in the pickled sid_to_nil dictionary
    """
    fname = random.choice(dircache.listdir(test_data_dir))
    f = open(os.path.join(test_data_dir, fname), "rb")
    nil = Nilsimsa(f.read())
    f.close()
    assert nil.hexdigest() == sid_to_nil[fname.split(".")[0]]

def test_compare_hex():
    """
    tests compare_digests by computing the nilsimsa score of two documents with a known score
    """
    sid_1 = "1352396387-81c1161097f9f00914e1b152ca4c0f46"
    sid_2 = "1338103128-006193af403dcc90c962184df08960a3"
    assert compare_digests(sid_to_nil[sid_1], sid_to_nil[sid_2]) == 95

def test_compatability():
    """
    testing compat with deprecated version by comparing nilsimsa
    scores of 5 randomly selected documents from the test corpus
    and asserting that both give the same hexdigest
    """
    names = dircache.listdir(test_data_dir)
    fnames = set([random.choice(names) for i in range(5)])
    for fname in fnames:
        f = open(os.path.join(test_data_dir, fname), "rb")
        text = f.read()
        f.close()
        if not(Nilsimsa(text).hexdigest() == orig_Nilsimsa(text).hexdigest()):
            assert False
    assert True

