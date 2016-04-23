#!/usr/bin/env python3
#from __future__ import print_function


A = 'a'
E = 'e'
O = 'o'
I = 'i'
Y = 'y'
U = 'u'
C = 'c'
S = 's'
Z = 'z'
X = 'x'
K = 'k'
G = 'g'
J = 'j'
M = 'm'
N = 'n'
P = 'p'
B = 'b'
#Vowels and consonants membership Values
phonetic_similarity_dict = {
	A:{A:1.0, E:0.8, I:0.8, O:0.8, U:0.8},
	E:{E:1.0, A:0.8, I:0.8, O:0.8, U:0.8},
	I:{I:1.0, A:0.8, E:0.8, O:0.8, U:0.8, Y:0.8},
  O:{O:1.0, A:0.8, E:0.8, I:0.8, U:0.8, Y:0.8},
  U:{U:1.0, A:0.8, E:0.8, O:0.8, I:0.8, Y:0.8},
	Y:{Y:1.0, I:0.8, E:0.8}, 
	C:{C:1.0, K:0.7, S:0.7},
	S:{S:1.0, C:0.7, Z:0.7},
	Z:{Z:1.0, S:0.7, X:0.7},
  X:{X:1.0, S:0.7, Z:0.7},
	K:{K:1.0, C:0.7},
	G:{G:1.0, J:0.7},
	J:{J:1.0, G:0.7},
	M:{M:1.0, N:0.7},
	N:{N:1.0, M:0.7},
	P:{P:1.0, B:0.7},
	B:{B:1.0, P:0.7}
}

first_keyboard_row = 'qwertyuiop[]'
second_keyboard_row = 'asdfghjkl;"'
third_keyboard_row =  'zxcvbnm,.'

keyboard_dictionary = {}


for i, letter in enumerate(first_keyboard_row):
  keyboard_dictionary[letter] = (i + 0.0,0.0)

for i, letter in enumerate(second_keyboard_row):
  keyboard_dictionary[letter] = (i+0.2,1.0)

for i, letter in enumerate(third_keyboard_row):
  keyboard_dictionary[letter] = (i+0.7,2.0)


def find_keyboard_proximity(letter1, letter2):
  if letter1 in keyboard_dictionary and letter2 in keyboard_dictionary:
    keyboard_coordinate1 = keyboard_dictionary[letter1]
    keyboard_coordinate2 = keyboard_dictionary[letter2]

    x_distance =  abs(keyboard_coordinate1[0] - keyboard_coordinate2[0])
    y_distance = abs(keyboard_coordinate1[1] - keyboard_coordinate2[1])

    if y_distance == 0.0 and x_distance == 0.0:
      return 1.0

    elif y_distance == 0.0 and x_distance <1.1:
      return 0.7

    elif y_distance < 1.1 and x_distance < 1.2:
        return 0.4

    else:
      return 0

  else:
    return 0

def find_phonetic_similarity(letter1, letter2):
 	if letter1 in phonetic_similarity_dict:
 		if letter2 in phonetic_similarity_dict[letter1]:
 			return phonetic_similarity_dict[letter1][letter2]

 	return 0.0


# Damerau-Levenshtein edit distance implementation modified from James Jensen's implementation (https://gist.github.com/badocelot/5327337)
def fuzzyLevenshtein(a, b):
    # "Infinity" -- greater than maximum possible edit distance
    # Used to prevent transpositions for first characters
    a = a.lower()
    b = b.lower()

    INF = len(a) + len(b)

    # Matrix: (M + 2) x (N + 2)
    matrix  = [[INF for n in range(len(b) + 2)]]
    matrix += [[INF] + list(range(len(b) + 1))]
    matrix += [[INF, m] + [0] * len(b) for m in range(1, len(a) + 1)]

    # Holds last row each element was encountered: `DA` in the Wikipedia pseudocode
    last_row = {}

    # Fill in costs
    for row in range(1, len(a) + 1):
        # Current character in `a`
        ch_a = a[row-1]

        # Column of last match on this row: `DB` in pseudocode
        last_match_col = 0

        for col in range(1, len(b) + 1):
            # Current character in `b`
            ch_b = b[col-1]

            # Last row with matching character; `i1` in pseudocode
            last_matching_row = last_row.get(ch_b, 0)

            # Cost of substitution
            if ch_a == ch_b:
              cost = 0
            else:
              keyboard_cost = 1 - find_keyboard_proximity(ch_a,ch_b)
              phonetic_similariy = 1 - find_phonetic_similarity(ch_a,ch_b)

              #spelling_cost = find_spelling_distance(ch_a,ch_b)
              cost = min(keyboard_cost,phonetic_similariy)

            #cost = 0 if ch_a == ch_b else 1

            # Compute substring distance
            matrix[row+1][col+1] = min(
                matrix[row][col] + cost, # Substitution
                matrix[row+1][col] + 1,  # Addition
                matrix[row][col+1] + 1,  # Deletion
                #this comparison separates the alg from levenshtein
                matrix[last_matching_row][last_match_col] + (row - last_matching_row - 1) + 0.4
                + (col - last_match_col - 1)) # Transposition


            # If there was a match, update last_match_col
            # Doing this here lets me be rid of the `j1` variable from the original pseudocode
            if cost == 0:
                last_match_col = col

        # Update last row for current character
        last_row[ch_a] = row

    # Return last element
    return float(matrix[-1][-1])


# Levenshtein edit distance implementation modified from James Jensen's implementation (https://gist.github.com/badocelot/5327337)
def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    # "Infinity" -- greater than maximum possible edit distance
    # Used to prevent transpositions for first characters
    a = a.lower()
    b = b.lower()

    INF = len(a) + len(b)

    # Matrix: (M + 2) x (N + 2)
    matrix  = [[INF for n in range(len(b) + 2)]]
    matrix += [[INF] + list(range(len(b) + 1))]
    matrix += [[INF, m] + [0] * len(b) for m in range(1, len(a) + 1)]

    # Holds last row each element was encountered: `DA` in the Wikipedia pseudocode
    last_row = {}

    # Fill in costs
    for row in range(1, len(a) + 1):
        # Current character in `a`
        ch_a = a[row-1]

        # Column of last match on this row: `DB` in pseudocode
        last_match_col = 0

        for col in range(1, len(b) + 1):
            # Current character in `b`
            ch_b = b[col-1]

            # Last row with matching character; `i1` in pseudocode
            last_matching_row = last_row.get(ch_b, 0)

            # Cost of substitution
            if ch_a == ch_b:
              cost = 0
            else:
              cost = 1

            #cost = 0 if ch_a == ch_b else 1

            # Compute substring distance
            matrix[row+1][col+1] = min(
                matrix[row][col] + cost, # Substitution
                matrix[row+1][col] + 1,  # Addition
                matrix[row][col+1] + 1)  # Deletion

            # If there was a match, update last_match_col
            # Doing this here lets me be rid of the `j1` variable from the original pseudocode
            if cost == 0:
                last_match_col = col

        # Update last row for current character
        last_row[ch_a] = row

    # Return last element
    return float(matrix[-1][-1])

if __name__=="__main__":
  from sys import argv
  print("all okay")
