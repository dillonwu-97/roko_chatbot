######################################################################
# Extracts tables from wikipedia
# Usage: 
# python classer.py input.txt
# This is specific to emora stdm
# It takes as input all of the transition functions and then generates the important auto() states
######################################################################

import argparse
import sys

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("input", help = "file to be read in")
	args = parser.parse_args()

	uniq = []
	with open(args.input, "r") as f:
		for i in f:
			try:
				# print(i)
				before_arrow = (i.split("State.")[1]).split(",")[0]
				uniq.append(before_arrow)
			except:
				continue
			try:
				after_arrow = (i.split("State.")[2]).split(",")[0].split(")")[0]
				uniq.append(after_arrow)
			except:
				continue
	uniq = list(set(uniq))
	uniq.sort()
	for i in uniq:
		print(i + str("= auto()"))

if __name__ == "__main__":
	main()

