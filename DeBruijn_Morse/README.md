# Morse Code Master List Optimized By Debruijn Sequence

The following files are intended to show the ability optimizing the memory storage of a code dictionary (in this case, Morse) using a Debruijn sequence.

## References
  * [Debruijn Sequences](https://en.wikipedia.org/wiki/De_Bruijn_sequence)
	
## Functionality
  * *morsecodedebruijn1.py* starts with each character code, and **slides** the next character code over that initial master sequence.  If no complete match is found, the code is added to the end of the string.
  * *morsecodedebruijn2.py* performs the same activities as *morsecodedebruijn1.py*, but now alters the sequence of letters and numbers to find a more optimal layout.  
	
## Example 
Considering the first five letters of the Morse code ("A"=".-", "B"="-...", "C"="-.-.", "D"="-..", "E"="."), we can assume the following fit:

A:			**.-**
A+B:		.**-...** (They match on the dash)
A+B+C:		.-...**-.-.** (No match found) 
A+B+C+D:	.**-..**.-.-. ("D" matches on the first dash)
A+B+C+D+E:  **.**-...-.-. (Match found on the first dot)