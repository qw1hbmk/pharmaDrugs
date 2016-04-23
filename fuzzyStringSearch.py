#!/usr/bin/env python
from __future__ import print_function
# This is a straightforward implementation of a well-known algorithm, and thus
# probably shouldn't be covered by copyright to begin with. But in case it is,
# the author (Magnus Lie Hetland) has, to the extent possible under law,
# dedicated all copyright and related and neighboring rights to this software
# to the public domain worldwide, by distributing it under the CC0 license,
# version 1.0. This software is distributed without any warranty. For more
# information, see <http://creativecommons.org/publicdomain/zero/1.0>

vowels = ['a','e','i','o','u','y']
sSound = ['c','s']
zSound = ['z', 's','x']
kSound = ['c','k']
gSound = ['j','g']
fSound = ['p','f']
mSound = ['m','n']


# keyboard_dictionary = 
# {
#   'q':{}, 'w':{}, 'e':{}, 'r':{}, 't':{}. 'y':{}, 'u':{}, 'i':{}, 'o':{}, 'p':{}, '[':{},
#   'a':{}, 's':{}, 'd':{}, 'f':{}, 'g':{}, 'h':{}, 'j':{}, 'k':{}, 'l':{}, ';':{}, 
#   'z':{}, 'x':{}, 'c':{}, 'v':{}, 'b':{}, 'n'{}. 'm':{}, ',':{}
# }

# 'q':[0,0], 'w':[0,1], 'e':[0,2], 'r':[0,3], 't':[0,4], 'y':[0,5], 'u': [0,6], 'i':[0,7], 
# 'a':[1,0.2], 'w'

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


def find_keyboard_distance(letter1, letter2):
  keyboard_coordinate1 = keyboard_dictionary[letter1]
  keyboard_coordinate2 = keyboard_dictionary[letter2]

  x_distance =  abs(keyboard_coordinate1[0] - keyboard_coordinate2[0])
  y_distance = abs(keyboard_coordinate1[1] - keyboard_coordinate2[1])

  if y_distance == 0.0 and x_distance == 0.0:
    return 0.0

  elif y_distance == 0.0 and x_distance <1.1:
    return 0.3

  elif y_distance < 1.1 and x_distance < 1.2:
      return 0.6

  else:
    return 1.0

# Damerau-Levenshtein edit distance implementation
# Based on pseudocode from Wikipedia: https://en.wikipedia.org/wiki/Damerau-Levenshtein_distance

def damerau_levenshtein_distance(a, b):
    # "Infinity" -- greater than maximum possible edit distance
    # Used to prevent transpositions for first characters
    INF = len(a) + len(b)

    # Matrix: (M + 2) x (N + 2)
    matrix  = [[INF for n in xrange(len(b) + 2)]]
    matrix += [[INF] + range(len(b) + 1)]
    matrix += [[INF, m] + [0] * len(b) for m in xrange(1, len(a) + 1)]

    # Holds last row each element was encountered: `DA` in the Wikipedia pseudocode
    last_row = {}

    # Fill in costs
    for row in xrange(1, len(a) + 1):
        # Current character in `a`
        ch_a = a[row-1]

        # Column of last match on this row: `DB` in pseudocode
        last_match_col = 0

        for col in xrange(1, len(b) + 1):
            # Current character in `b`
            ch_b = b[col-1]

            # Last row with matching character; `i1` in pseudocode
            last_matching_row = last_row.get(ch_b, 0)

            # Cost of substitution
            if ch_a == ch_b:
              cost = 0
            else:
              keyboard_cost = find_keyboard_distance(ch_a,ch_b)
              #spelling_cost = find_spelling_distance(ch_a,ch_b)
              cost = min(keyboard_cost,1)

            #cost = 0 if ch_a == ch_b else 1

            # Compute substring distance
            matrix[row+1][col+1] = min(
                matrix[row][col] + cost, # Substitution
                matrix[row+1][col] + 1,  # Addition
                matrix[row][col+1] + 1,  # Deletion
                #this comparison separates the alg from levenshtein
                matrix[last_matching_row][last_match_col] + (row - last_matching_row - 1) + 1
                + (col - last_match_col - 1)) # Transposition


            # If there was a match, update last_match_col
            # Doing this here lets me be rid of the `j1` variable from the original pseudocode
            if cost == 0:
                last_match_col = col

        # Update last row for current character
        last_row[ch_a] = row

    # Return last element
    return matrix[-1][-1]



def levenshtein(a,b):
  "Calculates the Levenshtein distance between a and b."
  n, m = len(a), len(b)
  if n > m:
    # Make sure n <= m, to use O(min(n,m)) space
    a,b = b,a
    n,m = m,n
    
  current = range(n+1)
  for i in range(1,m+1):
    previous, current = current, [i]+[0]*n
    for j in range(1,n+1):
      add, delete = previous[j]+1, current[j-1]+1
      change = previous[j-1]
      if a[j-1] != b[i-1]:
        change = change + 1

      current[j] = min(add, delete, change)
      
  return current[n]


def fuzzyLevenshtein(a,b):
  "Calculates the fuzzy Levenshtein distance between a and b."

  n, m = len(a), len(b)
  if n > m:
    # Make sure n <= m, to use O(min(n,m)) space
    a,b = b,a
    n,m = m,n
    
  current = range(n+1)
  for i in range(1,m+1):
    previous, current = current, [i]+[0]*n
    for j in range(1,n+1):
      add, delete = previous[j]+1, current[j-1]+1
      change = previous[j-1]
      if a[j-1] != b[i-1]:

        if a[j-1] in vowels and b[i-1] in vowels:
          change+=0.2
        elif a[j-1] in sSound and b[i-1] in sSound:
          change+=0.2
        elif a[j-1] in zSound and b[i-1] in zSound:
          change+=0.2
        elif a[j-1] in gSound and b[i-1] in gSound:
          change+=0.2
        elif a[j-1] in kSound and b[i-1] in kSound:
          change+=0.2
        else:
          change = change + 1
          
      current[j] = min(add, delete, change)
      
  return current[n]




def phonetics(a,b):
  "Calculates the phonetic distance between a and b."
  n, m = len(a), len(b)
  if n > m:
    # Make sure n <= m, to use O(min(n,m)) space
    a,b = b,a
    n,m = m,n
    
  current = range(n+1)
  for i in range(1,m+1):
    previous, current = current, [i]+[0]*n
    for j in range(1,n+1):
      add, delete = previous[j]+1, current[j-1]+1
      change = previous[j-1]
      if a[j-1] != b[i-1]:
        if a[j-1] in vowels and b[i-1] in vowels:
          pass
        else:
          change = change + 1
      current[j] = min(add, delete, change)
      
  return current[n]



def fuzzyVowels(a,b):
  #Padding because need to be able to look back at letters
  a = " " + a
  b = " " + b
  vowelScore = 0
  totalScore = 0
  n, m = len(a), len(b)
  if n > m:
    a,b = b, a
    n, m = m, n

  i = 0
  j = 0
  if a[i] != b[j]:
    if a[i] in vowels and b[j] in vowels:
      vowelScore +=1
      totalScore+=1
    else:
      totalScore +=1
  i+=1
  j+=1

  while i < n and j < m:
    #print ("a: ", a[i], "b: ", b[j])
    if a[i] != b[j]:

      #vowel cases

      if a[i] in vowels and b[j] in vowels:
        vowelScore +=1
        totalScore +=1
        #print "a and b", a[i], b[j]
        i+=1
        j+=1
      elif a[i-1] in vowels and b[j] in vowels:
        vowelScore+=1
        totalScore+=1
        #print "not a, just b", a[i], b[j]
        j+=1
      elif a[i] in vowels and b[j-1] in vowels:
        vowelScore+=1
        totalScore+=1
        #print "a, not b", a[i], b[j]
        i+=1


      #consonant cases
      elif a[i] in sSound and b[j] in sSound:
        vowelScore +=1
        totalScore +=1
        #print "a and b", a[i], b[j]
        i+=1
        j+=1
      elif a[i] in kSound and b[j] in kSound:
        vowelScore +=1
        totalScore +=1
        #print "a and b", a[i], b[j]
        i+=1
        j+=1

      elif a[i] in gSound and b[j] in gSound:
        vowelScore +=1
        totalScore +=1
        #print "a and b", a[i], b[j]
        i+=1
        j+=1

      elif a[i] in zSound and b[j] in zSound:
        vowelScore +=1
        totalScore +=1
        #print "a and b", a[i], b[j]
        i+=1
        j+=1        

      elif a[i] in fSound and b[j] in fSound:
        if a[i] == "p" and a[i+1] == "h":
          i+=2
          j+=1
          vowelScore +=1
        elif b[j] == "p" and b[j+1] == "h":
          j+=2
          i+=1
          vowelScore +=1
        else: 
          i+=1
          j+=1
        totalScore +=1

      else:
        totalScore+=1
        i+=1
        j+=1
    else:
      vowelScore+=1
      totalScore+=1
      i+=1
      j+=1

  i, j = n-i, m-j
  #add any remaining letters to total score

  totalScore = totalScore + i + j
  #print ("vowelScore", vowelScore)
  #print ("totalScore", totalScore)

  #removes padding (1)
  return float(vowelScore-1)/(totalScore -1)



def keyboardPosition(a,b):
  pass




if __name__=="__main__":
  from sys import argv
  #print levenshtein(argv[1],argv[2])3
  #print (fuzzyVowels("cipralex","sirpilex"))
  #print (levenshtein("cipralex","sirplex"))
  #print (fuzzyLevenshtein("cipralex","sirplex"))
  print (damerau_levenshtein_distance("fish", "fihs"))
  print (find_keyboard_distance("d","f"))
  #print(fuzzyVowels("tylenol", "tylenal"))



  #print levenshtein(argv[1],argv[2])3
  #print (fuzzyVowels("cipralex","sirpilex"))
  #print (levenshtein("cipralex","sirplex"))
  #print (fuzzyLevenshtein("cipralex","sirplex"))
  #print (damerau_levenshtein_distance("Flexeril", "Flexeral"))
  #print (levenshtein("Fentanyl", "Fentynal"))
  # print (find_keyboard_proximity("d","f"))
  # print (find_phonetic_similarity("a","e"))
  #print(fuzzyVowels("tylenol", "tylenal"))



  # print (damerau_levenshtein_distance("Zenex", "Xanax")) = 0.7
  # print (levenshtein("Zenex", "Xanax")) = 3

  #print (damerau_levenshtein_distance("Vivance", "Vyvanse"))
  #print (levenshtein("Vivance", "Vyvanse"))

misspellings = [
  "Amblefy"
  ,"Adelet" +1
  ,"Backtrin"
  ,"Balsomre"
  ,"Catiprus"
  ,"Cephalexen"
  ,"Darvasit"
  ,"Demeral"
  ,"Effexir"
  ,"Embril" -1
  ,"Fimera" +1
  ,"Phentynil" +1
  ,"Heperin"
  ,"Humera"
  ,"Akluseg" +1
  ,"keppre"
  ,"Genuvia"
  ,"Lavaquin" +0.5
  ,"Lexopro"
  ,"Maxzide"
  ,"Meklazine" +0.5 
  ,"Naproxin"
  ,"Neurotoninin"
  ,"Omaprezil"
  ,"Oxycoton"
  ,"Perkaset"
  ,"Pertzi"
  ,"Relephen"
  ,"Remecade"
  ,"Ciraquil"
  ,"Simcore"
  ,"Tamaflue"
  ,"Tegratol"
  ,"Valium"
  ,"Veremist"
  ,"Warfarin"
  ,"Xanax"
  ,"Zenekal"
  ,"Zocore"
  ,"Zymprexa"]

correct_spellings = [
"ambilify", "adalet", "bactrim", "belsomra", "catapress", "cephalexin", "darvocet", "demerol",
"effexor", "emrel" "femara", "fentanyl", "heparin", "humira", "inclusig", "januvia", "keppra",
"klonopin", "levaquin", "lexapro", "maxzide", "meclizine", "naproxen", "neurontin", "omeprazole",
"oxycontin", "percocet", "pertzye", "relafen", "remicade", "seroquel", "simcor", "tamiflu", 
"tegretol", "valium", "veramyst", "warfarin", "xanax", "xenical", "zocar", "zyprexia"]

sum_fuzzy_misspellings = 0
sum_misspellings = 0
for i in range(len(misspellings)):
  sum_fuzzy_misspellings += fuzzy_damerau_levenshtein_distance(misspellings[i], correct_spellings[i])
  sum_misspellings += levenshtein(misspellings[i], correct_spellings[i])

print ("fuzzy", sum_fuzzy_misspellings/40)
print("nonfuzz", sum_misspellings/40)


typos = [
"ujmping,"
"siz",
"qeuipment",
"sic",
"sippers",
"quick;y",
"wuite",
"waltx",
"gifl",
"Aompyc",
"[ygamas",
"Pheonix"]

original = [
"jumping",
"six",
"equipment",
"six",
"quickly",
"quite",
"waltz",
"girl",
"Zompyc",
"pygamas",
"phoenix"]

sum_fuzzy_misspellings = 0
sum_misspellings = 0
for i in range(len(original)):
  sum_fuzzy_misspellings += fuzzy_damerau_levenshtein_distance(typos[i], original[i])
  sum_misspellings += levenshtein(typos[i], original[i])

print ("fuzzy", sum_fuzzy_misspellings/11)
print("nonfuzz", sum_misspellings/11)