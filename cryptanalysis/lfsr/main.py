from berlekamp_massey import berlekamp_massey

class LFSR:
    def __init__(self, initial_state, cpoly):
        self.n = len(cpoly) - 1
        self.state = initial_state[:self.n]
        self.cpoly = cpoly

    def next(self):
        byte = 0
        for _ in range(8):
            byte = (byte << 1) | self.state[0]
            next_bit = 0
            for i in range(1, self.n+1):
                next_bit += self.state[self.n-i] * self.cpoly[i]
            next_bit %= 2
            self.state = self.state[1:] + [next_bit]
        return byte

def xor_bytes(byte_seq1, byte_seq2):
    return [b1 ^ b2 for b1, b2 in zip(byte_seq1, byte_seq2)]

def bytes_to_bits(byte_seq):
    return [int(bit) for byte in byte_seq for bit in format(byte, '08b')]

def main():
    png_header = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

    # Read the first 8 bytes of the encrypted file to get the encrypted header
    with open('challenge.png.encrypt', 'rb') as f:
        encrypted_header = f.read(8)

    # Compute the initial state of the LFSR by XORing the PNG header with the encrypted header
    initial_state = bytes_to_bits(xor_bytes(png_header, encrypted_header))

    # Find the connection polynomial of the LFSR using the Berlekamp-Massey algorithm
    cpoly = berlekamp_massey(initial_state)

    # Initialize the LFSR with the initial state and connection polynomial
    lfsr = LFSR(initial_state, cpoly)

    # Decrypt the encrypted file and write the decrypted bytes to a new file
    with open('challenge.png.encrypt', 'rb') as encrypted_file:
        with open('challenge.png', 'wb') as decrypted_file:
            for byte in encrypted_file.read():
                decrypted_file.write(bytes([byte ^ lfsr.next()]))

if __name__ == "__main__":
    main()
