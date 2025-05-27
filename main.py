from collections import namedtuple
import re

Coord = namedtuple("Coord", ["row", "col"])

# Pad taken from newspaper cliping in 'The Discovery'
newspaper_pad = """The whole grain goodness of blue chip dividend stocks has its limits.
Utility stocks, consumer staples, pipelines, telecoms and real estate investment trusts have all lost ground over the past month, even while the broader market has been flat. With the bond market signalling an expectation of rising interest rates, the five-year rally for steady blue-chip dividend payers has stalled.
Should you be scared if you own a lot of these stocks either directly or through mutual funds or exchange-traded funds? David Baskin, president of Baskin Financial Services, has a two-pronged answer: Keep your top-quality dividend stocks, but be prepared to follow his firm's example in trimming holdings in stocks such as TransCanada Corp., Keyera Corp. and Pembina Pipeline Corp."""

# Encrypted message taken from pictograms in 'The Discovery'
#  XX10 00XX  XX11
#      \  |  /           
# 11XX -     - 01XX
#      /  |  \
#  XX01 10XX  XX00
pictogram_binary = (
    "1000 1111 1010 1001 0000 1111 1100 0001 0010 1000 1010 0010 1110 1000 0101 1111 0011 1100 0011 1110 0011 0000 1010 0001 1111 1011"
    "1011 0100 0011 1010 0111 0111 1000 0001 0101 0011 1010 1000 1000 1000 1010 1111 1000 0111 1011 0111 1111 1010"
    "1100 1111 0001 1000 1001 0100 0110 0101 0000 1110 1011 0111 1010 0010 0000 0100 1101 0010 1111 1000 1101 0011 0110"
    "0001 0101 1111 1110 1011 0010 0001 0000 1110 0100 0100 1100 0001 0100 1011 1101 0100 0010 0000 1100 1011 1101 0100"
    "0011 0011 0001 0010 1111 0010 1011 1001 1100 0110 0011 0110 1010 0000 0011 0111 1101 0000 0100 0101 1001 0011 1011 0010"
    "1000 0111 0010 1110 1100 1101 1011 1111 1000 0010 0110 1111 1100 0000 1100 0110 1100 0111 0011 0001 0011 0011"
    "1011 1010 0010 1100 1000 0011 1010 1011 1110 1011 0010 0010 1101 1000 1011 0111 1100 0010"
    ).replace(" ", "")

polybius_square = [
    ['F', 'G', 'H', 'I', 'J', 'K'],
    ['E', 'X', 'Y', 'Z', '0', 'L'],
    ['D', 'W', '7', '8', '1', 'M'],
    ['C', 'V', '6', '9', '2', 'N'],
    ['B', 'U', '5', '4', '3', 'O'],
    ['A', 'T', 'S', 'R', 'Q', 'P']
]

def generate_pad_binary(newspaper_pad: str) -> str:
    # the chars to represent as 1 in binary output
    vowels = "aiueoy"
    # sanitise the input (lowercase & no special chars)
    newspaper_pad = re.sub(r"[^a-z0-9]", "", newspaper_pad.lower())
    result = ""
    for char in newspaper_pad:
        if char in vowels:
            result += "1"
        else:
            result += "0"
    return result

def xor(a: str, b: str) -> str:
    """
        XOR two binary strings of equal length.

        Args:
            a (str): First binary string.
            b (str): Second binary string.

        Returns:
            str: XOR result as a binary string.
    """
    result = ""
    for x, y in zip(a, b):
        if x != y:
            result += "1"
        else:
            result += "0"
    return result

def bin_to_polybius_square_coords(encrypted_binary: str) -> list[Coord]:
    # split into three digit binary co-ordinates
    coords = []
    for i in range(0, len(encrypted_binary), 6):
        chunk = encrypted_binary[i:i+6]
        if len(chunk) < 6:
            continue
        row = int(chunk[:3], 2)
        col = int(chunk[3:], 2)
        coords.append(Coord(row, col))
    return coords

def polybius_square_decrypt(coordinates: list[Coord]) -> str:
    decrypted_text = ""
    for coordinate in coordinates:
        if coordinate.row > 5 or coordinate.col > 5:
            break
        decrypted_text += polybius_square[coordinate.row][coordinate.col]
    return decrypted_text

# 1 - generate binary newspaper_pad
pad_binary = generate_pad_binary(newspaper_pad)

# 2 - XOR encryped message with binary newspaper_pad
decrypted_msg_bin = xor(pictogram_binary, pad_binary)

# 3 - run XOR binary through polybius square
polybius_square_coordinates = bin_to_polybius_square_coords(decrypted_msg_bin)
decrypted_text = polybius_square_decrypt(polybius_square_coordinates)
print(decrypted_text)