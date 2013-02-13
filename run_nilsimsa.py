# Copyright (C) MetaCarta, Incorporated.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# Port of nilsimsa-20050414.rb from Ruby to Python 
#
# Ported by Michael Itz at MetaCarta
#
# Original comments from Ruby version:
# ---------------------------------------------------------
# Nilsimsa hash (build 20050414)
# Ruby port (C) 2005 Martin Pirker
# released under GNU GPL V2 license
# 
# inspired by Digest::Nilsimsa-0.06 from Perl CPAN and
# the original C nilsimsa-0.2.4 implementation by cmeclax
#  http://ixazon.dynip.com/~cmeclax/nilsimsa.html
# ---------------------------------------------------------
"""
This is a command-line wrapper around the nilsimsa python package.

Computes and compares nilsimsa codes.

A nilsimsa code is something like a hash, but unlike hashes, a small
change in the message results in a small change in the nilsimsa
code. Such a function is called a locality-sensitive hash.

Python port of ruby version that was inspired by a perl version:
   http://ixazon.dynip.com/~cmeclax/nilsimsa.html
"""

# $ Id: $

if __name__ == '__main__':

    import nilsimsa

    import sys
    import os.path
    from optparse import OptionParser
    parser = OptionParser(usage="python nilsimsa.py <list of files to hash> or  --test or --help",
                          description=__doc__)
    parser.add_option("--test", action="callback", callback=nilsimsa.selftest, help="Run a test of this nilsimsa tool.")
    parser.add_option("-c", "--compare", action="store_true", dest="compare", default=False, help="Compare the nilsimsa hash of the first file to each of the subsequent files listed on the command line.")
    parser.add_option("--compare_hexdigests", action="store_true", dest="compare_hexdigests", default=False, help="Compare two hexdigest nilsimsa hashes.")
    parser.add_option("--digest", action="store_true", dest="digest", default=False, help="get a hexdigest nilsimsa hash for the file named on the commandline.")
    (options, args)= parser.parse_args()
    if options.compare_hexdigests:
        print compare_hexdigests( args[0], args[1] )
        sys.exit(0)
    if options.digest:
        print Nilsimsa( data=open( args[0] ).read() ).hexdigest()
        sys.exit(0)    
    first = None
    for filename in args:
        # digest files supplied as arguments
        if os.path.exists(filename):
            nilsimsa = Nilsimsa()
            nilsimsa.from_file(filename)
            distance = ""
            percent_match = ""
            if options.compare:
                if first==None:
                    first = nilsimsa
                else:
                    distance = first.compare( nilsimsa.digest() )
                    percent_match = "%.2f%%" % (100. * (127 + distance) / 255.)
            print "%s\t%s\t%s\t%s" % (nilsimsa.hexdigest(), distance, percent_match, filename)
        else:
            print "error: can't find %s" % filename

