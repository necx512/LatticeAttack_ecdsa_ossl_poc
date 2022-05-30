from Crypto.PublicKey import ECC
import random

def bezout_fct(a,b):
    if b == 0:
        return 1,0
    else:
        u , v = bezout_fct(b , a % b)
        return v , u - (a//b)*v
def compute_inverse(a,p):
    c = bezout_fct(a,p)
    inverse = c[0]
    if( inverse < 0):
        inverse = inverse + p
    return inverse

# Curve prime256v1 256-bit prime field Weierstrass curve. 
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
G_x = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
G_y = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
h = 0x1
generator = ECC.EccPoint(G_x,G_y,'prime256v1')
zero = generator.point_at_infinity()
private_key = 0x8d0fffad90de5b3fa0aead7efdd10c551bc2e90082ed155c645f1c6a00c42753
publickey = private_key*generator
Hash = 25868803900419490524558457030329531658547424494090813520878887231621724976998
width = 3
# https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Point_multiplication
# https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication

last =  2**(width-1) - 1
power_minusone = 2**(width-1)
power = 2**(width)

def pre_compute(point,w):
    dic = {}
    for i in range(1,last+1,2):
        dic[i] = i*point
        dic[-i] = ECC.EccPoint( int(dic[i].x) ,p - int(dic[i].y),'prime256v1') # inverse
        if(dic[i] + dic[-i] != zero):
            print("===============> FAILED");
            exit(-1)
    return dic

dic = pre_compute(generator,width)

def mods(a,w):
    dmodpower = a%power
    if( dmodpower >= power_minusone):
        return dmodpower - power
    else:
        return dmodpower

def wnaf_representation(k,w):
    ki = []
    while(k > 0):
        if((k%2) == 1):
            tki = mods(k,w)
            k = k - tki
        else:
            tki = 0
        ki.append(tki)
        k = k//2
    ki.reverse()
    return ki

def wnaf_mul(k,point,w,zero):
    Q = zero
    #dic = pre_compute(point,w)
    ki = wnaf_representation(k,w)
    m = len(ki)
    seq=""
    for j in range(m):
        seq=seq+"D"
        Q = 2*Q
        if(ki[j] != 0):
            seq=seq+"A"
            Q = Q + dic[ki[j]]
    return Q,seq







#nonce = 0x1F68FA89723F87EAF361544D81372188CC2E6326E9C097C702F066C275B8DC3BC - n
#nonce_inverse = compute_inverse(nonce, n)
#kG,seq = wnaf_mul(nonce,generator,3,zero)
#r = int(kG.x)
#s = (nonce_inverse*(Hash + private_key*r))%n;
#print(hex(r))
#print(hex(s))
for i in range(10000): # 1/2**7 => il faut 2**7 signatures en moyenne pour avoir une bonne signature. Puisqu'on veut 60 signatures, il faut 60*2**7 = 
  while(True):
    nonce = random.randrange(1,n)
    nonce_inverse = compute_inverse(nonce, n)
    kG,seq = wnaf_mul(nonce,generator,3,zero)
    r = int(kG.x)
    if(r == 0):
        continue
    s = (nonce_inverse*(Hash + private_key*r))%n;
    if(s == 0):
        continue
    print(hex(nonce).upper()[2:])
    print(seq)
    print(hex(r).upper()[2:])
    print(hex(s).upper()[2:])
    break
  
