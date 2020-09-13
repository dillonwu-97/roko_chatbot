######################################################################
# Extracts tables from wikipedia
# Usage: 
# python grapher.py input.txt label
# input.txt must be in the following example format:
# Start example: 	
#	df.add_system_transition(State.fS1bb, State.fU2a, '[!"thats really interesting."#fave_games]')
# 	df.add_system_transition (State.fS1c, State.fU2a, '[!#fave_games]')
# 	df.add_system_transition(State.fS1a, State.fU2b, r'[!#SPECIFIC1]')
# 	# Specific
# 	df.add_user_transition(State.fU2b, State.fS2ba, '[$ans1=#ONT("specAnswer1")]') #Specific
# 	df.set_error_successor(State.fU2b, State.fS2bb)
# 	df.set_error_successor(State.fU2a, State.fS2bb)
# End example:
######################################################################

import argparse
import sys
import re

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("input", help = "file to be read in")
	parser.add_argument("label", help = "type 'true' or 'false' for whether or not you want a label")
	parser.add_argument("module", help = 'module: type in none, meta, health specific, general, social, or learning')
	args = parser.parse_args()


	module = {
		"meta": "m",
		"health": "h",
		"specific": "f",
		"general": "g",
		"social": "s",
		"learning": "L",
		"none": None

	}

	colors = {
		"m": "orchid1",
		"h": "lawngreen",
		"f": "mediumpurple1",
		"g": "cyan",
		"s": "yellow",
		"L": "orange",
		"none": None

	}

	# initializing empty dictionary of lists
	colored_nodes = {}
	for i in colors.keys():
		colored_nodes[i] = []

	with open(args.input, "r") as f:
		mod = module[args.module.lower()]
		for i in f:
			try:
				# print(i)
				before_arrow = (i.split("State.")[1]).split(",")[0]
				after_arrow = (i.split("State.")[2]).split(",")[0].split(")")[0]
				if before_arrow[0] == mod or after_arrow[0] == mod or mod == None:
					color = before_arrow[0]
					# print(color)
					if args.label == 'true':
						# print('HI')
						# print(i.split("State.")[2].split(",")[1])
						try:
							label = (i.split("State.")[2].split(",")[1]).replace(")", "").replace("'", "").replace("\"","").rstrip()
							label = label.split(" ")
							label_with_space = []
							for i in range(len(label)):
								label_with_space.append(label[i])
								# print(label[i])
								if i%5 == 0 and i != 0:
									label_with_space.append('\\n')
							label = " ".join(label_with_space)

						except:
							label = "error"
						colored_nodes[color].append("%s->%s[label=\"%s\"]" %(before_arrow, after_arrow, label))
					else:
						colored_nodes[color].append("%s->%s" %(before_arrow, after_arrow))
			except:
				continue
	# print(colored_nodes["g"])
	for key in sorted(colored_nodes.keys()):
		if key == "none":
			continue
		print("node [style = filled, color = %s] {" %(colors[key]))
		for i in colored_nodes[key]:
			print(i)
		print("}")





if __name__ == "__main__":
	main()