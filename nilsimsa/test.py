"""
Purpose: Set of unit tests for nilsimsa package.

Test data consists of 20 randomly selected documents from a Diffeo corpus.

This software is released under an MIT/X11 open source license.

Copyright 2012-2015 Diffeo, Inc.
"""
from __future__ import absolute_import, division
try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    from dircache import listdir
except ImportError:
    from os import listdir   # dircache gone in Python 3
import os
import pytest
import random
import time

from nilsimsa.deprecated._deprecated_nilsimsa import Nilsimsa as orig_Nilsimsa
from nilsimsa import Nilsimsa, compare_digests, convert_hex_to_ints

test_data_dir = os.path.join(os.path.dirname(__file__), "test_data/")
test_data = "test_dict.p"
test_dict = os.path.join(test_data_dir, test_data)
sid_to_nil = pickle.load(open(test_dict, "rb"))

def test_nilsimsa():
    """
    tests the nilsimsa hash by choosing a random test file
    computes the nilsimsa digest and compares to the true
    value stored in the pickled sid_to_nil dictionary
    """
    fname = random.choice(listdir(test_data_dir))
    f = open(os.path.join(test_data_dir, fname), "rb")
    nil = Nilsimsa(f.read())
    f.close()
    assert nil.hexdigest() == sid_to_nil[fname.split(".")[0]]

def test_nilsimsa_speed():
    """
    computes nilsimsa hash for all test files and prints speed
    """
    corpus = []
    for fname in listdir(test_data_dir):
        f = open(os.path.join(test_data_dir, fname), "rb")
        corpus.append(f.read())
        f.close()
    start = time.time()
    for text in corpus:
        Nilsimsa(text)
    elapsed = time.time() - start
    print("%d in %f --> %f per second" % (
        len(corpus), elapsed, len(corpus)/elapsed))

def test_unicode():
    """
    ensures that feeding unicode to Nilsimsa behaves gracefully
    """
    nil = Nilsimsa(u'\u1F631')
    assert nil.hexdigest()

def test_compare_hex():
    """
    tests compare_digests by computing the nilsimsa score of two documents with a known score
    """
    sid_1 = "1352396387-81c1161097f9f00914e1b152ca4c0f46"
    sid_2 = "1338103128-006193af403dcc90c962184df08960a3"
    assert compare_digests(sid_to_nil[sid_1], sid_to_nil[sid_2]) == 95

def test_compare_threshold():
    """
    tests compare_digests by computing the nilsimsa score of two
    documents with a known score and the threshold set well above that
    score, so that it bails out early
    """
    sid_1 = "1352396387-81c1161097f9f00914e1b152ca4c0f46"
    sid_2 = "1338103128-006193af403dcc90c962184df08960a3"
    threshold = 110
    score = compare_digests(sid_to_nil[sid_1], sid_to_nil[sid_2], threshold=threshold)
    assert score == threshold - 1

def test_compare_threshold_hex():
    """
    tests compare_digests by computing the nilsimsa score of two
    documents with a known score and the threshold set well above that
    score, so that it bails out early
    """
    sid_1 = "1352396387-81c1161097f9f00914e1b152ca4c0f46"
    sid_2 = "1338103128-006193af403dcc90c962184df08960a3"
    threshold = 110
    digest_1 = convert_hex_to_ints(sid_to_nil[sid_1])
    digest_2 = convert_hex_to_ints(sid_to_nil[sid_2])
    score = compare_digests(digest_1, digest_2, is_hex_1=False, is_hex_2=False,threshold=threshold)
    assert score == threshold - 1

def test_compatability():
    """
    testing compat with deprecated version by comparing nilsimsa
    scores of 5 randomly selected documents from the test corpus
    and asserting that both give the same hexdigest
    """
    names = listdir(test_data_dir)
    fnames = set([random.choice(names) for i in range(5)])
    for fname in fnames:
        f = open(os.path.join(test_data_dir, fname), "rb")
        text = f.read()
        f.close()
        if not(Nilsimsa(text).hexdigest() == orig_Nilsimsa(text).hexdigest()):
            assert False
    assert True
