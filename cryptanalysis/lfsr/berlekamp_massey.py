def berlekamp_massey(sequence):
    """
    Implements the Berlekamp-Massey algorithm to find the shortest linear feedback shift register (LFSR)
    for a given binary sequence.

    Args:
        sequence (list of int): A binary sequence.

    Returns:
        list of int: The coefficients of the shortest LFSR that generates the given sequence.
    """
    N = len(sequence)
    C = [0] * N
    B = [0] * N
    C[0] = 1
    B[0] = 1
    L = 0
    m = 1
    b = 1

    for n in range(N):
        d = sequence[n]
        for i in range(1, L+1):
            d ^= C[i] & sequence[n-i]

        if d == 0:
            m += 1
        elif 2 * L <= n:
            T = C.copy()
            for i in range(n-m+1):
                C[i+m] ^= d * B[i] // b
            L = n + 1 - L
            B = T
            b = d
            m = 1
        else:
            for i in range(n-m+1):
                C[i+m] ^= d * B[i] // b
            m += 1

    return C[:L+1]
