#!/usr/bin/python2.7
import sys
import fpylll
from sage.all import *

def readlinectl(f):
    a=f.readline()
    if a=='':
        print("not enough signature")
        sys.exit(-1)
    return a


def build_curve():
    global generator, curve_order, point_Q, hash_used
    p = Integer(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)
    Fp = GF(p)
    E = EllipticCurve(Fp,[0, 0, 0, 0, 7])
    xG=Integer(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798)
    yG=Integer(0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
    generator = E(xG,yG)
    curve_order = generator.order() # 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    point_Q=E(105446788395762283883686341154635018056472261768203060453998927670231275974399 , 45196933497292158243775372590167696637090390309515456771822855521211499639505)
    hash_used = 25868803900419490524558457030329531658547424494090813520878887231621724976998


class LatMat:
  def __init__(self,nbrOfSignatures):
    # 10 bits avec 30 signatures : (30*2**10)/2
    # 9 bits avec 40 signatures 
    # 8 bits avec 40 signatures
    # 7 bits avec 50 signatures
    # 6 bits avec 70 signatures
    # 5 bits avec 110 signatures
    # 4 bits avec 190 signatures : (190*2**(4))/2 mais temps de reduction plus lent
    self.nbrOfSignatures = nbrOfSignatures
    
    self.A = fpylll.IntegerMatrix(self.nbrOfSignatures + 2, self.nbrOfSignatures + 2)
    self.A[self.nbrOfSignatures,self.nbrOfSignatures] = 1
    self.uvec = [0 for i in range(self.nbrOfSignatures+1)]
  
  def addtrace(self,ri,si,hi,ai,li,sig_idx):
      powinv = inverse_mod(2**li,curve_order)
      siinv  = inverse_mod(si,curve_order)
      ui = Integer(mod((ai - hi*siinv)*powinv,curve_order)) + (curve_order // 2**(li+1))
      ti = Integer(mod(ri * powinv * siinv,curve_order))
      self.uvec[sig_idx]=(2**(li+1))*ui
      self.A[sig_idx,sig_idx] = (2**(li+1))*curve_order
      self.A[self.nbrOfSignatures,sig_idx] = (2**(li+1))*ti


  def findkey(self):
      uvectuple = tuple(self.uvec)
  
      #SVP
      for i in range(self.nbrOfSignatures + 1):
        self.A[self.nbrOfSignatures + 1,i] = self.uvec[i]
      self.A[self.nbrOfSignatures + 1,self.nbrOfSignatures + 1] = curve_order
      
      self.uvec.append(curve_order)
      fpylll.BKZ.reduction(self.A,o=fpylll.BKZ.Param(block_size=10))
  
      return Integer(self.A[1,self.nbrOfSignatures]);
    
  

def len_seq(seq):
  li = 0
  for i in seq:
      if i == 'A':
          break
      else:
          li = li + 1
  return li

def read_one_signature(file,wanted_len):
  good_signature = False
  while(good_signature == False):
    readlinectl(f) #nonce
    seq = readlinectl(f)[:-1][::-1]
    ri = int(readlinectl(f),16)
    si = int(readlinectl(f),16)
    li = len_seq(seq) + 1
    ai = 2**(li-1)
    if (li >= wanted_len):
        return  ri,si,li,ai

if __name__ == "__main__":
  build_curve()
  lm = LatMat(60)
  filename="outSigGenk"
  f = open(filename)
  l = []
  j=0
  readsig = 0
  while readsig < 60:
      ri,si,li,ai = read_one_signature(f,7)
      lm.addtrace(ri,si,hash_used,ai,li,readsig)
      readsig = readsig + 1
      if readsig == 60:#lm.cur == 0:
          print("Expected key = "+hex(0x1999999999999999999999999999999948236711c7d7eda9f92ea30e14d239b9))
          print("Found key    = "+hex(lm.findkey()))
          break
