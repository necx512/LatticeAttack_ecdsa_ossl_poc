# Quick Start
1. Run `make clean` 
2. Run `make` 
3. Generate some (5000 in this exemple) signatures by running: `./generateSignature 5000`.
4. Run `python3 lattice_k`

# Requirements
pip3 install PyCryptodome (Only required for *wNAFpython* directory)

# Nb signatures / nb of known bits
10 bits avec 30 signatures : (30*2**10)/2
9 bits avec 40 signatures 
8 bits avec 40 signatures
7 bits avec 50 signatures
6 bits avec 70 signatures
5 bits avec 110 signatures
4 bits avec 190 signatures : (190*2**(4))/2 mais temps de reduction plus lent


# References
https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Point_multiplication
https://crypto.stackexchange.com/questions/26547/how-can-a-lattice-attack-be-applied-to-ecdsa-signatures
http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=A3522D6371B33FD55DDADD9566D6779C?doi=10.1.1.95.797&rep=rep1&type=pdf [Smart and Howgrave-Graham ]
https://www.di.ens.fr/~pnguyen/pub_NgSh02.htm [Shparlinski and Nguyen.]
https://eprint.iacr.org/2014/161.pdf [“Ooh Aah... Just a Little Bit” : A small amount of side channel can go a long way - Naomi Benger, Joop van de Pol, Nigel P. Smart, and Yuval Yarom]

