#############################################################
# Gets rid of duplicates in the json file, makes lower case and sorts
# to run:
# python dupsorter.py
############################################################

import json


def main():
	with open('../src/ont_dict.json') as json_file:
		ontology = json.load(json_file)
	for key in ontology["ontology"]:
		ontology["ontology"][key] = list(set(ontology["ontology"][key]))
		ontology["ontology"][key] = [i.lower() for i in ontology["ontology"][key]]
		ontology["ontology"][key].sort()
	
	print(ontology)
	with open('../src/ont_dict.json', 'w') as json_file: 
		json.dump(ontology, json_file)

if __name__ == '__main__':
	main()