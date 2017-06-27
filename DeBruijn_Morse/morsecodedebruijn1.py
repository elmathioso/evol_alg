#------------------------------------
#       Morse Code Optimizer        -
#       Mathieu Lemay, 2015         -
#------------------------------------
# This program generates a Morse code string
# which contains at one place or another all of the 
# characters present in the CODE list.
#
# It is inspired by the De Bruijn sequence approach:
# https://en.wikipedia.org/wiki/De_Bruijn_sequence
# Samy Kamkar's explanation: https://youtu.be/iSSRaIU9_Vc?t=259
# Instead of optimizing the sequence, it arrived at 32 bits, which is 
# storable as a single uint32 variable, or 4 uint8 bytes.

# It generates a lookup table, where each byte contains 
# information about the position of the character in the master
# string, and the length.  

# Therefore, the total space required for the lookup table and the master
# string is 26 bytes (alpha) + 10 bytes (numbers) + 4 bytes (master string)
# which equals 40 bytes.

import math 
import os

#from http://code.activestate.com/recipes/578407-simple-morse-code-translator-in-python/
CODE = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
     	'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
        
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' 
        }
		
#starting alphabet - not optimized, but functional
sequence = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"		


# Slide over previous string to see if there is a match;
#  if not, append partially or completely
def induced_fitting(growing_string, character):
	
	#check if string already exists
	if character not in growing_string:
		
		# for every character
		for i in range(len(character), 0, -1):
			
			# check if string can be fitted partially on the tail
			if growing_string.endswith(character[:i]):

				#partial tail found.  Add remainder and exit.
				remainder = character[i-len(character):]
				growing_string = growing_string + remainder
				break
				
		else: # "else" related to the FOR loop - no match found.
			#add end to master string
			growing_string = growing_string + character
			
	return growing_string
	
	
	
# Match every character to the master string.  Either find a match in the previous 
# string, partially append, or completely append.
def evaluate_alphabet(alphabet):

	# start off the sequence
	pseudo_debruijn_string = induced_fitting(CODE[alphabet[0]], CODE[alphabet[1]])
	
	# go over every character
	for i in range(1, len(alphabet)):

		pseudo_debruijn_string = induced_fitting(pseudo_debruijn_string, CODE[alphabet[i]])
		print(pseudo_debruijn_string)

	return pseudo_debruijn_string
	
	
	
# convert the position and length to a single byte
def translate_to_binary(master_string, character):
	# find position of character in string
	position = master_string.find(character)

	#convert length to binary
	length = len(character)
	
	#convert 5 first bits to position(xxxxx---), 3 last bits to length (-----xxx)
	return (format((position * 2**3 + length), '#04x')).upper()

	
	
# return morse character from combination byte
def translate_to_morse(master_string, character):

	char_position = math.floor(int(character, 16) / 2**3)
	char_length = int(character, 16) % 2**3
	for i in range(char_length):
		print(master_string[char_position + i], end="")
	print()

	
	
	
	
# ------------------------------------	
# program start
# ------------------------------------	

print("#####################################")
print("#       Morse Code Optimizer        #")
print("#       Mathieu Lemay, 2015         #")
print("#####################################")
print()	

# calculate original length, 1 bytes per dot/dash
total_starting_length = 0
for key, value in list(CODE.items()):
	total_starting_length = total_starting_length + len(value)
print("Total starting length:", total_starting_length, "bytes")

# generate master morse list
master_morse = evaluate_alphabet(sequence)

# get number of bytes required to represent master sequence
master_morse_length = math.ceil(len(master_morse) / 8)
print("Master Morse sequence:", master_morse, "(", len(master_morse), "bits long)\n")
master_morse_binary = master_morse.replace(".", "0")
master_morse_binary = master_morse_binary.replace("-", "1")
master_morse_binary = int(master_morse_binary, 2)
master_morse_binary = (format(master_morse_binary, '#04x')).upper()
print("Master Morse in hex: ", master_morse_binary)
print("\n######################\n")

#generate lookup table
BINCODE = {}
print("Generating lookup table:")
for char in sequence:
	BINCODE[char] = translate_to_binary(master_morse, CODE[char])
	print(char, ":  ", translate_to_binary(master_morse, CODE[char]))
print("\n######################\n")


# test sequence
hello = "HELLOWORLD"
print("Printing \"HELLOWORLD\":")
for i in range(len(hello)):

	#go over every character and print Morse sequence
	translate_to_morse(master_morse, BINCODE[hello[i]])

print("\n######################\n")

	
# evaluate success:
new_length = len(BINCODE) + master_morse_length
print("Original memory cost: ", total_starting_length, " bytes")
print("New memory cost: ", new_length, " bytes")
print("Memory use reduction: ", round(((1 - (new_length / total_starting_length)) * 100), 1), "%")

os.system("pause")