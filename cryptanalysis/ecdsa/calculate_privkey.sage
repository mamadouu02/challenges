import base64
import binascii
from hashlib import sha256
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

# Elliptic Curve Parameters for secp521r1
p = 0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
K = GF(p)
a = K(0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc)
b = K(0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00)
E = EllipticCurve(K, (a, b))
G = E(0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66,
      0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650)
E.set_order(0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409 * 0x1)

# Function to extract x and y from the DSS signature
def extract_signature_components(signature_base64):
    """Decode the base64-encoded signature and extract the x and y components."""
    signature_bytes = base64.b64decode(signature_base64)
    x, y = decode_dss_signature(signature_bytes)
    return x, y

# Function to read message and signature from file
def read_message_and_signature(file_path):
    """Read the message and signature from a file."""
    with open(file_path, "r") as f:
        lines = f.readlines()
    return lines[0].strip(), lines[1].strip()

# Function to calculate k based on the hash and y differences
def calculate_k(hash_diff, y_diff, order):
    """Calculate nonce k using hash and y differences."""
    return (hash_diff * pow(y_diff, -1, order)) % order

# Function to calculate private key s
def calculate_private_key_s(y, k, hash_m, x, order):
    """Calculate private key s using y, k, hash of the message, and x."""
    return ((y * k - hash_m) * pow(x, -1, order)) % order

# Processing function for files to check redundancy
def process_files(num_files, order):
    """Process multiple files to find redundancy and calculate k and s if possible."""
    x_values = {}

    for i in range(1, num_files + 1):
        message_file = f"messages/m{i}"
        
        try:
            # Extract message and signature
            message, signature_base64 = read_message_and_signature(message_file)
            x, y = extract_signature_components(signature_base64)
            
            if x in x_values:
                print(f"Redundancy found! Value of x: {hex(x)} used in messages {x_values[x][0]} and {i}.")
                return x_values[x][0], i, x, (x_values[x][1], y)
            else:
                x_values[x] = (i, y)
        
        except FileNotFoundError:
            print(f"Error: File {message_file} not found.")
        except Exception as e:
            print(f"Error processing file {message_file}: {e}")

    return None, None, None, None

def main():
    order = E.order()
    
    # Process files to check for redundancy
    msg_index_1, msg_index_2, x, y_values = process_files(30, order)
    
    if x:
        message_1, signature_base64_1 = read_message_and_signature(f"messages/m{msg_index_1}")
        message_2, signature_base64_2 = read_message_and_signature(f"messages/m{msg_index_2}")
        
        hash_m1 = int(sha256(message_1.encode()).hexdigest(), 16)
        hash_m2 = int(sha256(message_2.encode()).hexdigest(), 16)

        # Calculate k
        h_diff = (hash_m1 - hash_m2) % order
        y_diff = (y_values[0] - y_values[1]) % order
        k = calculate_k(h_diff, y_diff, order)
        print(f"Calculated k: {k}")

        # Calculate private key s
        s = calculate_private_key_s(y_values[0], k, hash_m1, x, order)
        print(f"Calculated private key s: {s}")
    else:
        print("No redundancy found; cannot exploit nonce reuse.")

if __name__ == "__main__":
    main()
