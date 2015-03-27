# -*- coding: utf-8 -*-
# Author: Douglas Creager <dcreager@dcreager.net>
# This file is placed into the public domain.
 
# Calculates the current version number.  If possible, this is the
# output of “git describe”, modified to conform to the versioning
# scheme that setuptools uses.  If “git describe” returns an error
# (most likely because we're in an unpacked copy of a release tarball,
# rather than in a git working copy), then we fall back on reading the
# contents of the RELEASE-VERSION file.
#
# To use this script, simply import it your setup.py file, and use the
# results of get_git_version() as your package version:
#
# from version import get_git_version
#
# setup(
#     version=get_git_version()[0],
#     .
#     .
#     .
# )
#
# This will automatically update the RELEASE-VERSION file, if
# necessary.  Note that the RELEASE-VERSION file should *not* be
# checked into git; please add it to your top-level .gitignore file.
#
# You'll probably want to distribute the RELEASE-VERSION file in your
# sdist tarballs; to do this, just create a MANIFEST.in file that
# contains the following line:
#
#   include RELEASE-VERSION
 
__all__ = ("get_git_version")

import os
import sys
import traceback
from subprocess import Popen, PIPE
 
 
def call_git_describe(abbrev=4):
    dot_git = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '.git')
    if not os.path.exists(dot_git):
        return None, None

    line = None
    p = None
    try:
        p = Popen(['git', 'describe', '--abbrev=%d' % abbrev],
                  stdout=PIPE, stderr=PIPE, 
                  cwd=os.path.dirname(os.path.abspath(__file__)))
        p.stderr.close()
        describe_line = p.stdout.readlines()[0].strip()

        p = Popen(['git', 'rev-parse', 'HEAD'],
                  stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        source_hash = p.stdout.readlines()[0].strip()
        source_hash = source_hash[:abbrev]

        parts = describe_line.split('-')
        if len(parts) == 1:
            version = parts[0]

        else:
            ver, rel, source_hash = parts
            version_parts = ver.split('.')
            lasti = len(version_parts) - 1
            # increment whatever the last part of this a.b.c.d.yadda
            version_parts[lasti] = str(int(version_parts[lasti]) + 1)
            version = '{}.dev{}'.format('.'.join(version_parts), rel)

        return version, source_hash
 
    except Exception, exc:
        sys.stderr.write('line: %r\n' % line)
        sys.stderr.write(traceback.format_exc(exc))
        try:
            sys.stderr.write('p.stderr.read()=%s\n' % p.stderr.read())
        except Exception, exc:
            sys.stderr.write(traceback.format_exc(exc))
        try:
            sys.stderr.write('os.getcwd()=%s\n' % os.getcwd())
        except Exception, exc:
            sys.stderr.write(traceback.format_exc(exc))
        return None, None
 
 
def read_release_version():
    try:
        f = open("RELEASE-VERSION", "r")
 
        try:
            version = f.readlines()[0]
            return version.strip().split(',')
 
        finally:
            f.close()
 
    except:
        return None, None
 
 
def write_release_version(version, source_hash):
    f = open("RELEASE-VERSION", "w")
    f.write("%s,%s\n" % (version, source_hash))
    f.close()
 
 
def get_git_version(abbrev=4):
    # Read in the version that's currently in RELEASE-VERSION.
 
    release_version, release_source_hash = read_release_version()
 
    # First try to get the current version using “git describe”.
 
    version, source_hash = call_git_describe(abbrev)
 
    # If that doesn't work, fall back on the value that's in
    # RELEASE-VERSION.
 
    if version is None:
        version = release_version
        source_hash = release_source_hash
 
    # If we still don't have anything, that's an error.
 
    if version is None:
        # raise ValueError("Cannot find the version number!")
        version = '0.0.0'
        source_hash = ''
 
    # If the current version is different from what's in the
    # RELEASE-VERSION file, update the file to be current.
 
    if version != release_version or source_hash != release_source_hash:
        write_release_version(version, source_hash)
 
    # Finally, return the current version.
 
    return version, source_hash
 
 
if __name__ == "__main__":
    print get_git_version()
