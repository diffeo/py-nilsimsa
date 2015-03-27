This is a implementation of the nilsimsa algorithm, see http://en.wikipedia.org/wiki/Nilsimsa_Hash

An earlier version of this library was a port to Python of nilsimsa.pl (by way of a ruby port), which was GPLed.  The reimplementation has an explanation of how these hashes work, and is MIT/X11 licensed.

"A nilsimsa code is something like a hash, but unlike hashes, a small change in the message results in a small change in the nilsimsa code. Such a function is called a locality-sensitive hash." Quoted from: http://ixazon.dynip.com/~cmeclax/nilsimsa.html