######################################################################
# Takes a word/phrase in a file and replaces it with another word/phrase
# Usage: 
# python replacer.py file_to_replace "old_string" "new_string"
######################################################################

import fileinput
import argparse

# This function converts a string of letters to what you want it to be
def convert(file, string_from, string_to):
	with fileinput.FileInput(file, inplace=True, backup='.bak') as file:
	    for line in file:
	        print(line.replace(string_from, string_to), end='')

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help = "file to be read in")
	parser.add_argument("string_from", help = "string you want to replace")
	parser.add_argument("string_to", help = "string you want to make it become")
	args = parser.parse_args()
	convert(args.file, args.string_from, args.string_to)

if __name__ == '__main__':
	main()