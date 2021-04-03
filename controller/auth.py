import os
import binascii
import random
import base64
from Cryptodome.Cipher import AES

modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = b'0CoJUm6Qyw8W8jud'
pubKey = '010001'


# 其中modulus、nonce、pubKey均为已知
# 算法先通过RandomKey生成一个16位的随机字符串作为密钥secKey
# 再将明文text进行两次AES加密获得密文encText
# 因为secKey是在客户端上生成的，所以还需要对其进行RSA加密再传给服务端

def encrypt(text):
    data = str(text).encode("utf-8")
    secKey = RanEncrypt()
    params = AesEncrypt(AesEncrypt(data, nonce), secKey)
    encSecKey = RsaEncrypt(secKey, pubKey, modulus)

    return {"params": params, "encSecKey": encSecKey}


def RanEncrypt():
    secKey = binascii.hexlify(os.urandom(16))[:16]
    return secKey


def AesEncrypt(text, key):
    pad = 16 - len(text) % 16
    text = text + bytearray([pad] * pad)
    encryptor = AES.new(key, 2, b"0102030405060708")
    ciphertext = encryptor.encrypt(text)
    Aesencryptext = base64.b64encode(ciphertext)
    return Aesencryptext


def RsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    ciphertext = pow(int(binascii.hexlify(text), 16), int(pubKey, 16), int(modulus, 16))
    Rsaencrypttext = format(ciphertext, "x").zfill(256)
    return Rsaencrypttext
