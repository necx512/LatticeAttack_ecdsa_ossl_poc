OPENSSLPATH=openssl-1.0.1e
all:
	tar xf openssl-1.0.1e_modified.tgz
	cd openssl-1.0.1e/ ; ./config ; make
	gcc -Wall -o testECDSAk testECDSAk.c ${OPENSSLPATH}/libcrypto.a -ldl -I${OPENSSLPATH}/include
clean:
	rm -rf openssl-1.0.1e outSigGenk
	rm -f testECDSAk
