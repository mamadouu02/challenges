import base64
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

def main():
    # Read the public key
    with open("pubkey.pem", "r") as f:
        pubkey = RSA.importKey(f.read())
    n = pubkey.n
    e = pubkey.e

    # Query FactorDB API to factorize the modulus (n)
    res = requests.get("https://factordb.com/api", params={"query": n})
    data = res.json()
    factors = data["factors"]
    p = int(factors[0][0])
    q = int(factors[1][0])

    # Compute the private exponent (d) using the modular inverse of e and phi
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    privkey = RSA.construct((n, e, d, p, q))

    # Decrypt the ciphertext using the private key
    with open("ciphertext.txt", "r") as f:
        ciphertext = base64.b64decode(f.read())
    cipher = PKCS1_v1_5.new(privkey)
    plaintext = cipher.decrypt(ciphertext, None)

    # Write the decrypted plaintext
    with open("plaintext.txt", "w") as f:
        f.write(plaintext.decode())

if __name__ == "__main__":
    main()
