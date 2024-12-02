from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

s = 182696500728840230479621823519185310839242538506102680518855385654604107284272021239477382873087372363666649671206904122209453086593819518986849024681589583

# Create the private key using SECP521r1 curve from the integer s
private_key = ec.derive_private_key(s, ec.SECP521R1())

# Save the private key to a PEM file
with open("private.pem", "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

print("Private key saved to private.pem")