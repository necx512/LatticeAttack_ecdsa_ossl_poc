// https://en.bitcoin.it/wiki/Secp256k1
#include <openssl/pem.h>
#include <openssl/evp.h>
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <string.h>

#define Hash "25868803900419490524558457030329531658547424494090813520878887231621724976998"

#include "privatek.hpp"

void
printBN (const BIGNUM * a)
{
  fflush (stdout);
  BIO *out = BIO_new_fd (fileno (stdout), BIO_NOCLOSE);
  BN_print (out, a);
  printf ("\n");
  BIO_free (out);
}

int
main ()
{
  BIGNUM *hashBN = NULL;	//=BN_new();
  BN_dec2bn (&hashBN, Hash);

  char hash[500];
  memset (hash, '\0', 500);
  BN_bn2bin (hashBN, (unsigned char *) hash);

  EC_KEY *ecprivkey = EC_KEY_new_by_curve_name (NID_secp256k1);
  if (ecprivkey == NULL)
    {
      fprintf (stderr, "can't read key\n");
      exit (EXIT_FAILURE);
    }
  if (EC_KEY_generate_key (ecprivkey) == 0)
    {
      fprintf (stderr, "can't generate key\n");
      exit (EXIT_FAILURE);
    }
  BIGNUM *priv = BN_new ();
  BN_hex2bn (&priv, PRIVATE);
  EC_KEY_set_private_key (ecprivkey, priv);
  printf ("\n");
  ECDSA_SIG *err =
  ECDSA_do_sign ((unsigned char *) hash, strlen (hash), ecprivkey);
  printf ("\n");
  if (err == NULL)
    {
      unsigned long iterr = ERR_get_error ();
      fprintf (stderr, "fail to sign\n%s\n", ERR_error_string (iterr, NULL));
      exit (EXIT_FAILURE);
    }
  printBN (err->r);
  printBN (err->s);

}
